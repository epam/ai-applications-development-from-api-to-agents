from openai import OpenAI, AsyncOpenAI

from t1_llm_api._models.message import Message
from t1_llm_api._models.role import Role
from t1_llm_api.openai.base import BaseOpenAIClient


class OpenAIClient(BaseOpenAIClient):
    """
    Client for OpenAI Chat Completions API using the official SDK.

    This implementation uses the official OpenAI Python library to interact
    with the Chat Completions API, providing both synchronous and streaming
    response capabilities.

    Attributes:
        _client (OpenAI): Synchronous OpenAI client instance.
        _async_client (AsyncOpenAI): Asynchronous OpenAI client instance.
        Inherits all other attributes from BaseOpenAIClient.
    """

    def __init__(self, endpoint: str, model_name: str, system_prompt: str, api_key: str):
        """
        Initialize the OpenAI Chat Completions client with SDK.

        Args:
            endpoint (str): The OpenAI API endpoint (for compatibility, not used by SDK).
            model_name (str): The OpenAI model to use (e.g., 'gpt-5').
            system_prompt (str): The system message to guide the model's behavior.
            api_key (str): The OpenAI API key for authentication.
        """
        #TODO:
        # Call to __init__ of super class
        # Add OpenAI and AsyncOpenAI clients https://github.com/openai/openai-python?tab=readme-ov-file#usage
        # (In readme you can find samples with both of these clients)
        # Useful link with request/response samples https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create
        raise NotImplementedError

    def response(self, messages: list[Message], **kwargs) -> Message:
        """
        Get a synchronous response from OpenAI's Chat Completions API.

        Args:
            messages (list[Message]): The conversation history.
            **kwargs: Additional parameters for the API (currently unused).

        Returns:
            Message: The AI's response message.

        Note:
            The system prompt is automatically prepended to the messages.
            The response is printed to stdout before being returned.
        """
        #TODO:
        # - Prepare message history with System prompt
        # - Call client
        # - Print response to console
        # - Return ASSISTANT message
        raise NotImplementedError

    async def stream_response(self, messages: list[Message], **kwargs) -> Message:
        """
        Get a streaming response from OpenAI's Chat Completions API.

        The response is streamed token-by-token, with each chunk printed
        immediately as it arrives.

        Args:
            messages (list[Message]): The conversation history.
            **kwargs: Additional parameters for the API (currently unused).

        Returns:
            Message: The complete AI response message after all chunks are received.

        Note:
            The system prompt is automatically prepended to the messages.
            Each token is printed to stdout as it arrives for real-time display.
        """
        #TODO:
        # - Prepare message history with System prompt
        # - Call client with streaming mode
        # - Handle stream with chunks
        # - Print response to console
        # - Return ASSISTANT message
        raise NotImplementedError
