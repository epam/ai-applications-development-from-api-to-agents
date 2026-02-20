import json

from openai import OpenAI

from commons.constants import OPENAI_API_KEY, OPENAI_RESPONSES_ENDPOINT
from t2_llms_output_tuning._clients._base_client import AIClient
from commons.models.message import Message
from commons.models.role import Role


class OpenAIResponsesClient(AIClient):

    def __init__(self, model_name: str):
        api_key = OPENAI_API_KEY
        if not api_key or api_key.strip() == "":
            raise ValueError("API key cannot be null or empty")

        super().__init__(
            endpoint=OPENAI_RESPONSES_ENDPOINT,
            model_name=model_name,
            api_key=f"Bearer {api_key}",
            api_key_header_name="Authorization"
        )
        self._client = OpenAI(api_key=api_key)

    def response(
            self,
            messages: list[Message],
            print_request: bool,
            print_only_content: bool,
            **kwargs
    ) -> Message:
        input_messages = [message.to_dict() for message in messages]

        request_data = {
            "model": self._model_name,
            "input": input_messages,
            **kwargs
        }
        if print_request:
            headers = {
                "Authorization": self._api_key,
                "Content-Type": "application/json"
            }
            self._print_request(request_data, headers)

        api_response = self._client.responses.create(
            model=self._model_name,
            input=input_messages,
            **kwargs
        )

        content = api_response.output_text
        print("" + "=" * 50 + " RESPONSE " + "=" * 50)
        if print_only_content:
            print(content)
        else:
            print(json.dumps(api_response.to_dict(), indent=2, sort_keys=True))
        print("=" * 109)
        return Message(Role.ASSISTANT, content)