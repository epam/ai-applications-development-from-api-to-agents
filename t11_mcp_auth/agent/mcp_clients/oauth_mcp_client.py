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
        #TODO:
        # 1. Await `self.token_manager.authenticate()` to run the PKCE browser flow
        # 2. Await `self.token_manager.auth_headers()`, assign to `headers`
        # 3. Create `httpx2.AsyncClient(headers=headers)`, assign to `self._http_client`
        # 4. Create `Client(streamable_http_client(self.mcp_server_url, http_client=self._http_client))`,
        #    assign to `self.client`
        # 5. Await `self.client.__aenter__()` (it calls `server/discover`, there is no handshake and no session)
        # 6. Print f"Connected to {self.client.server_info} (protocol version {self.client.protocol_version})"
        #    and `self.client.server_capabilities.model_dump_json(indent=2, exclude_none=True)`
        # 7. Return `self`
        raise NotImplementedError()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        #TODO:
        # 1. If `self.client` is set, await `self.client.__aexit__(exc_type, exc_val, exc_tb)` and set `self.client = None`
        # 2. If `self._http_client` is set, await `self._http_client.aclose()` and set `self._http_client = None`
        #    (the transport doesn't close an http client that was passed to it)
        raise NotImplementedError()

    async def get_tools(self) -> list[dict[str, Any]]:
        """Get available tools from MCP server"""
        #TODO:
        # 1. If `self.client` is not set, raise RuntimeError("MCP client not connected")
        # 2. Call `await self.client.list_tools()`, assign to `tools`
        # 3. Return a list of dicts built from `tools.tools`:
        #       [
        #           {
        #               "type": "function",
        #               "function": {
        #                   "name": tool.name,
        #                   "description": tool.description,
        #                   "parameters": tool.input_schema
        #               }
        #           }
        #           for tool in tools.tools
        #       ]
        raise NotImplementedError()

    async def call_tool(self, tool_name: str, tool_args: dict[str, Any]) -> Any:
        """
        Call a tool on the MCP server.
        Proactively refreshes the token before it expires.
        """
        #TODO:
        # 1. If `self.client` is not set, raise RuntimeError("MCP client not connected")
        # 2. Print f"    🔧 Calling `{tool_name}` with {tool_args}"
        # 3. If `self.token_manager.is_token_expired()`:
        #       - Print "    🔄 Token expired — refreshing..."
        #       - Await `self._refresh_token()`
        # 4. Return `await self._do_call_tool(tool_name, tool_args)`
        raise NotImplementedError()

    async def _do_call_tool(self, tool_name: str, tool_args: dict[str, Any]) -> Any:
        #TODO:
        # 1. Call `await self.client.call_tool(tool_name, tool_args)`,
        #    assign to `tool_result` (type hint: CallToolResult)
        # 2. If `tool_result.content` is empty, return "No content returned from tool"
        # 3. Get `content = tool_result.content[0]`, print f"    ⚙️: {content}\n"
        # 4. If `content` is an instance of `TextContent`, return `content.text`
        # 5. Return `str(content)`
        raise NotImplementedError()

    async def _refresh_token(self) -> None:
        """Refresh OAuth token and send it with the next requests"""
        #TODO:
        # 1. Await `self.token_manager.refresh()`
        # 2. Update headers of the http client: `self._http_client.headers.update(await self.token_manager.auth_headers())`
        #    Every MCP request is a separate HTTP POST (stateless MCP, no session), so there is nothing to reconnect
        # 3. Print "    ✅ Next requests will use the fresh token"
        raise NotImplementedError()
