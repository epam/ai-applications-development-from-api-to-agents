from abc import abstractmethod, ABC
from typing import Optional, Any

from mcp import ClientSession


class T11MCPClient(ABC):

    def __init__(self) -> None:
        self.session: Optional[ClientSession] = None

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...

    @abstractmethod
    async def get_tools(self) -> list[dict[str, Any]]:
        """Get available tools from MCP server"""
        ...

    @abstractmethod
    async def call_tool(self, tool_name: str, tool_args: dict[str, Any]) -> Any:
        """Call a specific tool on the MCP server"""
        ...
