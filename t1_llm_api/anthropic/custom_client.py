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
        #TODO:
        # https://platform.claude.com/docs/en/build-with-claude/working-with-messages
        # 0. Make a request in Postman to see the request and response
        # 1. Prepare headers dict with:
        #   - "x-api-key" (self api key)
        #   - "Content-Type" ("application/json")
        #   - "anthropic-version" ("2023-06-01")
        # 2. Prepare request data dict:
        #   - "model" (self model_name)
        #   - "system" (self system_prompt)
        #   - "max_tokens" (1024)
        #   - "messages" ([message.to_dict() for message in messages])
        # 3. Execute post request to AI API `requests.post(url=self._endpoint, headers=headers, json=request_data)`
        # 4.1. If response status code is 200 then:
        #   - get response json
        #   - get content block
        #   - if content blocks are present:
        #       - get content: "".join(block.get("text", "") for block in content_blocks if block.get("type") == "text")
        #       - print content
        #       - return ASSISTANT message (role assistant, content is generated content)
        #   - raise ValueError("No content blocks present in the response")
        # 4.2. Otherwise raise Exception(f"HTTP {response.status_code}: {response.text}")
        raise NotImplementedError

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
        #TODO:
        # https://platform.claude.com/docs/en/build-with-claude/streaming
        # 0. Make a request in Postman to see the request and response
        # 1. Prepare headers dict with:
        #   - "x-api-key" (self api key)
        #   - "Content-Type" ("application/json")
        #   - "anthropic-version" ("2023-06-01")
        # 2. Prepare request data dict:
        #   - "model" (self model_name)
        #   - "system" (self system_prompt)
        #   - "max_tokens" (kwargs.get("max_tokens", 1024))
        #   - "stream" (True)
        #   - "messages" ([msg.to_dict() for msg in messages])
        # 3. Initialize empty contents list to collect streamed text chunks
        # 4. Create aiohttp ClientSession using `async with aiohttp.ClientSession() as session:`
        # 5. Execute async POST request using `async with session.post(url=self._endpoint, headers=headers, json=request_data) as response:`
        # 6.1. If response status is 200:
        #   - iterate through response content lines using `async for line in response.content:`
        #   - decode each line: `line_str = line.decode('utf-8').strip()`
        #   - check if line starts with "data: " (SSE format)
        #   - extract JSON data: `data = line_str[6:].strip()`
        #   - parse JSON data: `parsed_data = json.loads(data)`
        #   - get event type: `event_type = parsed_data.get("type")`
        #   - if event_type == "content_block_delta":
        #       - get delta: `delta = parsed_data.get("delta", {})`
        #       - if delta.get("type") == "text_delta":
        #           - get text content: `text_content = delta.get("text", "")`
        #           - if text_content is not empty:
        #               - print text_content without newline (end='')
        #               - append text_content to contents list
        #   - else if event_type is `message_stop` then break from the loop
        # 6.2. Otherwise:
        #   - get error text: `error_text = await response.text()`
        #   - print error: f"{response.status} {error_text}"
        # 7. Print empty line (for formatting)
        # 8. Return ASSISTANT message with joined contents: `Message(role=Role.ASSISTANT, content=''.join(contents))`
        raise NotImplementedError
