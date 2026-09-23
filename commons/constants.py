"""
Configuration constants for AI service integrations.

This module centralizes all API endpoints, API keys, models, and default configuration
values used across different AI service providers (OpenAI, Anthropic, Gemini).

All API keys are loaded from environment variables for security.
"""

import os

# Default system prompt used across all AI services
DEFAULT_SYSTEM_PROMPT = "You are an assistant who answers concisely and informatively."

# OpenAI API configuration
OPENAI_HOST = "https://api.openai.com"
OPENAI_CHAT_COMPLETIONS_ENDPOINT = f"{OPENAI_HOST}/v1/chat/completions"
OPENAI_RESPONSES_ENDPOINT = f"{OPENAI_HOST}/v1/responses"
OPENAI_EMBEDDINGS_ENDPOINT = f"{OPENAI_HOST}/v1/embeddings"
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
# GPT-5.6 family: gpt-5.6-sol (flagship), gpt-5.6-terra (mini tier), gpt-5.6-luna (nano tier).
# They are reasoning models: a non-default `temperature`/`top_p` works only with `reasoning_effort="none"`,
# `max_completion_tokens` replaces `max_tokens`, and `stop`/`presence_penalty` are not supported
OPENAI_TERRA_MODEL = "gpt-5.6-terra"
OPENAI_LUNA_MODEL = "gpt-5.6-luna"
OPENAI_EMBEDDINGS_MODEL = "text-embedding-3-small"

# Anthropic API configuration
ANTHROPIC_ENDPOINT = "https://api.anthropic.com/v1/messages"
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
# Claude Sonnet 5 rejects non-default `temperature`/`top_p`/`top_k` and `budget_tokens` thinking, and runs adaptive
# thinking by default (responses can start with a `thinking` block). Claude Haiku 4.5 still supports them
ANTHROPIC_SONNET_MODEL = "claude-sonnet-5"
ANTHROPIC_HAIKU_MODEL = "claude-haiku-4-5"

# Google Gemini API configuration
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models"
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
GEMINI_FLASH_MODEL = "gemini-3-flash-preview"

# User Service API configuration
USER_SERVICE_ENDPOINT = "http://localhost:8041"