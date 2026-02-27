import asyncio
import base64
import hashlib
import os
import secrets
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Event, Thread
from urllib.parse import parse_qs, urlencode, urlparse

import httpx

# ==================== KEYCLOAK CONFIGURATION ====================

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://localhost:8089")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "mcp-realm")
CLIENT_ID = os.getenv("MCP_CLIENT_ID", "mcp-client")

REDIRECT_PORT = 9999
REDIRECT_URI = f"http://localhost:{REDIRECT_PORT}/callback"

_BASE = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect"
AUTH_ENDPOINT = f"{_BASE}/auth"
TOKEN_ENDPOINT = f"{_BASE}/token"


# ==================== PKCE HELPERS ====================

def _generate_pkce_pair() -> tuple[str, str]:
    """
    Generate PKCE code_verifier and code_challenge (S256 method).

    code_verifier  — random URL-safe string (43-128 chars)
    code_challenge — BASE64URL(SHA256(code_verifier))
    """
    code_verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    return code_verifier, code_challenge


def _build_auth_url(code_challenge: str, state: str) -> str:
    """Build the Keycloak /authorize URL with PKCE parameters"""
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile",
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    return f"{AUTH_ENDPOINT}?{urlencode(params)}"


# ==================== LOCAL CALLBACK SERVER ====================

def _run_callback_server(code_holder: dict, ready_event: Event) -> None:
    """
    Starts a temporary HTTP server on localhost:9999 to receive the
    authorization code from Keycloak's redirect.

    Runs in a background thread; signals ready_event when code arrives.
    """

    class _CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse(self.path)
            if parsed.path == "/callback":
                params = parse_qs(parsed.query)
                code_holder["code"] = params.get("code", [None])[0]
                code_holder["state"] = params.get("state", [None])[0]
                code_holder["error"] = params.get("error", [None])[0]

                # Send a friendly browser response
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()

                if code_holder["code"]:
                    body = b"""
                    <html><body style="font-family:monospace;background:#0a0c10;color:#34d399;
                                       display:flex;align-items:center;justify-content:center;
                                       height:100vh;margin:0;font-size:18px;">
                        <div>&#10003; Authentication successful. You can close this tab.</div>
                    </body></html>
                    """
                else:
                    body = b"""
                    <html><body style="font-family:monospace;background:#0a0c10;color:#f87171;
                                       display:flex;align-items:center;justify-content:center;
                                       height:100vh;margin:0;font-size:18px;">
                        <div>&#10007; Authentication failed. Check terminal for details.</div>
                    </body></html>
                    """
                self.wfile.write(body)
                ready_event.set()

        def log_message(self, format, *args):  # silence default request logging
            pass

    server = HTTPServer(("localhost", REDIRECT_PORT), _CallbackHandler)
    server.timeout = 1
    while not ready_event.is_set():
        server.handle_request()
    server.server_close()


# ==================== TOKEN EXCHANGE ====================

async def _exchange_code_for_tokens(code: str, code_verifier: str) -> dict:
    """POST the authorization code + code_verifier to get access/refresh tokens"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TOKEN_ENDPOINT,
            data={
                "grant_type": "authorization_code",
                "client_id": CLIENT_ID,
                "redirect_uri": REDIRECT_URI,
                "code": code,
                "code_verifier": code_verifier,
            }
        )
        response.raise_for_status()
        return response.json()


async def _refresh_access_token(refresh_token: str) -> dict:
    """Use the refresh_token to get a new access_token without user interaction"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TOKEN_ENDPOINT,
            data={
                "grant_type": "refresh_token",
                "client_id": CLIENT_ID,
                "refresh_token": refresh_token,
            }
        )
        response.raise_for_status()
        return response.json()


# ==================== OAUTH TOKEN MANAGER ====================

class OAuthTokenManager:
    """
    Manages the full OAuth 2.0 + PKCE lifecycle:
      - Initial browser-based authorization
      - Stores access_token + refresh_token
      - Transparently refreshes tokens when expired

    Usage:
        manager = OAuthTokenManager()
        await manager.authenticate()          # opens browser once
        headers = await manager.auth_headers()  # always returns valid headers
    """

    def __init__(self):
        self._access_token: str | None = None
        self._refresh_token: str | None = None
        self._expires_at: float | None = None

    async def authenticate(self) -> None:
        """
        Run the PKCE authorization code flow:
        1. Generate PKCE pair + state
        2. Open browser → Keycloak login page
        3. Wait for callback with auth code
        4. Exchange code for tokens
        """
        code_verifier, code_challenge = _generate_pkce_pair()
        state = secrets.token_urlsafe(16)

        # ── Start callback server in background thread ──────────────────
        code_holder: dict = {}
        ready_event = Event()
        Thread(
            target=_run_callback_server,
            args=(code_holder, ready_event),
            daemon=True
        ).start()

        # ── Open browser ────────────────────────────────────────────────
        auth_url = _build_auth_url(code_challenge, state)
        print(f"\n🌐 Opening browser for Keycloak login...")
        print(f"   URL: {auth_url}\n")
        webbrowser.open(auth_url)

        # ── Wait for callback (blocking, up to 120s) ────────────────────
        print("⏳ Waiting for authentication callback on http://localhost:9999/callback ...")
        await asyncio.get_event_loop().run_in_executor(
            None, lambda: ready_event.wait(timeout=120)
        )

        if not ready_event.is_set():
            raise TimeoutError("OAuth callback not received within 120 seconds")

        if code_holder.get("error"):
            raise RuntimeError(f"OAuth error from Keycloak: {code_holder['error']}")

        if code_holder.get("state") != state:
            raise RuntimeError("OAuth state mismatch — possible CSRF attack")

        auth_code = code_holder["code"]
        if not auth_code:
            raise RuntimeError("No authorization code received in callback")

        # ── Exchange code for tokens ────────────────────────────────────
        print("🔄 Exchanging authorization code for tokens...")
        tokens = await _exchange_code_for_tokens(auth_code, code_verifier)
        self._store_tokens(tokens)
        print(f"✅ Authenticated! Token expires in {tokens.get('expires_in')}s\n")

    def _store_tokens(self, tokens: dict) -> None:
        self._access_token = tokens["access_token"]
        self._refresh_token = tokens.get("refresh_token")
        expires_in = tokens.get("expires_in", 300)
        self._expires_at = time.time() + expires_in - 30  # 30s buffer

    def is_token_expired(self) -> bool:
        """Returns True if the access token is missing or within 30s of expiry"""
        return self._expires_at is None or time.time() >= self._expires_at

    async def refresh(self) -> None:
        """Refresh the access token using the stored refresh_token"""
        if not self._refresh_token:
            raise RuntimeError("No refresh token available — re-authentication required")
        print("🔄 Refreshing access token...")
        tokens = await _refresh_access_token(self._refresh_token)
        self._store_tokens(tokens)
        print("✅ Token refreshed")

    async def auth_headers(self) -> dict[str, str]:
        """Return Authorization headers with the current access token"""
        if not self._access_token:
            raise RuntimeError("Not authenticated — call authenticate() first")
        return {"Authorization": f"Bearer {self._access_token}"}
