from t2_llms_output_tuning._clients.openai_chat_completions_client import OpenAIChatCompletionsClient
from t2_llms_output_tuning._clients.openai_responses_client import OpenAIResponsesClient
from t2_llms_output_tuning._main import run


chat_completions_client = OpenAIChatCompletionsClient('gpt-5.2')
responses_client = OpenAIResponsesClient('gpt-5.2')

run(
    client=responses_client,
    print_request=True, # Switch to False if you do not want to see the request in console
    print_only_content=False, # Switch to True if you want to see only content from response

    max_output_tokens=16
)