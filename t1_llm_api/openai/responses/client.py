from openai import OpenAI, AsyncOpenAI

from t1_llm_api._models.message import Message
from t1_llm_api._models.role import Role
from t1_llm_api.openai.base import BaseOpenAIClient


class OpenAIResponsesClient(BaseOpenAIClient):
    """
    Client for OpenAI Responses API using the official SDK.

    This implementation uses the official OpenAI Python library to interact
    with the Responses API, which uses 'instructions' instead of system messages
    and 'input' instead of messages.

    Attributes:
        _client (OpenAI): Synchronous OpenAI client instance.
        _async_client (AsyncOpenAI): Asynchronous OpenAI client instance.
        Inherits all other attributes from BaseOpenAIClient.
    """

    def __init__(self, endpoint: str, model_name: str, system_prompt: str, api_key: str):
        """
        Initialize the OpenAI Responses client with SDK.

        Args:
            endpoint (str): The OpenAI API endpoint (for compatibility, not used by SDK).
            model_name (str): The OpenAI model to use (e.g., 'gpt-5').
            system_prompt (str): The instruction to guide the model's behavior.
            api_key (str): The OpenAI API key for authentication.
        """
        #TODO:
        # Call to __init__ of super class
        # Add OpenAI and AsyncOpenAI clients https://github.com/openai/openai-python?tab=readme-ov-file#usage
        # (In readme you can find samples with both of these clients)
        raise NotImplementedError

    def response(self, messages: list[Message], **kwargs) -> Message:
        """
        Get a synchronous response from OpenAI's Responses API.

        Args:
            messages (list[Message]): The conversation history.
            **kwargs: Additional parameters for the API (currently unused).

        Returns:
            Message: The AI's response message.

        Note:
            Uses the Responses API format with 'instructions' and 'input' parameters.
            The response is printed to stdout before being returned.
        """
        #TODO:
        # - Prepare input messages
        # - Call client
        # - Print response to console
        # - Return ASSISTANT message
        raise NotImplementedError

    async def stream_response(self, messages: list[Message], **kwargs) -> Message:
        """
        Get a streaming response from OpenAI's Responses API.

        The response is streamed using event-based streaming, with each delta
        printed immediately as it arrives.

        Args:
            messages (list[Message]): The conversation history.
            **kwargs: Additional parameters for the API (currently unused).

        Returns:
            Message: The complete AI response message after all deltas are received.

        Note:
            Uses the Responses API streaming format with event types.
            Listens for 'response.output_text.delta' events to build the response.
        """
        #TODO:
        # - Prepare input messages
        # - Call client with streaming mode
        # - Handle stream with events
        # - Print response to console
        # - Return ASSISTANT message
        raise NotImplementedError