from typing import Optional, Any

from mcp import Client
from mcp.types import CallToolResult, TextContent


class MCPClient:
    """Handles MCP server connection and tool execution"""

    def __init__(self, mcp_server_url: str) -> None:
        self.server_url = mcp_server_url
        self.client: Optional[Client] = None

    @classmethod
    async def create(cls, mcp_server_url: str) -> 'MCPClient':
        """Async factory method to create and connect MCPClient"""
        instance = cls(mcp_server_url)
        await instance.connect()
        return instance

    async def connect(self):
        """Connect to MCP server"""
        # Client calls `server/discover` to select the protocol version. It falls back to the legacy
        # `initialize` handshake only if the server doesn't support stateless MCP (2026-07-28)
        self.client = Client(self.server_url)
        await self.client.__aenter__()

        print(f"Connected to {self.client.server_info} (protocol version {self.client.protocol_version})")
        print(self.client.server_capabilities.model_dump_json(indent=2, exclude_none=True))

    async def close(self):
        """Close connection to MCP server"""
        if self.client:
            await self.client.__aexit__(None, None, None)
            self.client = None

    async def get_tools(self) -> list[dict[str, Any]]:
        """Get available tools from MCP server"""
        if not self.client:
            raise RuntimeError("MCP client not connected. Call connect() first.")

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
        """Call a specific tool on the MCP server"""
        if not self.client:
            raise RuntimeError("MCP client not connected. Call connect() first.")

        print(f"    Calling `{tool_name}` with {tool_args}")

        tool_result: CallToolResult = await self.client.call_tool(tool_name, tool_args)
        content = tool_result.content

        print(f"    ⚙️: {content}\n")

        if content and isinstance(content[0], TextContent):
            return content[0].text

        return content
