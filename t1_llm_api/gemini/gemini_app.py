import asyncio

from t1_llm_api.base_app import start
from t1_llm_api.constants import GEMINI_ENDPOINT, GEMINI_API_KEY, DEFAULT_SYSTEM_PROMPT
from t1_llm_api.gemini.client import GeminiAIClient
from t1_llm_api.gemini.custom_client import CustomGeminiAIClient

gemini_client = GeminiAIClient(
    endpoint=GEMINI_ENDPOINT,
    model_name='gemini-3-flash-preview',
    api_key=GEMINI_API_KEY,
    system_prompt=DEFAULT_SYSTEM_PROMPT,
)
gemini_custom_client = CustomGeminiAIClient(
    endpoint=GEMINI_ENDPOINT,
    model_name='gemini-3-flash-preview',
    api_key=GEMINI_API_KEY,
    system_prompt=DEFAULT_SYSTEM_PROMPT,
)

asyncio.run(
    start(False, gemini_custom_client)
)