from mcp import Client

from t9_mcp_fundamentals.agent.mcp_clients.base import MCPClient


class HttpMCPClient(MCPClient):
    """Handles MCP server connection and tool execution via http"""

    def __init__(self, mcp_server_url: str) -> None:
        super().__init__()
        self.mcp_server_url = mcp_server_url

    async def __aenter__(self):
        # Client calls `server/discover` to select the protocol version. There is no handshake and no session:
        # every request carries its protocol version in `_meta`. Legacy servers (2025-11-25 and earlier) are
        # supported via fallback to the `initialize` handshake
        self.client = Client(self.mcp_server_url)
        await self.client.__aenter__()

        print(f"Connected to {self.client.server_info} (protocol version {self.client.protocol_version})")
        print(self.client.server_capabilities.model_dump_json(indent=2, exclude_none=True))

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.__aexit__(exc_type, exc_val, exc_tb)
            self.client = None
