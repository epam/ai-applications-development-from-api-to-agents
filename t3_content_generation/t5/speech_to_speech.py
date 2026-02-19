import base64
import json
from datetime import datetime

import requests

from constants import OPENAI_API_KEY, OPENAI_HOST


class _OpenAIClient:

    def __init__(self):
        api_key = OPENAI_API_KEY
        if not api_key:
            raise ValueError("API key cannot be null or empty")

        self._api_key = "Bearer " + api_key
        self._endpoint = OPENAI_HOST + "/v1/chat/completions"

    def call(self, print_request=True, print_response=True, **kwargs):
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
            choices = data.get("choices", [])
            if choices:
                message = choices[0].get("message", {})
                if message:
                    audio = message.get("audio", {})
                    if audio:
                        audio_data = audio.get("data")
                        if audio_data:
                            audio_bytes = base64.b64decode(audio_data)
                            output_file = f"{datetime.now()}.mp3"

                            with open(output_file, 'wb') as f:
                                f.write(audio_bytes)
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")


def _encode_audio(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode("utf-8")


client = _OpenAIClient()
client.call(
    model="gpt-audio",
    modalities=["text", "audio"],
    audio={"voice": "ballad", "format": "mp3"},
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": _encode_audio("question.mp3"),
                        "format": "mp3"
                    }
                }
            ]
        }
    ]
)
