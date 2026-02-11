import asyncio

from t1_llm_api.anthropic.client import AnthropicAIClient
from t1_llm_api.anthropic.custom_client import CustomAnthropicAIClient
from t1_llm_api.base_app import start
from t1_llm_api.constants import ANTHROPIC_ENDPOINT, ANTHROPIC_API_KEY, DEFAULT_SYSTEM_PROMPT

anthropic_client = AnthropicAIClient(
    endpoint=ANTHROPIC_ENDPOINT,
    model_name='claude-sonnet-4-5',
    api_key=ANTHROPIC_API_KEY,
    system_prompt=DEFAULT_SYSTEM_PROMPT,
)
anthropic_custom_client = CustomAnthropicAIClient(
    endpoint=ANTHROPIC_ENDPOINT,
    model_name='claude-sonnet-4-5',
    api_key=ANTHROPIC_API_KEY,
    system_prompt=DEFAULT_SYSTEM_PROMPT,
)

asyncio.run(
    start(True, anthropic_client)
)
