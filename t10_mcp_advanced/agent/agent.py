import json
from collections import defaultdict
from typing import Any

from openai import AsyncOpenAI

from commons.models.message import Message
from commons.models.role import Role
from t10_mcp_advanced.agent.clients.custom_mcp_client import CustomMCPClient
from t10_mcp_advanced.agent.clients.mcp_client import MCPClient


class CustomAgentMCP:
    """Handles AI model interactions and integrates with MCP client"""

    def __init__(
            self,
            api_key: str,
            model: str,
            tools: list[dict[str, Any]],
            tool_name_client_map: dict[str, MCPClient | CustomMCPClient]
    ):
        self.model = model
        self.tools = tools
        self.tool_name_client_map = tool_name_client_map
        self.openai = AsyncOpenAI(api_key=api_key)

    def _collect_tool_calls(self, tool_deltas):
        """Convert streaming tool call deltas to complete tool calls"""
        tool_dict = defaultdict(lambda: {"id": None, "function": {"arguments": "", "name": None}, "type": None})

        for delta in tool_deltas:
            idx = delta.index
            if delta.id: tool_dict[idx]["id"] = delta.id
            if delta.function.name: tool_dict[idx]["function"]["name"] = delta.function.name
            if delta.function.arguments: tool_dict[idx]["function"]["arguments"] += delta.function.arguments
            if delta.type: tool_dict[idx]["type"] = delta.type

        return list(tool_dict.values())

    async def _stream_response(self, messages: list[Message]) -> Message:
        """Stream OpenAI response and handle tool calls"""
        stream = await self.openai.chat.completions.create(
            **{
                "model": self.model,
                "messages": [msg.to_dict() for msg in messages],
                "tools": self.tools,
                "temperature": 0.0,
                "stream": True
            }
        )

        content = ""
        tool_deltas = []

        print("🤖: ", end="", flush=True)

        async for chunk in stream:
            delta = chunk.choices[0].delta

            # Stream content
            if delta.content:
                print(delta.content, end="", flush=True)
                content += delta.content

            if delta.tool_calls:
                tool_deltas.extend(delta.tool_calls)

        print()
        return Message(
            role=Role.ASSISTANT,
            content=content,
            tool_calls=self._collect_tool_calls(tool_deltas) if tool_deltas else []
        )

    async def get_completion(self, messages: list[Message]) -> Message:
        """Process user query with streaming and tool calling"""
        ai_message: Message = await self._stream_response(messages)

        # Check if any tool calls are present and perform them
        if ai_message.tool_calls:
            messages.append(ai_message)
            await self._call_tools(ai_message, messages)
            # recursively calling agent with tool messages
            return await self.get_completion(messages)

        return ai_message

    async def _call_tools(self, ai_message: Message, messages: list[Message]):
        """Execute tool calls using MCP client"""
        for tool_call in ai_message.tool_calls:
            tool_name = tool_call["function"]["name"]
            tool_args = json.loads(tool_call["function"]["arguments"])

            try:
                client = self.tool_name_client_map.get(tool_name)
                if not client:
                    raise Exception(f"Unable to call {tool_name}. MCP client not found.")

                tool_result = await client.call_tool(tool_name, tool_args)

                # Add tool result to history
                messages.append(
                    Message(
                        role=Role.TOOL,
                        content=str(tool_result),
                        tool_call_id=tool_call["id"],
                    )
                )
            except Exception as e:
                error_msg = f"Error: {e}"
                print(f"Error: {error_msg}")
                messages.append(
                    Message(
                        role=Role.TOOL,
                        content=error_msg,
                        tool_call_id=tool_call["id"],
                    )
                )
