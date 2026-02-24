from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):

    @abstractmethod
    def execute(self, arguments: dict[str, Any]) -> str:
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
    def input_schema(self) -> dict[str, Any]:
        pass

    @property
    def openai_schema(self) -> dict[str, Any]:
        """Provides tools JSON Schema according to the OpenAI API"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.input_schema
            }
        }

    @property
    def anthropic_schema(self) -> dict[str, Any]:
        """Provides tools JSON Schema according to the Anthropic API"""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema
        }
