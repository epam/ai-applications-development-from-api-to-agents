import json
import aiohttp
import requests

from t1_llm_api._models.message import Message
from t1_llm_api._models.role import Role
from t1_llm_api.base_client import AIClient


class CustomAnthropicAIClient(AIClient):
    """
    Custom HTTP client for Anthropic's Claude API.

    This implementation uses raw HTTP requests (requests/aiohttp) instead of
    the official SDK, demonstrating how to interact with Claude's API directly
    and handle its Server-Sent Events (SSE) streaming format.
    """

    def response(self, messages: list[Message], **kwargs) -> Message:
        """
        Get a synchronous response using raw HTTP POST request.

        Args:
            messages (list[Message]): The conversation history.
            **kwargs: Additional parameters like max_tokens (default: 1024).

        Returns:
            Message: The AI's response message.

        Raises:
            ValueError: If the API response contains no content blocks.
            Exception: If the HTTP request fails (non-200 status code).

        Note:
            Requires 'x-api-key' header and 'anthropic-version' header.
            Claude's API returns content as an array of content blocks.
            The response is printed to stdout before being returned.
        """
        headers = {
            "x-api-key": self._api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        request_data = {
            "model": self._model_name,
            "system": self._system_prompt,
            "max_tokens": kwargs.get("max_tokens", 1024),
            "messages": [message.to_dict() for message in messages]
        }

        response = requests.post(url=self._endpoint, headers=headers, json=request_data)

        if response.status_code == 200:
            data = response.json()
            content_blocks = data.get("content", [])
            if content_blocks:
                content = "".join(block.get("text", "") for block in content_blocks if block.get("type") == "text")
                print(content)
                return Message(Role.ASSISTANT, content)
            raise ValueError("No content blocks present in the response")
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")

    async def stream_response(self, messages: list[Message], **kwargs) -> Message:
        """
        Get a streaming response using raw HTTP with Server-Sent Events (SSE).

        The response is streamed using Anthropic's SSE format, with text deltas
        printed immediately as they arrive.

        Args:
            messages (list[Message]): The conversation history.
            **kwargs: Additional parameters like max_tokens (default: 1024).

        Returns:
            Message: The complete AI response message after all deltas are received.

        Note:
            Uses Server-Sent Events (SSE) format where each line starts with "data: ".
            Listens for 'content_block_delta' events with 'text_delta' type.
            Stops processing when 'message_stop' event is received.
            Each delta is printed to stdout as it arrives.
        """
        headers = {
            "x-api-key": self._api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        request_data = {
            "model": self._model_name,
            "system": self._system_prompt,
            "max_tokens": kwargs.get("max_tokens", 1024),
            "stream": True,
            "messages": [msg.to_dict() for msg in messages]
        }
        contents = []

        async with aiohttp.ClientSession() as session:
            async with session.post(url=self._endpoint, headers=headers, json=request_data) as response:
                if response.status == 200:
                    async for line in response.content:
                        line_str = line.decode('utf-8').strip()
                        if line_str.startswith("data: "):
                            data = line_str[6:].strip()
                            parsed_data = json.loads(data)
                            event_type = parsed_data.get("type")

                            if event_type == "content_block_delta":
                                delta = parsed_data.get("delta", {})
                                if delta.get("type") == "text_delta":
                                    text_content = delta.get("text", "")
                                    if text_content:
                                        print(text_content, end='')
                                        contents.append(text_content)
                            elif event_type == "message_stop":
                                break
                else:
                    error_text = await response.text()
                    print(f"{response.status} {error_text}")

                print()
                return Message(role=Role.ASSISTANT, content=''.join(contents))

