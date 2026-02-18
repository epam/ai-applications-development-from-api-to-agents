from t2_llms_output_tuning._clients.gemini_client import GeminiAIClient
from t2_llms_output_tuning._main import run


gemini_ai_client = GeminiAIClient('gemini-3-flash-preview')

run(
    client=gemini_ai_client,
    print_request=True, # Switch to False if you do not want to see the request in console
    print_only_content=False, # Switch to True if you want to see only content from response

    generationConfig={
        "maxOutputTokens": 16,
        "thinkingConfig": {
            "includeThoughts": True
        }
    }
)