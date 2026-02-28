from typing import Any

import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from mcp.types import CallToolResult, TextContent

from t11_mcp_auth.agent.mcp_clients._base import T11MCPClient


class ApiKeyMCPClient(T11MCPClient):
    """Handles MCP server connection and tool execution via http"""

    def __init__(self, mcp_server_url: str, api_key: str) -> None:
        super().__init__()
        self.mcp_server_url = mcp_server_url
        self.api_key = api_key
        self._streams_context = None
        self._session_context = None

    async def __aenter__(self):
        #TODO:
        # 1. Create `httpx.AsyncClient` with headers={"X-API-Key": self.api_key}, assign to `http_client`
        # 2. Call `streamable_http_client(self.mcp_server_url, http_client=http_client)`,
        #    assign to `self._streams_context`
        # 3. Await `self._streams_context.__aenter__()`, unpack result into `read_stream, write_stream, _`
        # 4. Create `ClientSession(read_stream, write_stream)`, assign to `self._session_context`
        # 5. Await `self._session_context.__aenter__()`, assign result to `self.session`
        # 6. Await `self.session.initialize()`, assign to `init_result`,
        #    print `init_result.model_dump_json(indent=2)`
        # 7. Return `self`
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
        # 1. If `self.session` is not set, raise RuntimeError("MCP client not connected. Call connect() first.")
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
        """Call a specific tool on the MCP server"""
        #TODO:
        # 1. If `self.session` is not set, raise RuntimeError("MCP client not connected. Call connect() first.")
        # 2. Print f"    🔧 Calling `{tool_name}` with {tool_args}"
        # 3. Call `await self.session.call_tool(tool_name, tool_args)`,
        #    assign to `tool_result` (type hint: CallToolResult)
        # 4. If `tool_result.content` is empty, return "No content returned from tool"
        # 5. Get `content = tool_result.content[0]`, print f"    ⚙️: {content}\n"
        # 6. If `content` is an instance of `TextContent`, return `content.text`
        # 7. Return `str(content)`
        raise NotImplementedError()