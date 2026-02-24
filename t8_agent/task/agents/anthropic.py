import json
from typing import Any

import requests

from commons.constants import ANTHROPIC_ENDPOINT
from t8_agent.task._models.message import Message
from t8_agent.task._models.role import Role
from t8_agent.task.agents._base import BaseAgent
from t8_agent.task.tools.base import BaseTool


class AnthropicBasedAgent(BaseAgent):

    def __init__(self, model: str, api_key: str, tools: list[BaseTool] | None = None, system_prompt: str | None = None):
        super().__init__(model, api_key, tools, system_prompt)
        #TODO:
        # 1. Set `self._endpoint` to `ANTHROPIC_ENDPOINT`
        # 2. Build `self._tools_schemas` using `tool.anthropic_schema` for each tool in `tools`
        #    Note: Anthropic uses a flat schema format — see `BaseTool.anthropic_schema`
        # 3. Print `self._endpoint` and `self._tools_schemas` (use json.dumps with indent=4)
        raise NotImplementedError()

    def get_response(self, messages: list[Message], print_request: bool = True) -> Message:
        #TODO:
        # 1. Build headers: `x-api-key: self._api_key`, `anthropic-version: 2023-06-01`,
        #    `Content-Type: application/json`
        # 2. Convert messages to Anthropic format using `_to_anthropic_messages(messages)`
        # 3. Build request_data: model, max_tokens=8096, messages, tools
        # 4. If `self._system_prompt` is set — add `"system": self._system_prompt` to request_data
        # 5. If `print_request` — print `self._endpoint` and the REQUEST payload
        # 6. POST to `self._endpoint` with headers and json body
        # 7. On HTTP 200:
        #    a. Get `content` blocks and `stop_reason`, print RESPONSE
        #    b. Extract text: first block where type == "text" (use next() with default None)
        #    c. Extract tool_use blocks: filter blocks where type == "tool_use"
        #    d. Build `ai_response` as Message(role=Role.AI, content=text,
        #       tool_calls=content_blocks if tool_use_blocks else None)
        #    e. If `stop_reason == "tool_use"`:
        #       - Append `ai_response` to `messages`
        #       - Call `_process_tool_calls(tool_use_blocks)` and extend `messages`
        #       - Recurse: return `self.get_response(messages, print_request)`
        #    f. Otherwise return `ai_response`
        # 8. On error — raise Exception with status code and response text
        raise NotImplementedError()

    def _to_anthropic_messages(self, messages: list[Message]) -> list[dict[str, Any]]:
        #TODO: Convert internal Message list to Anthropic API format.
        # Walk the list with an index `i` (while loop):
        # - Role.TOOL: group consecutive TOOL messages into one user message:
        #   {"role": "user", "content": [{"type": "tool_result", "tool_use_id": ..., "content": ...}, ...]}
        # - Role.AI: if msg.tool_calls is set use it as content (replays the full content blocks
        #   so Anthropic can correlate tool results), otherwise use msg.content as content
        # - Other roles: {"role": msg.role.value, "content": msg.content}
        # Return the resulting list
        raise NotImplementedError()

    def _process_tool_calls(self, tool_use_blocks: list[dict[str, Any]]) -> list[Message]:
        #TODO:
        # For each block in tool_use_blocks:
        # 1. Extract `tool_use_id` from block["id"]
        # 2. Extract `function_name` from block["name"]
        # 3. Get `arguments` from block["input"] — it is already a dict, no json.loads needed
        # 4. Call `_call_tool(function_name, arguments)` and store the result
        # 5. Append Message(role=Role.TOOL, name=function_name, tool_call_id=..., content=result)
        # 6. Print the function name and result
        # Return the list of tool messages
        raise NotImplementedError()

    def _call_tool(self, function_name: str, arguments: dict[str, Any]) -> str:
        #TODO:
        # 1. Look up the tool by `function_name` in `self._tools_dict`
        # 2. If found — call `tool.execute(arguments)` and return the result
        # 3. If not found — return `f"Unknown function: {function_name}"`
        raise NotImplementedError()