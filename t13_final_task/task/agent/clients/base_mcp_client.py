from abc import ABC, abstractmethod
from typing import Any

from task.agent.models import McpToolModel


class BaseMcpClient(ABC):

    @abstractmethod
    async def get_tools(self) -> list[McpToolModel]:
        """Get available tools from MCP server"""
        ...

    @abstractmethod
    async def call_tool(self, tool_name: str, tool_args: dict[str, Any]) -> Any:
        """Call a specific tool on the MCP server"""
        ...
