from typing import Any, Optional

import httpx2
from mcp import Client
from mcp.client.streamable_http import streamable_http_client
from mcp.types import CallToolResult, TextContent

from t11_mcp_auth.agent.mcp_clients._base import T11MCPClient


class ApiKeyMCPClient(T11MCPClient):
    """Handles MCP server connection and tool execution via http"""

    def __init__(self, mcp_server_url: str, api_key: str) -> None:
        super().__init__()
        self.mcp_server_url = mcp_server_url
        self.api_key = api_key
        self._http_client: Optional[httpx2.AsyncClient] = None

    async def __aenter__(self):
        #TODO:
        # 1. Create `httpx2.AsyncClient` with headers={"X-API-Key": self.api_key}, assign to `self._http_client`
        #    (stateless MCP: every request is a separate POST, so the API key header is sent with each of them)
        # 2. Create `Client(streamable_http_client(self.mcp_server_url, http_client=self._http_client))`,
        #    assign to `self.client`
        # 3. Await `self.client.__aenter__()` (it calls `server/discover`, there is no handshake and no session)
        # 4. Print f"Connected to {self.client.server_info} (protocol version {self.client.protocol_version})"
        #    and `self.client.server_capabilities.model_dump_json(indent=2, exclude_none=True)`
        # 5. Return `self`
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
        # 1. If `self.client` is not set, raise RuntimeError("MCP client not connected. Call connect() first.")
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
        """Call a specific tool on the MCP server"""
        #TODO:
        # 1. If `self.client` is not set, raise RuntimeError("MCP client not connected. Call connect() first.")
        # 2. Print f"    🔧 Calling `{tool_name}` with {tool_args}"
        # 3. Call `await self.client.call_tool(tool_name, tool_args)`,
        #    assign to `tool_result` (type hint: CallToolResult)
        # 4. If `tool_result.content` is empty, return "No content returned from tool"
        # 5. Get `content = tool_result.content[0]`, print f"    ⚙️: {content}\n"
        # 6. If `content` is an instance of `TextContent`, return `content.text`
        # 7. Return `str(content)`
        raise NotImplementedError()