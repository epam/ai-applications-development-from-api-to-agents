from typing import Any, Optional

import httpx2
from mcp import Client
from mcp.client.streamable_http import streamable_http_client
from mcp.types import CallToolResult, TextContent

from t11_mcp_auth.agent.mcp_clients._base import T11MCPClient
from t11_mcp_auth.agent.mcp_clients._oauth_keycloak import OAuthTokenManager


class OauthHttpMCPClient(T11MCPClient):
    """
    MCP client that authenticates via OAuth 2.0 + PKCE.

    On __aenter__:
      1. Runs the PKCE browser flow (opens Keycloak login once)
      2. Connects to the MCP server with the resulting Bearer token

    On tool calls:
      - Proactively refreshes the token before it expires. MCP is stateless (no session), so the new token
        is simply sent with the next request, there is nothing to reconnect
    """

    def __init__(self, mcp_server_url: str) -> None:
        super().__init__()
        self.mcp_server_url = mcp_server_url
        self.token_manager = OAuthTokenManager()
        self._http_client: Optional[httpx2.AsyncClient] = None

    async def __aenter__(self):
        # ── Step 1: Authenticate via browser PKCE flow ──────────────────
        await self.token_manager.authenticate()

        # ── Step 2: Build httpx2 client with Bearer token ────────────────
        headers = await self.token_manager.auth_headers()
        self._http_client = httpx2.AsyncClient(headers=headers)

        # ── Step 3: Connect to MCP server (server/discover, no session) ──
        self.client = Client(streamable_http_client(self.mcp_server_url, http_client=self._http_client))
        await self.client.__aenter__()

        print(f"Connected to {self.client.server_info} (protocol version {self.client.protocol_version})")
        print(self.client.server_capabilities.model_dump_json(indent=2, exclude_none=True))

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.__aexit__(exc_type, exc_val, exc_tb)
            self.client = None
        # The transport doesn't close an http client that was passed to it
        if self._http_client:
            await self._http_client.aclose()
            self._http_client = None

    async def get_tools(self) -> list[dict[str, Any]]:
        """Get available tools from MCP server"""
        if not self.client:
            raise RuntimeError("MCP client not connected")

        tools = await self.client.list_tools()
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.input_schema
                }
            }
            for tool in tools.tools
        ]

    async def call_tool(self, tool_name: str, tool_args: dict[str, Any]) -> Any:
        """
        Call a tool on the MCP server.
        Proactively refreshes the token before it expires.
        """
        if not self.client:
            raise RuntimeError("MCP client not connected")

        print(f"    🔧 Calling `{tool_name}` with {tool_args}")

        if self.token_manager.is_token_expired():
            print("    🔄 Token expired — refreshing...")
            await self._refresh_token()

        return await self._do_call_tool(tool_name, tool_args)

    async def _do_call_tool(self, tool_name: str, tool_args: dict[str, Any]) -> Any:
        tool_result: CallToolResult = await self.client.call_tool(tool_name, tool_args)

        if not tool_result.content:
            return "No content returned from tool"

        content = tool_result.content[0]
        print(f"    ⚙️: {content}\n")

        if isinstance(content, TextContent):
            return content.text
        return str(content)

    async def _refresh_token(self) -> None:
        """Refresh OAuth token and send it with the next requests"""
        await self.token_manager.refresh()

        # Every MCP request is a separate HTTP POST, so updating the header is enough
        self._http_client.headers.update(await self.token_manager.auth_headers())
        print("    ✅ Next requests will use the fresh token")
