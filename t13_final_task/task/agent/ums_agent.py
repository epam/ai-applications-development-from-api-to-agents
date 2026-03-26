import json
import logging
from collections import defaultdict
from typing import AsyncGenerator

from openai import AsyncOpenAI

from task.agent.models import Message
from task.agent.models import Role
from task.agent.guardrail import UMSDataGuardrail
from task.agent.tools.base import BaseTool

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
        # 1. Store tools as a dict `{tool.name: tool for tool in tools}` in `self.tools`
        # 2. Store tools schemas list in `self._tools_schemas` using `tool.schema` for each tool
        #    (use an empty list if `tools` is falsy)
        # 3. Store `model` in `self.model`
        # 4. Init `self.async_openai = AsyncOpenAI(api_key=api_key)`
        # 5. Init `self.guardrail = UMSDataGuardrail()`
        raise NotImplementedError()

    async def response(self, messages: list[Message]) -> Message:
        """Non-streaming completion with tool calling support"""
        logger.debug(
            "Creating non-streaming completion",
            extra={"message": messages, "model": self.model}
        )

        #TODO:
        # 1. Build `request_data` dict with keys `model`, `messages` (each converted via `.to_dict()`),
        #    `tools` (use `self._tools_schemas`), and `stream=False`
        # 2. Call `await self.async_openai.chat.completions.create(**request_data)` and store as `response`
        # 3. Build `ai_message = Message(role=Role.ASSISTANT, content=response.choices[0].message.content)`
        # 4. If `response.choices[0].message.tool_calls` is present, assign it to `ai_message.tool_calls`
        # 5. If `ai_message.tool_calls`: append `ai_message` to `messages`, call `await self._call_tools(ai_message, messages)`,
        #    then `return await self.response(messages)` (recursive call)
        # 6. Return `ai_message`
        raise NotImplementedError()

    async def stream_response(self, messages: list[Message]) -> AsyncGenerator[str, None]:
        """
        Streaming completion with tool calling support.
        Yields SSE-formatted chunks.
        """
        logger.debug(
            "Creating streaming completion",
            extra={"message_count": len(messages), "model": self.model}
        )

        #TODO:
        # 1. Build `request_data` the same way as in `response()` but with `stream=True`
        # 2. Create the stream via `await self.async_openai.chat.completions.create(**request_data)`
        # 3. Init `content_buffer = ""` and `tool_deltas = []`
        # 4. Iterate `async for chunk in stream`; for each get `delta = chunk.choices[0].delta`:
        #    - If `delta.content`: yield an SSE chunk in this shape and append content to `content_buffer`:
        #      ```
        #      {"choices": [{"delta": {"content": delta.content}, "index": 0, "finish_reason": None}]}
        #      ```
        #    - If `delta.tool_calls`: extend `tool_deltas` with them
        # 5. If `tool_deltas` after the loop:
        #    a. Collect full tool calls via `self._collect_tool_calls(tool_deltas)`
        #    b. Build `ai_message = Message(role=Role.ASSISTANT, content=content_buffer, tool_calls=tool_calls)`
        #       and append to `messages`
        #    c. For each tool_call: parse `tool_args` from `tool_call["function"]["arguments"]` with `json.loads`
        #       (default to `{}` on error), then yield a tool-call SSE event:
        #       ```
        #       {"tool_activity": {"type": "call", "name": tool_name, "arguments": tool_args}}
        #       ```
        #    d. Record `prev_len = len(messages)`, then `await self._call_tools(ai_message, messages)`
        #    e. For each new message in `messages[prev_len:]`, yield a tool-result SSE event:
        #       ```
        #       {"tool_activity": {"type": "result", "name": name, "content": msg.content}}
        #       ```
        #    f. Recursively `async for chunk in self.stream_response(messages): yield chunk`, then `return`
        # 6. If no tool calls: append `Message(role=Role.ASSISTANT, content=content_buffer)` to `messages`
        # 7. Yield the final SSE chunk and the done signal:
        #    ```
        #    {"choices": [{"delta": {}, "index": 0, "finish_reason": "stop"}]}
        #    ```
        #    then `yield "data: [DONE]\n\n"`

    def _collect_tool_calls(self, tool_deltas):
        """Convert streaming tool call deltas to complete tool calls"""
        #TODO:
        # 1. Create a `defaultdict` keyed by `delta.index`; each default value is:
        #    `{"id": None, "function": {"arguments": "", "name": None}, "type": None}`
        # 2. Iterate `tool_deltas`; for each delta use `delta.index` as the key and:
        #    - Set `id` if `delta.id` is present
        #    - Set `function.name` if `delta.function.name` is present
        #    - Concatenate `delta.function.arguments` onto `function.arguments` if present
        #    - Set `type` if `delta.type` is present
        # 3. Return `list(tool_dict.values())`
        raise NotImplementedError()

    async def _call_tools(self, ai_message: Message, messages: list[Message], silent: bool = False):
        """Execute tool calls using MCP client"""
        #TODO:
        # For each `tool_call` in `ai_message.tool_calls`:
        # 1. Extract `tool_name = tool_call["function"]["name"]`
        # 2. Parse `arguments = json.loads(tool_call["function"]["arguments"])`
        # 3. If the tool is found in `self.tools`:
        #    - Execute tool call
        #    - Append result to `messages`
        # 4. If the tool is NOT found: append a `Message(role=Role.TOOL, content="Error: ...", tool_call_id=tool_call["id"])`
        #    to `messages` describing that the tool was not found
        raise NotImplementedError()

        #TODO 2:
        # Implement it ONLY after you started the app
        # Make PII filtering for tool call result with `guardrail.redact(result)`
