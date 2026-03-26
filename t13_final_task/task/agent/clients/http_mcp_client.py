import logging
from typing import Optional, Any

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from mcp.types import CallToolResult, TextContent

from task.agent.clients.base_mcp_client import BaseMcpClient
from task.agent.models import McpToolModel

logger = logging.getLogger(__name__)


class HttpMcpClient(BaseMcpClient):

    def __init__(self, mcp_server_url: str) -> None:
        self.server_url = mcp_server_url
        self.session: Optional[ClientSession] = None
        self._streams_context = None
        self._session_context = None
        logger.debug("HttpMcpClient instance created", extra={"server_url": mcp_server_url})

    @classmethod
    async def create(cls, mcp_server_url: str) -> 'HttpMcpClient':
        logger.info("Creating HttpMcpClient", extra={"server_url": mcp_server_url})
        instance = cls(mcp_server_url)
        await instance.connect()
        return instance

    async def connect(self):
        logger.info("Connecting to MCP server", extra={"server_url": self.server_url})

        self._streams_context = streamable_http_client(self.server_url)
        read_stream, write_stream, _ = await self._streams_context.__aenter__()

        self._session_context = ClientSession(read_stream, write_stream)
        self.session: ClientSession = await self._session_context.__aenter__()

        init_result = await self.session.initialize()
        logger.info(
            "MCP session initialized",
            extra={
                "server_url": self.server_url,
                "init_result": init_result.model_dump()
            }
        )

    async def get_tools(self) -> list[McpToolModel]:
        if not self.session:
            logger.error("Attempted to get tools without active session")
            raise RuntimeError("MCP client not connected. Call connect() first.")

        logger.debug("Fetching tools from MCP server", extra={"server_url": self.server_url})
        tools = await self.session.list_tools()

        tool_list = [
            McpToolModel(
                name=tool.name,
                description=tool.description,
                parameters=tool.inputSchema,
            )
            for tool in tools.tools
        ]

        logger.info(
            "Retrieved tools from MCP server",
            extra={
                "server_url": self.server_url,
                "tool_count": len(tool_list),
                "tool_names": [tool.name for tool in tool_list]
            }
        )

        return tool_list

    async def call_tool(self, tool_name: str, tool_args: dict[str, Any]) -> Any:
        """Call a specific tool on the MCP server"""
        if not self.session:
            logger.error("Attempted to call tool without active session", extra={"tool_name": tool_name})
            raise RuntimeError("MCP client not connected. Call connect() first.")

        logger.info(
            "Calling MCP tool",
            extra={
                "server_url": self.server_url,
                "tool_name": tool_name,
                "tool_args": tool_args
            }
        )

        tool_result: CallToolResult = await self.session.call_tool(tool_name, tool_args)
        content = tool_result.content

        logger.debug(
            "MCP tool result received",
            extra={
                "tool_name": tool_name,
                "content": content
            }
        )

        if len(content) == 1 and isinstance(content[0], TextContent):
            return content[0].text

        return content