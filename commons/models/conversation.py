import uuid
from dataclasses import dataclass, field

from commons.models.message import Message


@dataclass
class Conversation:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    messages: list[Message] = field(default_factory=list)

    def add_message(self, message: Message) -> None:
        self.messages.append(message)

    def get_messages(self) -> list[Message]:
        return self.messages
    