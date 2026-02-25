import json
from typing import Any

import requests

from commons.constants import ANTHROPIC_ENDPOINT
from commons.models.message import Message
from commons.models.role import Role
from t8_agent.task.agents._base import BaseAgent
from t8_agent.task.tools.base import BaseTool


class AnthropicBasedAgent(BaseAgent):

    def __init__(self, model: str, api_key: str, tools: list[BaseTool] | None = None, system_prompt: str | None = None):
        super().__init__(model, api_key, tools, system_prompt)
        self._endpoint = ANTHROPIC_ENDPOINT
        self._tools_schemas = [tool.anthropic_schema for tool in tools] if tools else []

        print(self._endpoint)
        print(json.dumps(self._tools_schemas, indent=4))

    def get_response(self, messages: list[Message], print_request: bool = True) -> Message:
        headers = {
            "x-api-key": self._api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        anthropic_messages = self._to_anthropic_messages(messages)

        request_data = {
            "model": self._model,
            "max_tokens": 8096,
            "messages": anthropic_messages,
            "tools": self._tools_schemas,
        }
        if self._system_prompt:
            request_data["system"] = self._system_prompt

        if print_request:
            print(self._endpoint)
            print("REQUEST:", json.dumps({"messages": anthropic_messages}, indent=2))

        response = requests.post(url=self._endpoint, headers=headers, json=request_data)

        if response.status_code == 200:
            data = response.json()

            content_blocks = data.get("content", [])
            stop_reason = data.get("stop_reason")
            print("RESPONSE:", json.dumps(data, indent=2))
            print("-" * 100)

            text_content = next((b["text"] for b in content_blocks if b["type"] == "text"), None)
            tool_use_blocks = [b for b in content_blocks if b["type"] == "tool_use"]

            ai_response = Message(
                role=Role.ASSISTANT,
                content=text_content,
                tool_calls=content_blocks if tool_use_blocks else None,
            )

            if stop_reason == "tool_use":
                messages.append(ai_response)

                tool_messages = self._process_tool_calls(tool_use_blocks)
                messages.extend(tool_messages)

                return self.get_response(messages, print_request)

            return ai_response
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")

    def _to_anthropic_messages(self, messages: list[Message]) -> list[dict[str, Any]]:
        """Convert internal Message list to Anthropic API message format."""
        result = []
        i = 0
        while i < len(messages):
            msg = messages[i]
            if msg.role == Role.TOOL:
                # Group consecutive tool results into a single user message
                tool_results = []
                while i < len(messages) and messages[i].role == Role.TOOL:
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": messages[i].tool_call_id,
                        "content": messages[i].content,
                    })
                    i += 1
                result.append({"role": "user", "content": tool_results})
            elif msg.role == Role.ASSISTANT:
                content = msg.tool_calls if msg.tool_calls else msg.content
                result.append({"role": "assistant", "content": content})
                i += 1
            else:
                result.append({"role": msg.role.value, "content": msg.content})
                i += 1
        return result

    def _process_tool_calls(self, tool_use_blocks: list[dict[str, Any]]) -> list[Message]:
        """Process tool_use blocks and return tool result messages."""
        tool_messages = []
        for block in tool_use_blocks:
            tool_use_id = block["id"]
            function_name = block["name"]
            arguments = block["input"]

            tool_execution_result = self._call_tool(function_name, arguments)

            tool_messages.append(Message(
                role=Role.TOOL,
                name=function_name,
                tool_call_id=tool_use_id,
                content=tool_execution_result,
            ))

            print(f"FUNCTION '{function_name}'\n{tool_execution_result}\n{'-' * 50}")

        return tool_messages

    def _call_tool(self, function_name: str, arguments: dict[str, Any]) -> str:
        tool = self._tools_dict.get(function_name)
        if tool:
            return tool.execute(arguments)

        return f"Unknown function: {function_name}"
