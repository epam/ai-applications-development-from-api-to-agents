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
        # https://github.com/openai/openai-python?tab=readme-ov-file#usage
        # 1. Call to __init__ of super class
        # 2. Initialize OpenAI client: `self._client = OpenAI(api_key=api_key)`
        # 3. Initialize AsyncOpenAI client: `self._async_client = AsyncOpenAI(api_key=api_key)`
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
        # https://developers.openai.com/api/docs/guides/text?lang=python
        # 0. Make a request in Postman to see the request and response
        # 1. Prepare input messages list: `input_messages = [message.to_dict() for message in messages]`
        # 2. Create response using OpenAI client:
        #   - call `self._client.responses.create()` with:
        #     - model=self._model_name
        #     - instructions=self._system_prompt
        #     - input=input_messages
        # 3. Extract content from response: `content = response.output_text`
        # 4. Print content
        # 5. Return ASSISTANT message
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
        # https://developers.openai.com/api/docs/guides/text?lang=python
        # 0. Make a request in Postman to see the request and response
        # 1. Prepare input messages list: `input_messages = [message.to_dict() for message in messages]`
        # 2. Initialize empty contents list to collect streamed chunks
        # 3. Create streaming response using AsyncOpenAI client:
        #   - use `async with self._async_client.responses.stream()` with:
        #     - model=self._model_name
        #     - instructions=self._system_prompt
        #     - input=input_messages
        # 4. Iterate through stream events using `async for event in stream:`
        # 5. For each event, check if event type is "response.output_text.delta":
        #   - append event.delta to contents list
        #   - print event.delta without newline (end='')
        # 6. Print empty line (for formatting)
        # 7. Return ASSISTANT message with joined contents: `Message(role=Role.ASSISTANT, content="".join(contents))`
        raise NotImplementedError