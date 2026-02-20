import json

import requests

from commons.constants import ANTHROPIC_ENDPOINT, ANTHROPIC_API_KEY
from t2_llms_output_tuning._clients._base_client import AIClient
from commons.models.message import Message
from commons.models.role import Role


class AnthropicAIClient(AIClient):

    def __init__(self, model_name: str):
        super().__init__(
            endpoint=ANTHROPIC_ENDPOINT,
            model_name=model_name,
            api_key=ANTHROPIC_API_KEY,
            api_key_header_name="x-api-key"
        )

    def response(
            self,
            messages: list[Message],
            print_request: bool,
            print_only_content: bool,
            **kwargs
    ) -> Message:
        headers = {
            "x-api-key": self._api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        request_data = {
            "model": self._model_name,
            "max_tokens": kwargs.get("max_tokens", 1024),
            "messages": [message.to_dict() for message in messages],
            **kwargs
        }
        if print_request:
            self._print_request(request_data, headers)

        response = requests.post(url=self._endpoint, headers=headers, json=request_data)

        if response.status_code == 200:
            data = response.json()
            content_blocks = data.get("content", [])
            if content_blocks:
                content = "".join(block.get("text", "") for block in content_blocks if block.get("type") == "text")
                print("" + "=" * 50 + " RESPONSE " + "=" * 50)
                if print_only_content:
                    print(content)
                else:
                    print(json.dumps(data, indent=2, sort_keys=True))
                print("=" * 109)
                return Message(Role.ASSISTANT, content)
            raise ValueError("No content blocks present in the response")
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
