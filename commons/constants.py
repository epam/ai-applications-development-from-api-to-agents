"""
Configuration constants for AI service integrations.

This module centralizes all API endpoints, API keys, and default configuration
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

# Anthropic API configuration
ANTHROPIC_ENDPOINT = "https://api.anthropic.com/v1/messages"
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')

# Google Gemini API configuration
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models"
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')