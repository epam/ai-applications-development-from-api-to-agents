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
        self._streams_context = streamable_http_client(self.mcp_server_url)
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