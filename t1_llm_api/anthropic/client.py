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
        super().__init__(endpoint, model_name, api_key, system_prompt)
        self._client = Anthropic(api_key=api_key)
        self._async_client = AsyncAnthropic(api_key=api_key)

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
        response = self._client.messages.create(
            system=self._system_prompt,
            max_tokens=1024,
            model=self._model_name,
            messages=[msg.to_dict() for msg in messages]
        )

        content = ""
        for block in response.content:
            if block.type == 'text':
                content += block.text

        print(content)
        return Message(role=Role.ASSISTANT, content=content)

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
        content = []

        stream = await self._async_client.messages.create(
            system=self._system_prompt,
            max_tokens=1024,
            model=self._model_name,
            stream=True,
            messages=[msg.to_dict() for msg in messages]
        )

        async for chunk in stream:
            if chunk.type == "content_block_delta":
                if hasattr(chunk, 'delta') and hasattr(chunk.delta, 'text'):
                    delta_content = chunk.delta.text
                    content.append(delta_content)
                    print(delta_content, end='')

        print()
        return Message(role=Role.ASSISTANT, content="".join(content))
