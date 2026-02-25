from abc import ABC, abstractmethod

from commons.models.message import Message
from t8_agent.task.tools.base import BaseTool


class BaseAgent(ABC):
    """Abstract base class for LLM-backed agents.

    Subclasses implement provider-specific HTTP communication while sharing
    common state: model name, credentials, optional system prompt, and a
    registry of callable tools.
    """

    def __init__(self, model: str, api_key: str, tools: list[BaseTool] | None = None, system_prompt: str | None = None):
        """Initialise the agent.

        Args:
            model: Provider-specific model identifier (e.g. 'gpt-5.2', 'claude-sonnet-4.5').
            api_key: Secret key used to authenticate with the LLM provider.
            tools: Optional list of tools the agent may call. Each tool is
                indexed by its ``name`` for fast lookup during execution.
            system_prompt: Optional instruction passed to the model before the
                conversation. How it is forwarded depends on the provider
                (e.g. prepended as a system message for OpenAI, or sent as a
                top-level ``system`` field for Anthropic).

        Raises:
            ValueError: If ``api_key`` is empty or blank.
        """
        #TODO:
        # 1. Validate `api_key` — raise ValueError("API key cannot be null or empty") if it is None or blank
        # 2. Store model, api_key, system_prompt as instance attributes (use _model, _api_key, _system_prompt)
        # 3. Build self._tools_dict: dict[str, BaseTool] mapping each tool's name → tool object
        raise NotImplementedError()

    @abstractmethod
    def get_response(self, messages: list[Message], print_request: bool = True) -> Message:
        """Send the conversation to the LLM and return its reply.

        Tool calls are handled transparently: if the model requests one or more
        tools, the agent executes them and recurses until the model returns a
        plain text response.

        Args:
            messages: Ordered conversation history (excluding the system
                prompt, which is managed by the agent itself).
            print_request: When ``True``, log the outgoing request and
                incoming response to stdout for debugging.

        Returns:
            The final assistant ``Message`` after all tool rounds are complete.
        """
        ...

