import json
import aiohttp
import requests

from t1_llm_api._models.message import Message
from t1_llm_api._models.role import Role
from t1_llm_api.base_client import AIClient


class CustomGeminiAIClient(AIClient):
    """
    Custom HTTP client for Google Gemini API.

    This implementation uses raw HTTP requests (requests/aiohttp) instead of
    the official SDK, demonstrating how to interact with Gemini's API directly
    and handle its Server-Sent Events (SSE) streaming format.
    """

    def _to_gemini_contents(self, messages: list[Message]) -> list[dict]:
        """
        Convert Message objects to Gemini's content dictionary format.

        Gemini uses a different role naming convention where AI messages use
        the role "model" instead of "assistant".

        Args:
            messages (list[Message]): The conversation messages to convert.

        Returns:
            list[dict]: Messages in Gemini's dictionary format.
        """
        #TODO:
        # 1. Initialize empty contents list
        # 2. Iterate through messages:
        #   - get role from message: `role = msg.role`
        #   - append dict to contents: `{"role": role, "parts": [{"text": msg.content}]}`
        # 3. Return contents list
        raise NotImplementedError

    def response(self, messages: list[Message], **kwargs) -> Message:
        """
        Get a synchronous response using raw HTTP POST request.

        Args:
            messages (list[Message]): The conversation history.
            **kwargs: Additional parameters like max_tokens (default: 1024).

        Returns:
            Message: The AI's response message.

        Raises:
            ValueError: If the API response contains no candidates.
            Exception: If the HTTP request fails (non-200 status code).

        Note:
            The URL is constructed by appending ':generateContent' to the model endpoint.
            Uses 'x-goog-api-key' header for authentication.
            Response candidates contain content parts that are concatenated.
        """
        #TODO:
        # https://ai.google.dev/gemini-api/docs/text-generation
        # 0. Make a request in Postman to see the request and response
        # 1. Construct URL: `url = f"{self._endpoint}/{self._model_name}:generateContent"`
        # 2. Prepare headers dict with:
        #   - "Content-Type" ("application/json")
        #   - "x-goog-api-key" (self api key)
        # 3. Prepare request data dict:
        #   - "system_instruction" ({"parts": [{"text": self._system_prompt}]})
        #   - "contents" (self._to_gemini_contents(messages))
        #   - "generationConfig" ({"maxOutputTokens": kwargs.get("max_tokens", 1024)})
        # 4. Execute post request to AI API `requests.post(url=url, headers=headers, json=request_data)`
        # 5.1. If response status code is 200 then:
        #   - get response json
        #   - get candidates: `candidates = data.get("candidates", [])`
        #   - if candidates are present:
        #       - get parts: `parts = candidates[0].get("content", {}).get("parts", [])`
        #       - get content: `"".join(part.get("text", "") for part in parts)`
        #       - print content
        #       - return ASSISTANT message (role assistant, content is generated content)
        #   - raise ValueError("No candidates present in the response")
        # 5.2. Otherwise raise Exception(f"HTTP {response.status_code}: {response.text}")
        raise NotImplementedError

    async def stream_response(self, messages: list[Message], **kwargs) -> Message:
        """
        Get a streaming response using raw HTTP with Server-Sent Events (SSE).

        The response is streamed using Gemini's SSE format, with text chunks
        printed immediately as they arrive.

        Args:
            messages (list[Message]): The conversation history.
            **kwargs: Additional parameters like max_tokens (default: 1024).

        Returns:
            Message: The complete AI response message after all chunks are received.

        Note:
            The URL is constructed with ':streamGenerateContent?alt=sse' endpoint.
            Uses Server-Sent Events (SSE) format where each line starts with "data: ".
            Each SSE chunk contains candidates with content parts.
            Each text chunk is printed to stdout as it arrives.
        """
        #TODO:
        # https://ai.google.dev/gemini-api/docs/text-generation
        # 0. Make a request in Postman to see the request and response
        # 1. Construct URL: `url = f"{self._endpoint}/{self._model_name}:streamGenerateContent?alt=sse"`
        # 2. Prepare headers dict with:
        #   - "Content-Type" ("application/json")
        #   - "x-goog-api-key" (self api key)
        # 3. Prepare request data dict:
        #   - "system_instruction" ({"parts": [{"text": self._system_prompt}]})
        #   - "contents" (self._to_gemini_contents(messages))
        #   - "generationConfig" ({"maxOutputTokens": kwargs.get("max_tokens", 1024)})
        # 4. Initialize empty contents list to collect streamed text chunks
        # 5. Create aiohttp ClientSession using `async with aiohttp.ClientSession() as session:`
        # 6. Execute async POST request using `async with session.post(url=url, headers=headers, json=request_data) as response:`
        # 7.1. If response status is 200:
        #   - iterate through response content lines using `async for line in response.content:`
        #   - decode each line: `line_str = line.decode('utf-8').strip()`
        #   - check if line starts with "data: " (SSE format)
        #   - extract JSON data: `data = line_str[6:].strip()`
        #   - parse JSON data: `parsed_data = json.loads(data)`
        #   - get candidates: `candidates = parsed_data.get("candidates", [])`
        #   - if candidates are present:
        #       - get parts: `parts = candidates[0].get("content", {}).get("parts", [])`
        #       - for each part in parts:
        #           - get text content: `text_content = part.get("text", "")`
        #           - if text_content is not empty:
        #               - print text_content without newline (end='')
        #               - append text_content to contents list
        # 7.2. Otherwise:
        #   - get error text: `error_text = await response.text()`
        #   - print error: f"{response.status} {error_text}"
        # 8. Print empty line (for formatting)
        # 9. Return ASSISTANT message with joined contents: `Message(role=Role.ASSISTANT, content=''.join(contents))`
        raise NotImplementedError