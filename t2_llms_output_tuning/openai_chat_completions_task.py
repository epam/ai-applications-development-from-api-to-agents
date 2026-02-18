from t2_llms_output_tuning._clients.openai_chat_completions_client import OpenAIChatCompletionsClient
from t2_llms_output_tuning._main import run


run(
    client=OpenAIChatCompletionsClient('gpt-5.2'),
    print_request=True,  # Switch to False if you do not want to see the request in console
    print_only_content=False,  # Switch to True if you want to see only content from response

    max_tokens=16
)
