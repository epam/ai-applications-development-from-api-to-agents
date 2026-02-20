import json

import requests




class EmbeddingsClient:
    _endpoint: str
    _api_key: str

    def __init__(self, endpoint: str, model_name: str, api_key: str):
        if not api_key or api_key.strip() == "":
            raise ValueError("API key cannot be null or empty")

        self._endpoint = endpoint
        self._api_key = "Bearer " + api_key
        self._model_name = model_name

    def get_embeddings(
            self, inputs: str | list[str],
            dimensions: int,
            print_response: bool = False
    ) -> dict[int, list[float]]:
        """
        Generate dict of indexed embeddings:
            inputs[0](text) -> [0][embedding]
            inputs[1](text) -> [1][embedding]
            ...

        Args:
            inputs: input text, can be singular string or list of strings
            dimensions: number of dimensions
            print_response: to print response in chat or not
        """
        headers = {
            "Authorization": self._api_key,
            "Content-Type": "application/json"
        }
        request_data = {
            #TODO: add:
            # - inputs
            # - dimensions
            # - model
            # https://developers.openai.com/api/reference/resources/embeddings/methods/create
        }

        response = requests.post(url=self._endpoint, headers=headers, json=request_data, timeout=60)

        if response.status_code == 200:
            # TODO: Get response:
            #  Response JSON:
            #  {
            #     "data": [
            #         {
            #             "embedding": [
            #                 0.19686688482761383,
            #                 ...
            #             ],
            #             "index": 0,
            #             "object": "embedding"
            #         }
            #     ],
            #     ...
            #  }
            response_json = None # TODO: Parse to json (response.json())
            data = None # TODO: Get `data`
            if print_response:
                print("\n" + "=" * 50 + " RESPONSE " + "=" * 50)
                print(json.dumps(response_json, indent=2))
                print("=" * 108)
            return None # TODO: Return self._from_data(data)
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    def _from_data(self, data: list[dict]) -> dict[int, list[float]]:
        return {embedding_obj['index']: embedding_obj['embedding'] for embedding_obj in data}