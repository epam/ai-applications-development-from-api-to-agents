import json
from abc import ABC, abstractmethod
from typing import Any

from commons.models.message import Message


class AIClient(ABC):

    def __init__(self, endpoint: str, model_name: str, api_key: str, api_key_header_name: str):
        if not api_key or api_key.strip() == "":
            raise ValueError("API key cannot be null or empty")

        self._api_key = api_key
        self._endpoint = endpoint
        self._model_name = model_name
        self._api_key_header_name = api_key_header_name

    @abstractmethod
    def response(
            self,
            messages: list[Message],
            print_request: bool,
            print_only_content: bool,
            **kwargs
    ) -> Message:
        """
        Send synchronous request to AI API and return AI response.
        """
        ...

    def _print_request(self, request_data: dict, headers: dict):
        print("\n" + "=" * 50 + " REQUEST " + "=" * 50)
        print(f"🔗 Endpoint: {self._endpoint}")

        print("\n📋 Headers:")
        safe_headers = self._safe_headers(headers)
        for key, value in safe_headers.items():
            print(f"  {key}: {value}")

        print("\n📝 Request Body:")
        print(json.dumps(request_data, indent=2))

    def _safe_headers(self, headers: dict) -> dict[str, Any]:
        safe_headers = headers.copy()
        if self._api_key_header_name in safe_headers:
            api_key = safe_headers[self._api_key_header_name]
            safe_headers[self._api_key_header_name] = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"

        return safe_headers
