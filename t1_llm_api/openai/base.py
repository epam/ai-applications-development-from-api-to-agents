from abc import ABC

from t1_llm_api.base_client import AIClient


class BaseOpenAIClient(AIClient, ABC):
    """
    Abstract base class for OpenAI API clients.

    This class extends AIClient and adds OpenAI-specific initialization,
    particularly formatting the API key as a Bearer token for authorization.

    Attributes:
        Inherits all attributes from AIClient.
    """

    def __init__(self, endpoint: str, model_name: str, system_prompt: str, api_key: str):
        """
        Initialize the OpenAI client with Bearer token authentication.

        Args:
            endpoint (str): The OpenAI API endpoint URL.
            model_name (str): The OpenAI model identifier (e.g., 'gpt-5').
            system_prompt (str): The system-level instruction for the model.
            api_key (str): The raw OpenAI API key (will be prefixed with 'Bearer ').

        Raises:
            ValueError: If api_key is None, empty, or contains only whitespace.
        """
        if not api_key or api_key.strip() == "":
            raise ValueError("API key cannot be null or empty")
        super().__init__(
            endpoint=endpoint,
            model_name=model_name,
            system_prompt=system_prompt,
            api_key=f"Bearer {api_key}"
        )