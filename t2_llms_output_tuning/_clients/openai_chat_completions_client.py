import json

import requests

from commons.constants import OPENAI_API_KEY, OPENAI_CHAT_COMPLETIONS_ENDPOINT
from t2_llms_output_tuning._clients._base_client import AIClient
from commons.models.message import Message
from commons.models.role import Role


class OpenAIChatCompletionsClient(AIClient):

    def __init__(self, model_name: str):
        api_key = OPENAI_API_KEY
        if not api_key or api_key.strip() == "":
            raise ValueError("API key cannot be null or empty")

        super().__init__(
            endpoint=OPENAI_CHAT_COMPLETIONS_ENDPOINT,
            model_name=model_name,
            api_key=f"Bearer {api_key}",
            api_key_header_name="Authorization"
        )

    def response(
            self,
            messages: list[Message],
            print_request: bool,
            print_only_content: bool,
            **kwargs
    ) -> Message:
        headers = {
            "Authorization": self._api_key,
            "Content-Type": "application/json"
        }
        request_data = {
            "model": self._model_name,
            "messages": [message.to_dict() for message in messages],
            **kwargs
        }
        if print_request:
            self._print_request(request_data, headers)

        response = requests.post(url=self._endpoint, headers=headers, json=request_data)

        if response.status_code == 200:
            data = response.json()
            choices = data.get("choices", [])
            if choices:
                content = choices[0].get("message", {}).get("content")
                print("" + "=" * 50 + " RESPONSE " + "=" * 50)
                if print_only_content:
                    print(content)
                else:
                    print(json.dumps(data, indent=2, sort_keys=True))
                print("=" * 109)
                return Message(Role.ASSISTANT, content)
            raise ValueError("No Choice has been present in the response")
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
