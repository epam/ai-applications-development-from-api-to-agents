import json

import requests

from commons.constants import GEMINI_API_KEY, GEMINI_ENDPOINT
from t2_llms_output_tuning._clients._base_client import AIClient
from commons.models.message import Message
from commons.models.role import Role


class GeminiAIClient(AIClient):

    def __init__(self, model_name: str):
        super().__init__(
            endpoint=GEMINI_ENDPOINT,
            model_name=model_name,
            api_key=GEMINI_API_KEY,
            api_key_header_name="x-goog-api-key"
        )

    def response(
            self,
            messages: list[Message],
            print_request: bool,
            print_only_content: bool,
            **kwargs
    ) -> Message:
        url = f"{self._endpoint}/{self._model_name}:generateContent"
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self._api_key
        }
        generation_config = kwargs.get("generationConfig", {})
        generation_config.setdefault("maxOutputTokens", 1024)
        request_data = {
            "contents": self._to_gemini_contents(messages),
            "generationConfig": generation_config,
        }
        safety_settings = kwargs.get("safetySettings")
        if safety_settings:
            request_data["safetySettings"] = safety_settings

        if print_request:
            self._print_request(request_data, headers)

        response = requests.post(url=url, headers=headers, json=request_data)

        if response.status_code == 200:
            data = response.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                content = "".join(part.get("text", "") for part in parts)
                print("" + "=" * 50 + " RESPONSE " + "=" * 50)
                if print_only_content:
                    print(content)
                else:
                    print(json.dumps(data, indent=2, sort_keys=True))
                print("=" * 109)
                return Message(Role.ASSISTANT, content)
            raise ValueError("No candidates present in the response")
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")

    @staticmethod
    def _to_gemini_contents(messages: list[Message]) -> list[dict]:
        contents = []
        for msg in messages:
            contents.append({
                "role": msg.role.value,
                "parts": [{"text": msg.content}]
            })
        return contents