from typing import Any

import requests

from commons.constants import OPENAI_RESPONSES_ENDPOINT
from t8_agent.task.tools.base import BaseTool


class WebSearchTool(BaseTool):

    def __init__(self, open_ai_api_key: str):
        self.__api_key = f"Bearer {open_ai_api_key}"
        self.__endpoint = OPENAI_RESPONSES_ENDPOINT

    @property
    def name(self) -> str:
        #TODO: Provide tool name as `web_search_tool`
        raise NotImplementedError()

    @property
    def description(self) -> str:
        #TODO: Provide description of this tool
        raise NotImplementedError()

    @property
    def input_schema(self) -> dict[str, Any]:
        #TODO: Provide tool params Schema (it applies `request` string to search by)
        raise NotImplementedError()

    def execute(self, arguments: dict[str, Any]) -> str:
        #TODO:
        # https://developers.openai.com/api/docs/guides/tools-web-search
        # 1. Create `headers` dict: "Authorization": self.__api_key, "Content-Type": "application/json"
        # 2. Create `request_data` dict with:
        #    - "model": "gpt-5.2"
        #    - "tools": [{"type": "web_search"}]
        #    - "input": str(arguments["request"])
        # 3. Make POST call with `requests` lib: `url=self.__endpoint, headers=headers, json=request_data`
        # 4. Check if response status is 200 and if yes then return message content (output -> message -> content -> output_text),
        #    otherwise return `f"Error: {response.status_code} {response.text}"`
        raise NotImplementedError()