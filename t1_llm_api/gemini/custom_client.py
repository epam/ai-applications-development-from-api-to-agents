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
        contents = []
        for msg in messages:
            role = msg.role
            contents.append({
                "role": role,
                "parts": [{"text": msg.content}]
            })
        return contents

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
        url = f"{self._endpoint}/{self._model_name}:generateContent"
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self._api_key
        }

        request_data = {
            "system_instruction": {"parts": [{"text": self._system_prompt}]},
            "contents": self._to_gemini_contents(messages),
            "generationConfig": {
                "maxOutputTokens": kwargs.get("max_tokens", 1024)
            }
        }

        response = requests.post(url=url, headers=headers, json=request_data)

        if response.status_code == 200:
            data = response.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                content = "".join(part.get("text", "") for part in parts)
                print(content)
                return Message(Role.ASSISTANT, content)
            raise ValueError("No candidates present in the response")
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")

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
        url = f"{self._endpoint}/{self._model_name}:streamGenerateContent?alt=sse"
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self._api_key
        }

        request_data = {
            "system_instruction": {"parts": [{"text": self._system_prompt}]},
            "contents": self._to_gemini_contents(messages),
            "generationConfig": {
                "maxOutputTokens": kwargs.get("max_tokens", 1024)
            }
        }
        contents = []

        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, headers=headers, json=request_data) as response:
                if response.status == 200:
                    async for line in response.content:
                        line_str = line.decode('utf-8').strip()
                        if line_str.startswith("data: "):
                            data = line_str[6:].strip()
                            parsed_data = json.loads(data)
                            candidates = parsed_data.get("candidates", [])
                            if candidates:
                                parts = candidates[0].get("content", {}).get("parts", [])
                                for part in parts:
                                    text_content = part.get("text", "")
                                    if text_content:
                                        print(text_content, end='')
                                        contents.append(text_content)
                else:
                    error_text = await response.text()
                    print(f"{response.status} {error_text}")

                print()
                return Message(role=Role.ASSISTANT, content=''.join(contents))