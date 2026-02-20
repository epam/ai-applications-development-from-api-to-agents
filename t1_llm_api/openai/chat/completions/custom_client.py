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
        #TODO:
        # https://platform.openai.com/docs/api-reference/chat
        # 0. Make a request in Postman to see the request and response
        # 1. Prepare headers dict with:
        #   - "Authorization" (self api key)
        #   - "Content-Type" ("application/json")
        # 2. Prepare messages list:
        #   - create messages_dicts list with system message first:
        #     [{"role": "system", "content": self._system_prompt}, *[message.to_dict() for message in messages]]
        # 3. Prepare request data dict:
        #   - "model" (self model_name)
        #   - "messages" (messages_dicts)
        # 4. Execute post request to AI API `requests.post(url=self._endpoint, headers=headers, json=request_data)`
        # 5.1. If response status code is 200 then:
        #   - get response json
        #   - get choices: `choices = data.get("choices", [])`
        #   - if choices are present:
        #       - get content: `content = choices[0].get("message", {}).get("content")`
        #       - print content
        #       - return ASSISTANT message (role assistant, content is generated content)
        #   - raise ValueError("No Choice has been present in the response")
        # 5.2. Otherwise raise Exception(f"HTTP {response.status_code}: {response.text}")
        raise NotImplementedError

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
        #TODO:
        # https://platform.openai.com/docs/api-reference/chat
        # 0. Make a request in Postman to see the request and response
        # 1. Prepare headers dict with:
        #   - "Authorization" (self api key)
        #   - "Content-Type" ("application/json")
        # 2. Prepare messages list:
        #   - create messages_dicts list with system message first:
        #     [{"role": "system", "content": self._system_prompt}, *[message.to_dict() for message in messages]]
        # 3. Prepare request data dict:
        #   - "model" (self model_name)
        #   - "stream" (True)
        #   - "messages" (messages_dicts)
        # 4. Initialize empty contents list to collect streamed text chunks
        # 5. Create aiohttp ClientSession using `async with aiohttp.ClientSession() as session:`
        # 6. Execute async POST request using `async with session.post(url=self._endpoint, headers=headers, json=request_data) as response:`
        # 7.1. If response status is 200:
        #   - iterate through response content lines using `async for line in response.content:`
        #   - decode each line: `line_str = line.decode('utf-8').strip()`
        #   - check if line starts with "data: " (SSE format)
        #   - extract data: `data = line_str[6:].strip()`
        #   - if data is NOT "[DONE]":
        #       - get content snippet using self._get_content_snippet(data)
        #       - print content snippet without newline (end='')
        #       - append content snippet to contents list
        #   - otherwise print empty line (for formatting)
        # 7.2. Otherwise:
        #   - get error text: `error_text = await response.text()`
        #   - print error: f"{response.status} {error_text}"
        # 8. Return AI message with joined contents: `Message(role=Role.AI, content=''.join(contents))`
        raise NotImplementedError

    def _get_content_snippet(self, data: str) -> str:
        """
        Extract content from a streaming data chunk.

        Parses the JSON data from an SSE chunk and extracts the content delta.

        Args:
            data (str): The JSON string from the SSE data field.

        Returns:
            str: The content text from the chunk, or empty string if no content.
        """
        #TODO:
        # 1. Parse JSON data: `data = json.loads(data)`
        # 2. Get choices from data: `choices = data.get("choices")`
        # 3. If choices exist (use walrus operator: `if choices := data.get("choices"):`):
        #   - get delta from first choice: `delta = choices[0].get("delta", {})`
        #   - return content from delta: `delta.get("content", '')`
        # 4. Otherwise return empty string
        raise NotImplementedError
