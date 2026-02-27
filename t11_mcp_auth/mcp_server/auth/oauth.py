import os

import httpx
from jose import jwt, JWTError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

# ==================== CONFIGURATION ====================

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://localhost:8089")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "mcp-realm")
REQUIRED_ROLE = os.getenv("MCP_REQUIRED_ROLE", "mcp-tools-access")

ISSUER = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}"
JWKS_URL = f"{ISSUER}/protocol/openid-connect/certs"

# ==================== JWKS CACHE ====================

# Public keys are fetched once from Keycloak and cached in memory.
# This avoids a round-trip to Keycloak on every MCP request.
# Cache is invalidated on server restart; for production you'd add TTL-based refresh.
_jwks_cache: dict | None = None


async def _get_jwks() -> dict:
    """Fetch and cache Keycloak public keys (JWKS)"""
    global _jwks_cache
    if _jwks_cache is None:
        print(f"🔑 Fetching JWKS from {JWKS_URL}")
        async with httpx.AsyncClient() as client:
            response = await client.get(JWKS_URL)
            response.raise_for_status()
            _jwks_cache = response.json()
        print("🔑 JWKS cached successfully")
    return _jwks_cache


# ==================== MIDDLEWARE ====================

class JWTAuthMiddleware(BaseHTTPMiddleware):
    """
    Starlette middleware that:
      1. Extracts the Bearer token from the Authorization header
      2. Validates JWT signature using Keycloak public keys (JWKS)
      3. Verifies token issuer and expiry
      4. Checks that the user has the required realm role
    """

    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("Authorization", "")

        # ── Step 1: Check header presence ──────────────────────────────
        if not auth_header.startswith("Bearer "):
            return JSONResponse(
                {"error": "Unauthorized", "detail": "Missing or malformed Authorization header"},
                status_code=401
            )

        token = auth_header.removeprefix("Bearer ")

        # ── Step 2: Validate JWT signature + claims ─────────────────────
        try:
            jwks = await _get_jwks()
            claims = jwt.decode(
                token,
                jwks,
                algorithms=["RS256"],
                issuer=ISSUER,
                options={"verify_aud": False}  # audience check not needed for our setup
            )
        except JWTError as e:
            return JSONResponse(
                {"error": "Unauthorized", "detail": f"Invalid token: {e}"},
                status_code=401
            )

        # ── Step 3: Check realm role ────────────────────────────────────
        # Keycloak embeds roles in: claims["realm_access"]["roles"]
        realm_roles: list[str] = claims.get("realm_access", {}).get("roles", [])

        if REQUIRED_ROLE not in realm_roles:
            return JSONResponse(
                {
                    "error": "Forbidden",
                    "detail": f"Role '{REQUIRED_ROLE}' is required. User has roles: {realm_roles}"
                },
                status_code=403
            )

        print(f"✅ Authenticated: {claims.get('preferred_username')} | roles: {realm_roles}")
        return await call_next(request)
