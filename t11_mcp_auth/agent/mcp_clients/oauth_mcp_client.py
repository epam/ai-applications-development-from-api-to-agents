from typing import Any

import httpx
from mcp import ClientSession
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
      - Automatically retries with a refreshed token on 401 responses
    """

    def __init__(self, mcp_server_url: str) -> None:
        super().__init__()
        self.mcp_server_url = mcp_server_url
        self.token_manager = OAuthTokenManager()
        self._streams_context = None
        self._session_context = None
        self.session: ClientSession | None = None

    async def __aenter__(self):
        # ── Step 1: Authenticate via browser PKCE flow ──────────────────
        await self.token_manager.authenticate()

        # ── Step 2: Build httpx client with Bearer token ─────────────────
        headers = await self.token_manager.auth_headers()
        http_client = httpx.AsyncClient(headers=headers)

        # ── Step 3: Connect MCP session ──────────────────────────────────
        self._streams_context = streamable_http_client(
            self.mcp_server_url,
            http_client=http_client,
        )
        read_stream, write_stream, _ = await self._streams_context.__aenter__()

        self._session_context = ClientSession(read_stream, write_stream)
        self.session = await self._session_context.__aenter__()

        init_result = await self.session.initialize()
        print(init_result.model_dump_json(indent=2))

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session and self._session_context:
            await self._session_context.__aexit__(exc_type, exc_val, exc_tb)
        if self._streams_context:
            await self._streams_context.__aexit__(exc_type, exc_val, exc_tb)

    async def get_tools(self) -> list[dict[str, Any]]:
        """Get available tools from MCP server"""
        if not self.session:
            raise RuntimeError("MCP client not connected")

        tools = await self.session.list_tools()
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                }
            }
            for tool in tools.tools
        ]

    async def call_tool(self, tool_name: str, tool_args: dict[str, Any]) -> Any:
        """
        Call a tool on the MCP server.
        Proactively refreshes the token before it expires to avoid broken streams.
        """
        if not self.session:
            raise RuntimeError("MCP client not connected")

        print(f"    🔧 Calling `{tool_name}` with {tool_args}")

        if self.token_manager.is_token_expired():
            print("    🔄 Token expired — refreshing and reconnecting...")
            await self._reconnect_with_fresh_token()

        return await self._do_call_tool(tool_name, tool_args)

    async def _do_call_tool(self, tool_name: str, tool_args: dict[str, Any]) -> Any:
        tool_result: CallToolResult = await self.session.call_tool(tool_name, tool_args)

        if not tool_result.content:
            return "No content returned from tool"

        content = tool_result.content[0]
        print(f"    ⚙️: {content}\n")

        if isinstance(content, TextContent):
            return content.text
        return str(content)

    async def _reconnect_with_fresh_token(self) -> None:
        """Refresh OAuth token and re-establish the MCP session with the new token"""
        await self.token_manager.refresh()

        # Tear down old session
        if self._session_context:
            await self._session_context.__aexit__(None, None, None)
        if self._streams_context:
            await self._streams_context.__aexit__(None, None, None)

        # Re-connect with new token
        headers = await self.token_manager.auth_headers()
        http_client = httpx.AsyncClient(headers=headers)

        self._streams_context = streamable_http_client(
            self.mcp_server_url,
            http_client=http_client,
        )
        read_stream, write_stream, _ = await self._streams_context.__aenter__()

        self._session_context = ClientSession(read_stream, write_stream)
        self.session = await self._session_context.__aenter__()
        await self.session.initialize()
        print("    ✅ Reconnected with fresh token")
