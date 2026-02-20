import json
from typing import Any

import requests

from commons.constants import OPENAI_API_KEY


class OpenAIClientT3:

    def __init__(self, endpoint: str):
        api_key = OPENAI_API_KEY
        if not api_key:
            raise ValueError("API key cannot be null or empty")

        self._api_key = "Bearer " + api_key
        self._endpoint = endpoint

    def call(self, print_request = True, print_response = True, **kwargs) -> dict[str, Any]:
        headers = {
            "Authorization": self._api_key,
            "Content-Type": "application/json"
        }

        if print_request:
            print(json.dumps(kwargs, indent=2))

        response = requests.post(url=self._endpoint, headers=headers, json=kwargs)

        if response.status_code == 200:
            data = response.json()
            if print_response:
                print(json.dumps(data, indent=2))

            return data

        raise Exception(f"HTTP {response.status_code}: {response.text}")
