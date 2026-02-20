import json
import aiohttp
import requests

from commons.models.message import Message
from commons.models.role import Role
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
        #TODO:
        # https://developers.openai.com/api/docs/guides/text?lang=curl
        # 0. Make a request in Postman to see the request and response
        # 1. Prepare headers dict with:
        #   - "Authorization" (self api key)
        #   - "Content-Type" ("application/json")
        # 2. Prepare input messages list: `input_messages = [message.to_dict() for message in messages]`
        # 3. Prepare request data dict:
        #   - "model" (self model_name)
        #   - "instructions" (self system_prompt)
        #   - "input" (input_messages)
        # 4. Execute post request to AI API `requests.post(url=self._endpoint, headers=headers, json=request_data)`
        # 5.1. If response status code is 200 then:
        #   - get response json
        #   - get content using self._extract_output_text(data)
        #   - print content
        #   - return ASSISTANT message (role assistant, content is generated content)
        # 5.2. Otherwise raise Exception(f"HTTP {response.status_code}: {response.text}")
        raise NotImplementedError

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
        #TODO:
        # https://developers.openai.com/api/docs/guides/text?lang=curl
        # 0. Make a request in Postman to see the request and response
        # 1. Prepare headers dict with:
        #   - "Authorization" (self api key)
        #   - "Content-Type" ("application/json")
        # 2. Prepare input messages list: `input_messages = [message.to_dict() for message in messages]`
        # 3. Prepare request data dict:
        #   - "model" (self model_name)
        #   - "instructions" (self system_prompt)
        #   - "input" (input_messages)
        #   - "stream" (True)
        # 4. Initialize empty contents list to collect streamed text chunks
        # 5. Create aiohttp ClientSession using `async with aiohttp.ClientSession() as session:`
        # 6. Execute async POST request using `async with session.post(url=self._endpoint, headers=headers, json=request_data) as response:`
        # 7.1. If response status is 200:
        #   - initialize event_type = None
        #   - iterate through response content lines using `async for line in response.content:`
        #   - decode each line: `line_str = line.decode('utf-8').strip()`
        #   - if line starts with "event: ":
        #       - extract event type: `event_type = line_str[7:].strip()`
        #   - elif line starts with "data: " and event_type == "response.output_text.delta":
        #       - parse JSON data: `data = json.loads(line_str[6:])`
        #       - get delta: `delta = data.get("delta", "")`
        #       - if delta is not empty:
        #           - print delta without newline (end='')
        #           - append delta to contents list
        #   - elif line is empty string:
        #       - reset event_type = None
        # 7.2. Otherwise:
        #   - get error text: `error_text = await response.text()`
        #   - print error: f"{response.status} {error_text}"
        # 8. Print empty line (for formatting)
        # 9. Return ASSISTANT message with joined contents: `Message(role=Role.ASSISTANT, content=''.join(contents))`
        raise NotImplementedError

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
        #TODO:
        # 1. Get output list from data: `output = data.get("output", [])`
        # 2. Iterate through items in output:
        #   - if item.get("type") == "message":
        #       - iterate through content parts: `for content_part in item.get("content", []):`
        #           - if content_part.get("type") == "output_text":
        #               - return content_part.get("text", "")
        # 3. If no output text found, raise ValueError("No output text found in the response")
        raise NotImplementedError