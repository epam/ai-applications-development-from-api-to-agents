from dataclasses import dataclass

from t1_llm_api._models.role import Role


@dataclass
class Message:
    """
    Represents a single message in a conversation.

    A message consists of a role (who sent it) and content (what was said).

    Attributes:
        role (Role): The role of the message sender (SYSTEM, USER, or ASSISTANT).
        content (str): The text content of the message.
    """
    role: Role
    content: str

    def to_dict(self) -> dict[str, str]:
        """
        Convert the message to a dictionary format for API requests.

        Returns:
            dict[str, str]: A dictionary with 'role' and 'content' keys,
                          where role is converted to its string value.

        Example:
            {'role': 'user', 'content': 'Hello!'}
        """
        return {
            "role": self.role.value,
            "content": self.content
        }