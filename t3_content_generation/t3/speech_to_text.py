import json

import requests

from commons.constants import OPENAI_API_KEY, OPENAI_HOST


class OpenAIClient:
    def __init__(self, endpoint: str):
        api_key = OPENAI_API_KEY
        if not api_key:
            raise ValueError("API key cannot be null or empty")
        self._api_key = "Bearer " + api_key
        self._endpoint = endpoint

    def call(self, audio_file_path: str,  print_response=True, **kwargs):
        headers = {
            "Authorization": self._api_key,
        }

        files = {'file': open(audio_file_path, 'rb')}

        response = requests.post(
            url=self._endpoint,
            headers=headers,
            files=files,
            data=kwargs
        )

        files['file'].close()

        if response.status_code == 200:
            data = response.json()
            if print_response:
                print(json.dumps(data, indent=2))
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")


client = OpenAIClient(OPENAI_HOST + "/v1/audio/transcriptions",)
client.call(
    model="gpt-4o-transcribe",  # Use whisper-1 or gpt-4o-transcribe
    audio_file_path="audio_sample.mp3"
)