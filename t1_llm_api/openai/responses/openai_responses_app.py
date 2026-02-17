import asyncio

from t1_llm_api.base_app import start
from constants import OPENAI_RESPONSES_ENDPOINT, OPENAI_API_KEY, DEFAULT_SYSTEM_PROMPT
from t1_llm_api.openai.responses.client import OpenAIResponsesClient
from t1_llm_api.openai.responses.custom_client import CustomOpenAIResponsesClient

openai_client = OpenAIResponsesClient(
    endpoint=OPENAI_RESPONSES_ENDPOINT,
    model_name='gpt-5.2',
    api_key=OPENAI_API_KEY,
    system_prompt=DEFAULT_SYSTEM_PROMPT,
)
openai_custom_client = CustomOpenAIResponsesClient(
    endpoint=OPENAI_RESPONSES_ENDPOINT,
    model_name='gpt-5.2',
    api_key=OPENAI_API_KEY,
    system_prompt=DEFAULT_SYSTEM_PROMPT,
)

asyncio.run(
    start(True, openai_client)
)
