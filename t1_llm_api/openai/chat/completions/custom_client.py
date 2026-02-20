import json
import aiohttp
import requests

from commons.models.message import Message
from commons.models.role import Role
from t1_llm_api.openai.base import BaseOpenAIClient


class CustomOpenAIClient(BaseOpenAIClient):
    """
    Custom HTTP client for OpenAI Chat Completions API.

    This implementation uses raw HTTP requests (requests/aiohttp) instead of
    the official SDK, providing more control over the HTTP layer and demonstrating
    how to interact with the API directly.
    """

    def response(self, messages: list[Message], **kwargs) -> Message:
        """
        Get a synchronous response using raw HTTP POST request.

        Args:
            messages (list[Message]): The conversation history.
            **kwargs: Additional parameters for the API (currently unused).

        Returns:
            Message: The AI's response message.

        Raises:
            ValueError: If the API response contains no choices.
            Exception: If the HTTP request fails (non-200 status code).

        Note:
            The system prompt is automatically prepended to the messages.
            The response is printed to stdout before being returned.
        """
        headers = {
            "Authorization": self._api_key,
            "Content-Type": "application/json"
        }

        messages_dicts = [
            {"role": "system", "content": self._system_prompt},
            *[message.to_dict() for message in messages]
        ]

        request_data = {
            "model": self._model_name,
            "messages": messages_dicts
        }

        response = requests.post(url=self._endpoint, headers=headers, json=request_data)

        if response.status_code == 200:
            data = response.json()
            choices = data.get("choices", [])
            if choices:
                content = choices[0].get("message", {}).get("content")
                print(content)
                return Message(Role.ASSISTANT, content)
            raise ValueError("No Choice has been present in the response")
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")

    async def stream_response(self, messages: list[Message], **kwargs) -> Message:
        """
        Get a streaming response using raw HTTP with Server-Sent Events (SSE).

        The response is streamed token-by-token using OpenAI's SSE format,
        with each chunk printed immediately as it arrives.

        Args:
            messages (list[Message]): The conversation history.
            **kwargs: Additional parameters for the API (currently unused).

        Returns:
            Message: The complete AI response message after all chunks are received.

        Note:
            The system prompt is automatically prepended to the messages.
            Each token is printed to stdout as it arrives.
            Uses Server-Sent Events (SSE) format where each line starts with "data: ".
        """
        headers = {
            "Authorization": self._api_key,
            "Content-Type": "application/json"
        }
        messages_dicts = [
            {"role": "system", "content": self._system_prompt},
            *[message.to_dict() for message in messages]
        ]
        request_data = {
            "model": self._model_name,
            "stream": True,
            "messages": messages_dicts
        }
        contents = []

        async with aiohttp.ClientSession() as session:
            async with session.post(url=self._endpoint, headers=headers, json=request_data) as response:
                if response.status == 200:
                    async for line in response.content:
                        line_str = line.decode('utf-8').strip()
                        if line_str.startswith("data: "):
                            data = line_str[6:].strip()
                            if data != "[DONE]":
                                content_snippet = self._get_content_snippet(data)
                                print(content_snippet, end='')
                                contents.append(content_snippet)
                            else:
                                print()
                else:
                    error_text = await response.text()
                    print(f"{response.status} {error_text}")
                return Message(role=Role.ASSISTANT, content=''.join(contents))

    def _get_content_snippet(self, data: str) -> str:
        """
        Extract content from a streaming data chunk.

        Parses the JSON data from an SSE chunk and extracts the content delta.

        Args:
            data (str): The JSON string from the SSE data field.

        Returns:
            str: The content text from the chunk, or empty string if no content.
        """
        data = json.loads(data)
        if choices := data.get("choices"):
            delta = choices[0].get("delta", {})
            return delta.get("content", '')
        return ''
