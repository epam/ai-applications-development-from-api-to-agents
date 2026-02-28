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
        #TODO:
        # 1. Await `self.token_manager.authenticate()` to run the PKCE browser flow
        # 2. Await `self.token_manager.auth_headers()`, assign to `headers`
        # 3. Create `httpx.AsyncClient(headers=headers)`, assign to `http_client`
        # 4. Call `streamable_http_client(self.mcp_server_url, http_client=http_client)`,
        #    assign to `self._streams_context`
        # 5. Await `self._streams_context.__aenter__()`, unpack into `read_stream, write_stream, _`
        # 6. Create `ClientSession(read_stream, write_stream)`, assign to `self._session_context`
        # 7. Await `self._session_context.__aenter__()`, assign result to `self.session`
        # 8. Await `self.session.initialize()`, assign to `init_result`,
        #    print `init_result.model_dump_json(indent=2)`
        # 9. Return `self`
        raise NotImplementedError()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        #TODO:
        # 1. If `self.session` and `self._session_context` are set,
        #    await `self._session_context.__aexit__(exc_type, exc_val, exc_tb)`
        # 2. If `self._streams_context` is set,
        #    await `self._streams_context.__aexit__(exc_type, exc_val, exc_tb)`
        raise NotImplementedError()

    async def get_tools(self) -> list[dict[str, Any]]:
        """Get available tools from MCP server"""
        #TODO:
        # 1. If `self.session` is not set, raise RuntimeError("MCP client not connected")
        # 2. Call `await self.session.list_tools()`, assign to `tools`
        # 3. Return a list of dicts built from `tools.tools`:
        #       [
        #           {
        #               "type": "function",
        #               "function": {
        #                   "name": tool.name,
        #                   "description": tool.description,
        #                   "parameters": tool.inputSchema
        #               }
        #           }
        #           for tool in tools.tools
        #       ]
        raise NotImplementedError()

    async def call_tool(self, tool_name: str, tool_args: dict[str, Any]) -> Any:
        """
        Call a tool on the MCP server.
        Proactively refreshes the token before it expires to avoid broken streams.
        """
        #TODO:
        # 1. If `self.session` is not set, raise RuntimeError("MCP client not connected")
        # 2. Print f"    🔧 Calling `{tool_name}` with {tool_args}"
        # 3. If `self.token_manager.is_token_expired()`:
        #       - Print "    🔄 Token expired — refreshing and reconnecting..."
        #       - Await `self._reconnect_with_fresh_token()`
        # 4. Return `await self._do_call_tool(tool_name, tool_args)`
        raise NotImplementedError()

    async def _do_call_tool(self, tool_name: str, tool_args: dict[str, Any]) -> Any:
        #TODO:
        # 1. Call `await self.session.call_tool(tool_name, tool_args)`,
        #    assign to `tool_result` (type hint: CallToolResult)
        # 2. If `tool_result.content` is empty, return "No content returned from tool"
        # 3. Get `content = tool_result.content[0]`, print f"    ⚙️: {content}\n"
        # 4. If `content` is an instance of `TextContent`, return `content.text`
        # 5. Return `str(content)`
        raise NotImplementedError()

    async def _reconnect_with_fresh_token(self) -> None:
        """Refresh OAuth token and re-establish the MCP session with the new token"""
        #TODO:
        # 1. Await `self.token_manager.refresh()`
        # 2. If `self._session_context` is set,
        #    await `self._session_context.__aexit__(None, None, None)`
        # 3. If `self._streams_context` is set,
        #    await `self._streams_context.__aexit__(None, None, None)`
        # 4. Await `self.token_manager.auth_headers()`, assign to `headers`
        # 5. Create `httpx.AsyncClient(headers=headers)`, assign to `http_client`
        # 6. Call `streamable_http_client(self.mcp_server_url, http_client=http_client)`,
        #    assign to `self._streams_context`
        # 7. Await `self._streams_context.__aenter__()`, unpack into `read_stream, write_stream, _`
        # 8. Create `ClientSession(read_stream, write_stream)`, assign to `self._session_context`
        # 9. Await `self._session_context.__aenter__()`, assign result to `self.session`
        # 10. Await `self.session.initialize()`
        # 11. Print "    ✅ Reconnected with fresh token"
        raise NotImplementedError()