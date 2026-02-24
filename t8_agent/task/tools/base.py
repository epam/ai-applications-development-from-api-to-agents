from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    """Abstract base class for all agent tools.

    A tool is a callable capability the agent can invoke during its reasoning
    loop. Subclasses define what the tool does (``execute``), how it identifies
    itself to the model (``name``, ``description``), and what arguments it
    accepts (``input_schema``). The two schema properties then assemble that
    information into the format expected by each provider.
    """

    @abstractmethod
    def execute(self, arguments: dict[str, Any]) -> str:
        """Run the tool with the given arguments and return the result as a string.

        The agent calls this method when the model requests the tool. The
        returned string is sent back to the model as the tool result.

        Args:
            arguments: Key-value pairs matching the fields declared in
                ``input_schema``. The values are already parsed — no JSON
                decoding is needed inside this method.

        Returns:
            A human- and model-readable string describing the outcome.
            Return an informative error message rather than raising, so the
            model can react gracefully.
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier for this tool.

        Used as the function name in the tool schema sent to the model and as
        the key for tool lookup when the model requests a call.
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Short, clear description of what the tool does.

        The model uses this text to decide when to call the tool, so it should
        be specific enough to distinguish this tool from others without being
        overly verbose.
        """
        pass

    @property
    @abstractmethod
    def input_schema(self) -> dict[str, Any]:
        """JSON Schema object describing the tool's input parameters.

        Must follow the JSON Schema draft-07 ``object`` format::

            {
                "type": "object",
                "properties": {
                    "param": {"type": "string", "description": "..."}
                },
                "required": ["param"]
            }

        This schema is embedded verbatim into both ``openai_schema`` (as
        ``parameters``) and ``anthropic_schema`` (as ``input_schema``).
        """
        pass

    @property
    def openai_schema(self) -> dict[str, Any]:
        """Tool schema formatted for the OpenAI Chat Completions API.

        Wraps ``name``, ``description``, and ``input_schema`` inside the
        ``{"type": "function", "function": {...}}`` envelope that OpenAI
        expects in the ``tools`` array.
        https://developers.openai.com/api/docs/guides/function-calling#defining-functions
        """
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
        """Tool schema formatted for the Anthropic Messages API.

        Returns a flat dict with ``name``, ``description``, and
        ``input_schema`` — the structure Anthropic expects directly in the
        ``tools`` array (no ``"type": "function"`` wrapper).
        https://platform.claude.com/docs/en/api/messages/create#create.tools
        """
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema
        }
