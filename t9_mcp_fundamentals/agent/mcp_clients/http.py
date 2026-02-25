from typing import Optional

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

from t9_mcp_fundamentals.agent.mcp_clients.base import MCPClient


class HttpMCPClient(MCPClient):
    """Handles MCP server connection and tool execution via http"""

    def __init__(self, mcp_server_url: str) -> None:
        super().__init__()
        self.mcp_server_url = mcp_server_url
        self._streams_context = None
        self._session_context = None

    async def __aenter__(self):
        #TODO:
        # 1. Call `streamable_http_client` method with `mcp_server_url` and assign to `self._streams_context`
        # 2. Call `await self._streams_context.__aenter__()` and assign to `read_stream, write_stream, _`
        # 3. Create `ClientSession(read_stream, write_stream)` and assign to `self._session_context`
        # 4. Call `await self._session_context.__aenter__()` and assign it to `self.session`
        # 5. Call `self.session.initialize()`, and print its result (to check capabilities of MCP server later)
        # 6. return self
        raise NotImplementedError()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        #TODO:
        # This is shutdown method.
        # If session is present and session context is present as well then shutdown the session context (__aexit__ method with params)
        # If streams context is present then shutdown the streams context (__aexit__ method with params)
        raise NotImplementedError()