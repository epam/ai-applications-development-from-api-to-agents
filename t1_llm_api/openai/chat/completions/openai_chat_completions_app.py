import asyncio

from t1_llm_api.base_app import start
from commons.constants import OPENAI_CHAT_COMPLETIONS_ENDPOINT, OPENAI_API_KEY, DEFAULT_SYSTEM_PROMPT
from t1_llm_api.openai.chat.completions.client import OpenAIClient
from t1_llm_api.openai.chat.completions.custom_client import CustomOpenAIClient

openai_client = OpenAIClient(
    endpoint=OPENAI_CHAT_COMPLETIONS_ENDPOINT,
    model_name='gpt-5.2',
    api_key=OPENAI_API_KEY,
    system_prompt=DEFAULT_SYSTEM_PROMPT,
)
openai_custom_client = CustomOpenAIClient(
    endpoint=OPENAI_CHAT_COMPLETIONS_ENDPOINT,
    model_name='gpt-5.2',
    api_key=OPENAI_API_KEY,
    system_prompt=DEFAULT_SYSTEM_PROMPT,
)

asyncio.run(
    start(True, openai_client)
)
