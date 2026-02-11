import uuid
from dataclasses import dataclass, field

from t1_llm_api._models.message import Message


@dataclass
class Conversation:
    """
    Represents a conversation with message history.

    Each conversation has a unique identifier and maintains a list of messages
    in chronological order.

    Attributes:
        id (str): Unique identifier for the conversation, auto-generated as UUID4.
        messages (list[Message]): Chronological list of messages in the conversation.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    messages: list[Message] = field(default_factory=list)

    def add_message(self, message: Message) -> None:
        """
        Add a new message to the conversation history.

        Args:
            message (Message): The message to append to the conversation.
        """
        self.messages.append(message)

    def get_messages(self) -> list[Message]:
        """
        Retrieve all messages in the conversation.

        Returns:
            list[Message]: The complete list of messages in chronological order.
        """
        return self.messages
    