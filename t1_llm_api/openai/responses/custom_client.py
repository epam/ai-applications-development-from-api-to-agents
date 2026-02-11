import json
import aiohttp
import requests

from t1_llm_api._models.message import Message
from t1_llm_api._models.role import Role
from t1_llm_api.openai.base import BaseOpenAIClient


class CustomOpenAIResponsesClient(BaseOpenAIClient):
    """
    Custom HTTP client for OpenAI Responses API.

    This implementation uses raw HTTP requests (requests/aiohttp) instead of
    the official SDK, demonstrating how to interact with the Responses API directly
    and handle its unique event-based streaming format.
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
            ValueError: If the API response contains no output text.
            Exception: If the HTTP request fails (non-200 status code).

        Note:
            Uses the Responses API format with 'instructions' and 'input' parameters.
            The response is printed to stdout before being returned.
        """
        headers = {
            "Authorization": self._api_key,
            "Content-Type": "application/json"
        }

        input_messages = [message.to_dict() for message in messages]

        request_data = {
            "model": self._model_name,
            "instructions": self._system_prompt,
            "input": input_messages
        }

        response = requests.post(url=self._endpoint, headers=headers, json=request_data)

        if response.status_code == 200:
            data = response.json()
            content = self._extract_output_text(data)
            print(content)
            return Message(Role.ASSISTANT, content)
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")

    async def stream_response(self, messages: list[Message], **kwargs) -> Message:
        """
        Get a streaming response using raw HTTP with event-based streaming.

        The Responses API uses a different SSE format than Chat Completions,
        with explicit event types and data fields.

        Args:
            messages (list[Message]): The conversation history.
            **kwargs: Additional parameters for the API (currently unused).

        Returns:
            Message: The complete AI response message after all deltas are received.

        Note:
            Uses event-based Server-Sent Events (SSE) format.
            Listens for 'response.output_text.delta' events to build the response.
            Each line with "event: " specifies the event type, followed by "data: " with the payload.
        """
        headers = {
            "Authorization": self._api_key,
            "Content-Type": "application/json"
        }

        input_messages = [message.to_dict() for message in messages]

        request_data = {
            "model": self._model_name,
            "instructions": self._system_prompt,
            "input": input_messages,
            "stream": True
        }

        contents = []

        async with aiohttp.ClientSession() as session:
            async with session.post(url=self._endpoint, headers=headers, json=request_data) as response:
                if response.status == 200:
                    event_type = None
                    async for line in response.content:
                        line_str = line.decode('utf-8').strip()

                        if line_str.startswith("event: "):
                            event_type = line_str[7:].strip()
                        elif line_str.startswith("data: ") and event_type == "response.output_text.delta":
                            data = json.loads(line_str[6:])
                            delta = data.get("delta", "")
                            if delta:
                                print(delta, end='')
                                contents.append(delta)
                        elif line_str == "":
                            event_type = None
                else:
                    error_text = await response.text()
                    print(f"{response.status} {error_text}")

        print()
        return Message(role=Role.ASSISTANT, content=''.join(contents))

    @staticmethod
    def _extract_output_text(data: dict) -> str:
        """
        Extract text content from the Responses API output.

        The Responses API returns structured output with nested objects.
        This method navigates the structure to find the output_text content.

        Args:
            data (dict): The JSON response data from the API.

        Returns:
            str: The extracted text content.

        Raises:
            ValueError: If no output text is found in the response structure.
        """
        output = data.get("output", [])
        for item in output:
            if item.get("type") == "message":
                for content_part in item.get("content", []):
                    if content_part.get("type") == "output_text":
                        return content_part.get("text", "")
        raise ValueError("No output text found in the response")