import json

from openai import OpenAI

from commons.models.message import Message
from commons.models.role import Role
from t12_skills.custom.tools.base import BaseTool


class T12Agent:

    def __init__(self, client: OpenAI, model: str, tools: list[BaseTool] | None = None):
        self._client = client
        self._model = model
        self._tools: dict[str, BaseTool] = {tool.name: tool for tool in tools}
        self._tools_schemas = [tool.schema for tool in tools] if tools else []
        print(json.dumps(self._tools_schemas, indent=4))

    async def chat_completion(self, messages: list[Message], log_messages: bool = False) -> Message:
        #TODO:
        # 1. If `log_messages`, print "\n--- REQUEST ---" and `json.dumps([msg.to_dict() for msg in messages], indent=2, default=str)`
        # 2. Return `await self._chat_completion(messages, log_messages)`
        raise NotImplementedError()

    async def _chat_completion(self, messages: list[Message], log_messages: bool = False) -> Message:
        #TODO:
        # 1. Build `request = {"model": self._model, "messages": [msg.to_dict() for msg in messages], "tools": self._tools_schemas}`
        # 2. Call `self._client.chat.completions.create(**request)`, assign to `response`
        # 3. Get `choice = response.choices[0]`
        # 4. Create `assistant_msg = Message(role=Role.ASSISTANT, content="")`
        # 5. If `choice.message.content`, assign it to `assistant_msg.content`
        # 6. If `choice.message.tool_calls`, build and assign `assistant_msg.tool_calls` as list of dicts:
        #    [{"id": tc.id, "type": tc.type, "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
        #     for tc in choice.message.tool_calls]
        # 7. If `choice.finish_reason == "tool_calls"`:
        #       a. Append `assistant_msg` to `messages`
        #       b. Call `await self._dispatch_tool_calls(choice.message.tool_calls)`, assign to `tool_messages`
        #       c. Extend `messages` with `tool_messages`
        #       d. If `log_messages`, print `json.dumps(assistant_msg.to_dict(), ...)` and
        #          `json.dumps([tool_msg.to_dict() for tool_msg in tool_messages], ...)`
        #       e. Return `await self._chat_completion(messages, log_messages)`
        # 8. If `log_messages`, print "---------------\n"
        # 9. Print f"🤖: {assistant_msg.content}"
        # 10. Return `assistant_msg`
        raise NotImplementedError()

    async def _dispatch_tool_calls(self, tool_calls) -> list[Message]:
        #TODO:
        # 1. Initialize `tool_messages: list[Message] = []`
        # 2. For each `tc` in `tool_calls`:
        #       a. Get `tool = self._tools.get(tc.function.name)`
        #       b. If tool is None, set `content = f"ERROR: unknown tool '{tc.function.name}'"`
        #       c. Else call `await tool.execute(tc.id, json.loads(tc.function.arguments))`,
        #          assign to `result_msg`, set `content = result_msg.content`
        #       d. Append `Message(role=Role.TOOL, tool_call_id=tc.id, name=tc.function.name, content=content)`
        #          to `tool_messages`
        # 3. Return `tool_messages`
        raise NotImplementedError()
