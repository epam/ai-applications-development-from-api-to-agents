from t2_llms_output_tuning._clients.openai_responses_client import OpenAIResponsesClient
from t2_llms_output_tuning._main import run
from commons.constants import OPENAI_TERRA_MODEL


run(
    client=OpenAIResponsesClient(OPENAI_TERRA_MODEL),
    print_request=True, # Switch to False if you do not want to see the request in console
    print_only_content=False, # Switch to True if you want to see only content from response

    max_output_tokens=16
)