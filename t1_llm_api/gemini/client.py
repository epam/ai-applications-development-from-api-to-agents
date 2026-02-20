from google import genai
from google.genai import types

from commons.models.message import Message
from commons.models.role import Role
from t1_llm_api.base_client import AIClient


class GeminiAIClient(AIClient):
    """
    Client for Google Gemini API using the official SDK.

    This implementation uses the official Google GenAI Python library to interact
    with Gemini models, providing both synchronous and streaming response capabilities.

    Attributes:
        _client (genai.Client): Google GenAI client instance.
        Inherits all other attributes from AIClient.
    """

    def __init__(self, endpoint: str, model_name: str, api_key: str, system_prompt: str):
        """
        Initialize the Gemini client with SDK.

        Args:
            endpoint (str): The Gemini API endpoint (for compatibility, not used by SDK).
            model_name (str): The Gemini model to use (e.g., 'gemini-3-flash-preview').
            api_key (str): The Google API key for authentication.
            system_prompt (str): The system instruction to guide the model's behavior.
        """
        #TODO:
        # https://ai.google.dev/gemini-api/docs/text-generation#python_4
        # 1. Call to __init__ of super class
        # 2. Add self._client = genai.Client(api_key=api_key)
        raise NotImplementedError

    def _to_gemini_contents(self, messages: list[Message]) -> list[types.Content]:
        """
        Convert Message objects to Gemini Content format.

        Gemini uses a different role naming convention where AI messages use
        the role "model" instead of "assistant".

        Args:
            messages (list[Message]): The conversation messages to convert.

        Returns:
            list[types.Content]: Messages in Gemini's Content format.
        """
        contents = []
        for msg in messages:
            role = msg.role
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part(text=msg.content)]
                )
            )
        return contents

    def response(self, messages: list[Message], **kwargs) -> Message:
        """
        Get a synchronous response from Google's Gemini API.

        Args:
            messages (list[Message]): The conversation history.
            **kwargs: Additional parameters like max_tokens (default: 1024).

        Returns:
            Message: The AI's response message.

        Note:
            Gemini uses 'system_instruction' parameter for system-level guidance.
            The response is printed to stdout before being returned.
        """
        #TODO:
        # https://ai.google.dev/gemini-api/docs/text-generation#python_4
        # 0. Make a request in Postman to see the request and response
        # 1. Call client, use `self._client.models.generate_content` with such params:
        #   - model=self._model_name
        #   - contents=self._to_gemini_contents(messages)
        #   - config=types.GenerateContentConfig(
        #       system_instruction=self._system_prompt,
        #       max_output_tokens=kwargs.get("max_tokens", 1024),
        #     )
        # 2. Get content from response: `content = response.text`
        # 3. Print content to console
        # 4. Return ASSISTANT message (role assistant, content is generated content)
        raise NotImplementedError

    async def stream_response(self, messages: list[Message], **kwargs) -> Message:
        """
        Get a streaming response from Google's Gemini API.

        The response is streamed chunk-by-chunk, with each text chunk printed
        immediately as it arrives.

        Args:
            messages (list[Message]): The conversation history.
            **kwargs: Additional parameters like max_tokens (default: 1024).

        Returns:
            Message: The complete AI response message after all chunks are received.

        Note:
            Uses the async streaming interface provided by the Gemini SDK.
            Each chunk's text is printed to stdout as it arrives.
        """
        #TODO:
        # https://ai.google.dev/gemini-api/docs/text-generation#python_4
        # 0. Make a request in Postman to see the request and response
        # 1. Initialize empty content list to collect streamed chunks
        # 2. Call client, use `await self._client.aio.models.generate_content_stream` with such params:
        #   - model=self._model_name
        #   - contents=self._to_gemini_contents(messages)
        #   - config=types.GenerateContentConfig(
        #       system_instruction=self._system_prompt,
        #       max_output_tokens=kwargs.get("max_tokens", 1024),
        #     )
        # 3. Iterate through chunks in generated stream (async for chunk in await ...):
        #   - if chunk.text is not empty:
        #       - append chunk.text to content list
        #       - print chunk text to console `print(chunk.text, end='')`
        # 4. Print empty row
        # 5. Return ASSISTANT message (role assistant, content is joined content list)
        raise NotImplementedError