from t2_llms_output_tuning._clients.anthropic_client import AnthropicAIClient
from t2_llms_output_tuning._main import run


anthropic_ai_client = AnthropicAIClient('claude-sonnet-4-5')

run(
    client=anthropic_ai_client,
    print_request=True, # Switch to False if you do not want to see the request in console
    print_only_content=False, # Switch to True if you want to see only content from response

    max_output_tokens=16
)