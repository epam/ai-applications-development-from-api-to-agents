from anthropic import Anthropic, AsyncAnthropic

from commons.models.message import Message
from commons.models.role import Role
from t1_llm_api.base_client import AIClient


class AnthropicAIClient(AIClient):
    """
    Client for Anthropic's Claude API using the official SDK.

    This implementation uses the official Anthropic Python library to interact
    with Claude models, providing both synchronous and streaming response capabilities.

    Attributes:
        _client (Anthropic): Synchronous Anthropic client instance.
        _async_client (AsyncAnthropic): Asynchronous Anthropic client instance.
        Inherits all other attributes from AIClient.
    """

    def __init__(self, endpoint: str, model_name: str, api_key: str, system_prompt: str):
        """
        Initialize the Anthropic client with SDK.

        Args:
            endpoint (str): The Anthropic API endpoint (for compatibility, not used by SDK).
            model_name (str): The Claude model to use (e.g., 'claude-3-opus', 'claude-sonnet-4-5').
            api_key (str): The Anthropic API key for authentication.
            system_prompt (str): The system instruction to guide Claude's behavior.
        """
        #TODO:
        # 1. Call to __init__ of super class
        # 2. Add self._client = Anthropic(api_key=api_key)
        # 3. Add self._async_client = AsyncAnthropic(api_key=api_key)
        # Add Anthropic and AsyncAnthropic clients https://github.com/anthropics/anthropic-sdk-python (In readme you can find
        # samples with both of these clients)
        raise NotImplementedError

    def response(self, messages: list[Message], **kwargs) -> Message:
        """
        Get a synchronous response from Anthropic's Claude API.

        Args:
            messages (list[Message]): The conversation history.
            **kwargs: Additional parameters like max_tokens (default: 1024).

        Returns:
            Message: The AI's response message.

        Note:
            Claude's API uses a separate 'system' parameter for system instructions.
            Response content blocks are concatenated into a single text response.
            The response is printed to stdout before being returned.
        """
        #TODO:
        # 0. Make a request in Postman to see the request and response
        # 1. Call client, use `self._client.messages.create` with such params:
        #   - system=self._system_prompt
        #   - max_tokens=1024
        #   - model=self._model_name
        #   - messages=[msg.to_dict() for msg in messages]
        # 2. Iterate through response content and if content type is `text` then concat it
        # 3. Print content to console
        # 4. Return ASSISTANT message (role assistant, content is generated content)
        raise NotImplementedError

    async def stream_response(self, messages: list[Message], **kwargs) -> Message:
        """
        Get a streaming response from Anthropic's Claude API.

        The response is streamed using event-based streaming, with text deltas
        printed immediately as they arrive.

        Args:
            messages (list[Message]): The conversation history.
            **kwargs: Additional parameters like max_tokens (default: 1024).

        Returns:
            Message: The complete AI response message after all deltas are received.

        Note:
            Listens for 'content_block_delta' events with text deltas.
            Each delta is printed to stdout as it arrives for real-time display.
        """
        #TODO:
        # 0. Make a request in Postman to see the request and response
        # 1. Call client, use `await self._async_client.messages.create` with such params:
        #   - system=self._system_prompt
        #   - max_tokens=1024
        #   - model=self._model_name
        #   - stream=True
        #   - messages=[msg.to_dict() for msg in messages]
        # 2. Iterate through chunks in generated stream (async for chunk in stream)
        # 2.1. If chunk type is `content_block_delta` then:
        #   - Check if `hasattr(chunk, 'delta') and hasattr(chunk.delta, 'text')` and if yes then:
        #       - get delta text (chunk.delta.text) and assign to `delta_content`
        #       - collect content to array (later we will need to join all the parts into one string with content)
        #       - print chunk content to console `print(delta_content, end='')`
        # 3. Print empty row
        # 4. Return ASSISTANT message (role assistant, content is generated content)
        raise NotImplementedError
