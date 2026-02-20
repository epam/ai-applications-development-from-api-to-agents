from dataclasses import dataclass

from commons.models.role import Role


@dataclass
class Message:
    role: Role
    content: str

    def to_dict(self) -> dict[str, str]:
        return {
            "role": self.role.value,
            "content": self.content
        }