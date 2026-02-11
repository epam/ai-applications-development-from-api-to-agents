"""
Role enumeration for chat messages.

This module defines the different roles that can send messages in a conversation.
"""

from enum import StrEnum


class Role(StrEnum):
    """
    Enumeration of message roles in a conversation.

    Attributes:
        SYSTEM: System-level instructions that guide the AI's behavior.
        USER: Messages from the human user.
        ASSISTANT: Messages from the AI assistant (also called "assistant" in many APIs).
    """
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
