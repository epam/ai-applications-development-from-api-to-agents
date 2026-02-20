from abc import ABC, abstractmethod

from commons.models.message import Message


class AIClient(ABC):
    """
    Abstract base class for AI service clients.

    This class defines the interface that all AI service implementations must follow.
    It handles common initialization logic and requires concrete implementations for
    both synchronous and asynchronous response methods.

    Attributes:
        _api_key (str): The API key for authenticating with the AI service.
        _endpoint (str): The base URL endpoint for the AI service API.
        _model_name (str): The name/identifier of the AI model to use.
        _system_prompt (str): The system prompt that guides the AI's behavior.
    """

    def __init__(self, endpoint: str, model_name: str, api_key: str, system_prompt: str):
        """
        Initialize the AI client with required configuration.

        Args:
            endpoint (str): The API endpoint URL for the AI service.
            model_name (str): The specific model identifier to use.
            api_key (str): The API key for authentication.
            system_prompt (str): The system-level instruction for the AI model.

        Raises:
            ValueError: If api_key is None, empty, or contains only whitespace.
        """
        if not api_key or api_key.strip() == "":
            raise ValueError("API key cannot be null or empty")

        self._api_key = api_key
        self._endpoint = endpoint
        self._model_name = model_name
        self._system_prompt = system_prompt

    @abstractmethod
    def response(self, messages: list[Message], **kwargs) -> Message:
        """
        Send synchronous request to AI API and return AI response.

        Args:
            messages (list[Message]): The conversation history to send to the AI.
            **kwargs: Additional provider-specific parameters.

        Returns:
            Message: The AI's response as a Message object with role AI.

        Raises:
            NotImplementedError: This is an abstract method that must be implemented by subclasses.
        """
        ...

    @abstractmethod
    async def stream_response(self, messages: list[Message], **kwargs) -> Message:
        """
        Send asynchronous streaming request to AI API and return AI response.

        This method streams the response token-by-token, printing each chunk
        as it arrives before returning the complete message.

        Args:
            messages (list[Message]): The conversation history to send to the AI.
            **kwargs: Additional provider-specific parameters.

        Returns:
            Message: The complete AI response as a Message object with role AI.

        Raises:
            NotImplementedError: This is an abstract method that must be implemented by subclasses.
        """
        ...