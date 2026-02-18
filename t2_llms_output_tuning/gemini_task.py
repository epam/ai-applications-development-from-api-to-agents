from t2_llms_output_tuning._clients.gemini_client import GeminiAIClient
from t2_llms_output_tuning._main import run


run(
    client=GeminiAIClient('gemini-3-flash-preview'),
    print_request=True, # Switch to False if you do not want to see the request in console
    print_only_content=False, # Switch to True if you want to see only content from response

    generationConfig={
        "maxOutputTokens": 16,
        "thinkingConfig": {
            "includeThoughts": True
        }
    }
)