import base64
from datetime import datetime

from commons.constants import OPENAI_HOST
from t3_content_generation._openai_client import OpenAIClientT3


# https://platform.openai.com/docs/guides/image-generation?image-generation-model=gpt-image-1&api=image&multi-turn=imageid
# ---
# Request:
# curl -X POST "https://api.openai.com/v1/images/generations" \
#     -H "Authorization: Bearer $OPENAI_API_KEY" \
#     -H "Content-type: application/json" \
#     -d '{
#         "model": "gpt-image-1",
#         "prompt": "smiling catdog."
#     }'
# Response:
# {
#   "created": 1699900000,
#   "data": [
#     {
#       "b64_json": Qt0n6ArYAEABGOhEoYgVAJFdt8jM79uW2DO...,
#     }
#   ]
# }


def main(model_name: str, request: str, **kwargs):
    client = OpenAIClientT3(
        endpoint=OPENAI_HOST+"/v1/images/generations",
    )

    response = client.call(
        model=model_name,
        prompt=request,
        **kwargs
    )
    image_base64 = response["data"][0]["b64_json"]

    image_bytes = base64.b64decode(image_base64)
    filename= f"{datetime.now()}.png"
    with open(filename, "wb") as f:
        f.write(image_bytes)

    print(f"Image saved as {filename}")


main(
    model_name="gpt-image-1",
    request="smiling catdog"
)
