import json
import logging
from collections import defaultdict
from typing import AsyncGenerator

from openai import AsyncOpenAI

from t13_final_task.task.agent.models import Message
from t13_final_task.task.agent.models import Role
from t13_final_task.task.agent.guardrail import UMSDataGuardrail
from t13_final_task.task.agent.tools.base import BaseTool

logger = logging.getLogger(__name__)


class UMSAgent:
    """Handles AI model interactions and integrates with MCP client"""

    def __init__(
            self,
            api_key: str,
            model: str,
            tools: list[BaseTool]
    ):
        #TODO:
        # - Store tools as dict `tool.name: tool`
        # - Store tools schemas list
        # - Store model
        # - Init AsyncOpenAI
        # - Init UMSDataGuardrail
        raise NotImplementedError()

    async def response(self, messages: list[Message]) -> Message:
        """Non-streaming completion with tool calling support"""
        #TODO:
        # 1. Build request_data: model, messages (each .to_dict()), tools schemas, stream=False
        # 2. Call async_openai chat completions with request_data
        # 3. Build ai_message (Role.ASSISTANT) from response content
        # 4. If response has tool_calls, assign them to ai_message.tool_calls
        # 5. If ai_message has tool_calls: append ai_message to messages, call _call_tools(),
        #    then make recursive call
        # 6. Return ai_message
        raise NotImplementedError()

    async def stream_response(self, messages: list[Message]) -> AsyncGenerator[str, None]:
        """
        Streaming completion with tool calling support.
        Yields SSE-formatted chunks.
        """
        #TODO:
        # 1. Build request_data: model, messages (each .to_dict()), tools schemas, stream=True
        # 2. Stream via async_openai chat completions; buffer content and tool_deltas per chunk
        # 3. If tool_deltas after stream:
        #    - Collect tool_calls via _collect_tool_calls(), build ai_message, append to messages
        #    - Notify frontend about each tool call (type: "call") and result (type: "result") via SSE
        #    - Recursively yield from self.stream_response(messages), then return
        # 4. If no tool calls: append final assistant message
        # 5. Yield final SSE chunk with finish_reason="stop", then yield "data: [DONE]\n\n"
        raise NotImplementedError()

    def _collect_tool_calls(self, tool_deltas):
        """Convert streaming tool call deltas to complete tool calls"""
        #TODO:
        # 1. Use defaultdict keyed by delta.index; each entry has shape:
        #    {"id": None, "function": {"arguments": "", "name": None}, "type": None}
        # 2. For each delta: accumulate id, function.name, function.arguments (concatenate), type
        # 3. Return list(tool_dict.values())
        raise NotImplementedError()

    async def _call_tools(self, ai_message: Message, messages: list[Message], silent: bool = False):
        """Execute tool calls using MCP client"""
        #TODO:
        # Iterate through tool_calls:
        #   - Extract tool_name and arguments
        #   - If tool found in self.tools:
        #       - Execute tool call
        #       - Append tool message to messages
        #   - If tool not found: append a Tool Message error content and dont forget about tool_call_id
        raise NotImplementedError()

        #TODO 2:
        # Implement it ONLY after you started the app
        # Make PII filtering for tool call result