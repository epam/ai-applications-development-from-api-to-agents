import logging
from typing import Optional, Any

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.types import CallToolResult, TextContent

from task.agent.clients.base_mcp_client import BaseMcpClient
from task.agent.models import McpToolModel

logger = logging.getLogger(__name__)


class StdioMcpClient(BaseMcpClient):
    """Handles MCP server connection and tool execution via stdio"""

    def __init__(self, docker_image: str) -> None:
        self.docker_image = docker_image
        self.session: Optional[ClientSession] = None
        self._stdio_context = None
        self._session_context = None
        self._process = None
        logger.debug("StdioMCPClient instance created", extra={"docker_image": docker_image})

    @classmethod
    async def create(cls, docker_image: str) -> 'StdioMcpClient':
        """Async factory method to create and connect MCPClient"""
        logger.info("Creating StdioMCPClient", extra={"docker_image": docker_image})
        instance = cls(docker_image)
        await instance.connect()
        return instance

    async def connect(self):
        """Connect to MCP server via Docker"""
        server_params = StdioServerParameters(
            command="docker",
            args=["run", "--rm", "-i", self.docker_image]
        )

        logger.info("Starting Docker container for MCP", extra={"docker_image": self.docker_image})
        self._stdio_context = stdio_client(server_params)

        read_stream, write_stream = await self._stdio_context.__aenter__()

        self._session_context = ClientSession(read_stream, write_stream)
        self.session = await self._session_context.__aenter__()

        logger.debug("Initializing MCP session", extra={"docker_image": self.docker_image})
        init_result = await self.session.initialize()

        logger.info(
            "MCP session initialized via stdio",
            extra={
                "docker_image": self.docker_image,
                "capabilities": init_result.model_dump()
            }
        )

    async def get_tools(self) -> list[McpToolModel]:
        """Get available tools from MCP server"""
        if not self.session:
            logger.error("Attempted to get tools without active session", extra={"docker_image": self.docker_image})
            raise RuntimeError("MCP client not connected. Call connect() first.")

        logger.debug("Fetching tools from MCP server", extra={"docker_image": self.docker_image})
        tools_result = await self.session.list_tools()

        tool_list = [
            McpToolModel(
                name=tool.name,
                description=tool.description,
                parameters=tool.inputSchema,
            )
            for tool in tools_result.tools
        ]

        logger.info(
            "Retrieved tools from MCP server",
            extra={
                "docker_image": self.docker_image,
                "tool_count": len(tool_list),
                "tool_names": [tool.name for tool in tool_list]
            }
        )

        return tool_list

    async def call_tool(self, tool_name: str, tool_args: dict[str, Any]) -> Any:
        """Call a specific tool on the MCP server"""
        if not self.session:
            logger.error(
                "Attempted to call tool without active session",
                extra={"docker_image": self.docker_image, "tool_name": tool_name}
            )
            raise RuntimeError("MCP client not connected. Call connect() first.")

        logger.info(
            "Calling MCP tool via stdio",
            extra={
                "docker_image": self.docker_image,
                "tool_name": tool_name,
                "tool_args": tool_args
            }
        )

        tool_result: CallToolResult = await self.session.call_tool(tool_name, tool_args)

        if not tool_result.content:
            logger.warning(
                "Tool returned no content",
                extra={"tool_name": tool_name, "docker_image": self.docker_image}
            )
            return "No content returned from tool"

        content = tool_result.content[0]
        logger.debug(
            "MCP tool result received",
            extra={
                "tool_name": tool_name,
                "content": content
            }
        )

        if isinstance(content, TextContent):
            return content.text

        return str(content)