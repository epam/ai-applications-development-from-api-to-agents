from abc import abstractmethod, ABC
from typing import Optional, Any

from mcp import Client
from mcp.types import CallToolResult, TextContent, GetPromptResult, ReadResourceResult, Resource, TextResourceContents, BlobResourceContents, Prompt
from pydantic import AnyUrl


class MCPClient(ABC):

    def __init__(self) -> None:
        self.client: Optional[Client] = None

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...

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

        print(f"    🔧 Calling `{tool_name}` with {tool_args}")

        tool_result: CallToolResult = await self.client.call_tool(tool_name, tool_args)

        if not tool_result.content:
            return "No content returned from tool"

        content = tool_result.content[0]
        print(f"    ⚙️: {content}\n")

        if isinstance(content, TextContent):
            return content.text

        return str(content)

    async def get_resources(self) -> list[Resource]:
        """Get available resources from MCP server"""
        if not self.client:
            raise RuntimeError("MCP client not connected.")

        try:
            result = await self.client.list_resources()
            return result.resources
        except Exception as e:
            print(f"Server doesn't support list_resources: {e}")
            return []

    async def get_resource(self, uri: AnyUrl) -> str:
        """Get specific resource content"""
        if not self.client:
            raise RuntimeError("MCP client not connected.")

        resource_result: ReadResourceResult = await self.client.read_resource(uri)
        content = resource_result.contents[0]

        if isinstance(content, TextResourceContents):
            return content.text
        elif isinstance(content, BlobResourceContents):
            return content.blob
        raise ValueError(f"Unknown resource type for {uri}")

    async def get_prompts(self) -> list[Prompt]:
        """Get available prompts from MCP server"""
        if not self.client:
            raise RuntimeError("MCP client not connected.")

        try:
            result = await self.client.list_prompts()
            return result.prompts
        except Exception as e:
            print(f"Server doesn't support list_prompts: {e}")
            return []

    async def get_prompt(self, name: str) -> str:
        """Get specific prompt content"""
        if not self.client:
            raise RuntimeError("MCP client not connected.")

        prompt_result: GetPromptResult = await self.client.get_prompt(name)

        combined_content = ""
        for message in prompt_result.messages:
            if hasattr(message, 'content') and isinstance(message.content, TextContent):
                combined_content += message.content.text + "\n"
            elif hasattr(message, 'content') and isinstance(message.content, str):
                combined_content += message.content + "\n"

        return combined_content.strip()