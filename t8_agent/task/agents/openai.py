import json
from typing import Any

import requests

from commons.constants import OPENAI_CHAT_COMPLETIONS_ENDPOINT
from t8_agent.task._models.message import Message
from t8_agent.task._models.role import Role
from t8_agent.task.agents._base import BaseAgent
from t8_agent.task.tools.base import BaseTool


class OpenAIBasedAgent(BaseAgent):

    def __init__(self, model: str, api_key: str, tools: list[BaseTool] | None = None, system_prompt: str | None = None):
        super().__init__(model, api_key, tools, system_prompt)
        #TODO:
        # 1. Format `self._api_key` as a Bearer token: `f"Bearer {api_key}"`
        # 2. Build `self._tools_schemas` using `tool.openai_schema` for each tool in `tools`
        # 3. Set `self._endpoint` to `OPENAI_CHAT_COMPLETIONS_ENDPOINT`
        # 4. Print `self._endpoint` and `self._tools_schemas` (use json.dumps with indent=4)
        raise NotImplementedError()

    def get_response(self, messages: list[Message], print_request: bool = True) -> Message:
        #TODO:
        # 1. Build `request_messages`: if `self._system_prompt` is set, prepend a
        #    Message(role=Role.SYSTEM, content=self._system_prompt) to `messages` —
        #    do NOT store it in `messages` itself (local to this API call only)
        # 2. Build headers: `Authorization: self._api_key`, `Content-Type: application/json`
        # 3. Build request_data with `model`, serialized `request_messages` (.to_dict()), and `tools`
        # 4. If `print_request` — print `self._endpoint` and the REQUEST payload
        # 5. POST to `self._endpoint` with headers and json body
        # 6. On HTTP 200:
        #    a. Get `choices[0]`, print RESPONSE
        #    b. Extract `content` and `tool_calls` from `choices[0]["message"]`
        #    c. Build `ai_response` as Message(role=Role.AI, content=..., tool_calls=...)
        #    d. If `finish_reason == "tool_calls"`:
        #       - Append `ai_response` to `messages`
        #       - Call `_process_tool_calls(tool_calls)` and extend `messages` with the result
        #       - Recurse: return `self.get_response(messages, print_request)`
        #    e. Otherwise return `ai_response`
        # 7. On error — raise Exception with status code and response text
        raise NotImplementedError()

    def _process_tool_calls(self, tool_calls: list[dict[str, Any]]) -> list[Message]:
        #TODO:
        # For each tool_call in tool_calls:
        # 1. Extract `tool_call_id` from tool_call["id"]
        # 2. Extract `function_name` from tool_call["function"]["name"]
        # 3. Parse `arguments` with `json.loads(tool_call["function"]["arguments"])`
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