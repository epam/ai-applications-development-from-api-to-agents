import json
from datetime import datetime

import requests

from commons.constants import OPENAI_API_KEY, OPENAI_HOST


class _OpenAIClient:

    def __init__(self):
        api_key = OPENAI_API_KEY
        if not api_key:
            raise ValueError("API key cannot be null or empty")

        self._api_key = "Bearer " + api_key
        self._endpoint = OPENAI_HOST + "/v1/audio/speech"

    def call(self, print_request=True, **kwargs):
        headers = {
            "Authorization": self._api_key,
            "Content-Type": "application/json"
        }

        output_file: str = f"{datetime.now()}.mp3"

        if print_request:
            print(json.dumps(kwargs, indent=2))

        response = requests.post(url=self._endpoint, headers=headers, json=kwargs)

        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f"Audio saved to {output_file}")
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")


class Voice:
    alloy: str = 'alloy'
    ash: str = 'ash'
    ballad: str = 'ballad'
    coral: str = 'coral'
    echo: str = 'echo'
    fable: str = 'fable'
    nova: str = 'nova'
    onyx: str = 'onyx'
    sage: str = 'sage'
    shimmer: str = 'shimmer'


client = _OpenAIClient()
client.call(
    model="gpt-4o-mini-tts",
    input="Why can't we say that black is white?",
    voice=Voice.coral,
    instructions="Speak in a cheerful and positive tone."
)

