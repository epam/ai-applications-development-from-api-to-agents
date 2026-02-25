from dataclasses import dataclass
from typing import Any

from commons.models.role import Role


@dataclass
class Message:
    role: Role
    content: str
    tool_call_id: str | None = None
    name: str| None = None
    tool_calls: list[dict[str, Any]] | None = None

    def to_dict(self) -> dict[str, Any]:
        result = {
            "role": self.role.value,
            "content": self.content
        }
        if self.tool_call_id:
            result["tool_call_id"] = self.tool_call_id
        if self.name:
            result["name"] = self.name
        if self.tool_calls:
            result["tool_calls"] = self.tool_calls
        return result