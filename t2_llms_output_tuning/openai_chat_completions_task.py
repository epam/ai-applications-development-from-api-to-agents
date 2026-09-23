from t2_llms_output_tuning._clients.openai_chat_completions_client import OpenAIChatCompletionsClient
from t2_llms_output_tuning._main import run
from commons.constants import OPENAI_TERRA_MODEL


run(
    client=OpenAIChatCompletionsClient(OPENAI_TERRA_MODEL),
    print_request=True,  # Switch to False if you do not want to see the request in console
    print_only_content=False,  # Switch to True if you want to see only content from response

    max_completion_tokens=16,  # GPT-5.6 doesn't support `max_tokens`
    reasoning_effort="none"  # otherwise the reasoning tokens use up the whole limit and the content is empty
)
