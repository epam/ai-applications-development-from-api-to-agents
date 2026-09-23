import asyncio

from t1_llm_api.base_app import start
from commons.constants import GEMINI_ENDPOINT, GEMINI_API_KEY, DEFAULT_SYSTEM_PROMPT, GEMINI_FLASH_MODEL
from t1_llm_api.gemini.client import GeminiAIClient
from t1_llm_api.gemini.custom_client import CustomGeminiAIClient

gemini_client = GeminiAIClient(
    endpoint=GEMINI_ENDPOINT,
    model_name=GEMINI_FLASH_MODEL,
    api_key=GEMINI_API_KEY,
    system_prompt=DEFAULT_SYSTEM_PROMPT,
)
gemini_custom_client = CustomGeminiAIClient(
    endpoint=GEMINI_ENDPOINT,
    model_name=GEMINI_FLASH_MODEL,
    api_key=GEMINI_API_KEY,
    system_prompt=DEFAULT_SYSTEM_PROMPT,
)

asyncio.run(
    start(False, gemini_client)
)