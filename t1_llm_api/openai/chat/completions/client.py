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
        # https://github.com/openai/openai-python?tab=readme-ov-file#usage
        # 1. Call to __init__ of super class
        # 2. Initialize OpenAI client: `self._client = OpenAI(api_key=api_key)`
        # 3. Initialize AsyncOpenAI client: `self._async_client = AsyncOpenAI(api_key=api_key)`
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
        # https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create
        # 0. Make a request in Postman to see the request and response
        # 1. Prepare messages list with system message first:
        #   - create messages_dicts list: [{"role": "system", "content": self._system_prompt}, *[message.to_dict() for message in messages]]
        # 2. Create completion using OpenAI client:
        #   - call `self._client.chat.completions.create()` with:
        #     - model=self._model_name
        #     - messages=messages_dicts
        # 3. Extract content from response: `content = response.choices[0].message.content`
        # 4. Print content
        # 5. Return ASSISTANT message
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
        # https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create
        # 0. Make a request in Postman to see the request and response
        # 1. Prepare messages list with system message first:
        #   - create messages_dicts list: [{"role": "system", "content": self._system_prompt}, *[message.to_dict() for message in messages]]
        # 2. Initialize empty content list to collect streamed chunks
        # 3. Create streaming completion using AsyncOpenAI client:
        #   - call `await self._async_client.chat.completions.create()` with:
        #     - model=self._model_name
        #     - stream=True
        #     - messages=messages_dicts
        # 4. Iterate through stream chunks using `async for chunk in stream:`
        # 5. For each chunk, check if delta content exists using walrus operator:
        #   - `if delta_content := chunk.choices[0].delta.content:`
        #   - append delta_content to content list
        #   - print delta_content without newline (end='')
        # 6. Print empty line (for formatting)
        # 7. Return ASSISTANT message with joined content: `Message(role=Role.ASSISTANT, content="".join(content))`
        raise NotImplementedError
