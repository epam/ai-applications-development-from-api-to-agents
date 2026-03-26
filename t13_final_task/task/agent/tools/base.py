from abc import ABC, abstractmethod
from typing import Any


from t13_final_task.task.agent.models import Message

from t13_final_task.task.agent.models import Role


class BaseTool(ABC):

    async def execute(self, tool_call_id: str, arguments: dict[str, Any]) -> Message:
        try:
            content = await self._execute(arguments)
        except Exception as e:
            content = f"ERROR during tool call execution:\n {e}"

        return Message(
            role=Role.TOOL,
            tool_call_id=tool_call_id,
            content=content,
        )

    @abstractmethod
    async def _execute(self, arguments: dict[str, Any]) -> str:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def parameters(self) -> dict[str, Any]:
        pass

    @property
    def schema(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }
