import base64
import json
from datetime import datetime

import requests

from constants import OPENAI_API_KEY, OPENAI_HOST


# https://developers.openai.com/api/docs/guides/audio#add-audio-to-your-existing-application

class _OpenAIClient:

    def __init__(self):
        #TODO:
        # 1. Set up `_api_key` (use OPENAI_API_KEY env var), don't forget to check that it is present and add 'Bearer ' prefix
        # 2. Set up `_endpoint` (OPENAI_HOST + "/v1/chat/completions")
        raise NotImplementedError

    def call(self, print_request=True, print_response=True, **kwargs):
        #TODO:
        # 1. Set up `headers` dict, provide Authorization header with self._api_key and Content-Type as application/json
        # 2. Print request: print(json.dumps(kwargs, indent=2))
        # 3. Make POST request (use `requests` lib) with such params:
        #   - url=self._endpoint
        #   - headers=headers
        #   - json=kwargs
        # 4. If response is 200 then:
        #   - get response json and assign to the `data` variable
        #   - print response: `print(json.dumps(data, indent=2))`
        #   - get `choices` from `data`
        #   - if `choices` are present:
        #       - get `message` from first choice
        #       - if `message` is present:
        #           - get `audio` from `message`
        #           - if `audio` is present:
        #               - get audio `data`
        #               - if audio `data` is present:
        #                   - decode it wit base64.b64decode
        #                   - create output file name `f"{datetime.now()}.mp3"` and assign to `output_file` variable
        #                   - save it (open output_file (wb) and write byte `response.content`)
        # 4.1. Otherwise, raise Exception(f"HTTP {response.status_code}: {response.text}")
        raise NotImplementedError


def _encode_audio(audio_file_path):
    #TODO:
    # Function to encode audio to base64 you can find in documentation (works in the same way for images and audios)
    # https://developers.openai.com/api/docs/guides/images-vision?lang=python&format=base64-encoded#analyze-images
    raise NotImplementedError


client = _OpenAIClient()
client.call(
    #TODO:
    # - model="gpt-4o-audio-preview"
    # - modalities=["text", "audio"],
    # - audio={"voice": "ballad", "format": "mp3"},
    # - messages=[
    #     {
    #         "role": "user",
    #         "content": [
    #             {
    #                 "type": "input_audio",
    #                 "input_audio": {
    #                     "data": _encode_audio("question.mp3"),
    #                     "format": "mp3"
    #                 }
    #             }
    #         ]
    #     }
    # ]
    # ---
    # Optional: Instead of input_audio you can send text and model will generate response in audio format.
)
