import base64

from constants import OPENAI_HOST
from t3_content_generation._openai_client import OpenAIClientT3


def _encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def main(model_name: str, img_urls: list[str], request: str = "What's in this image/s?"):
    client = OpenAIClientT3(OPENAI_HOST + "/v1/chat/completions")

    img_content = [
        {
            "type": "image_url",
            "image_url": {
                "url": img_url,
            }
        }
        for img_url in img_urls
    ]

    client.call(
        model=model_name,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": request
                },
                *img_content,
            ],
        }],
    )


main(
    model_name="gpt-5.2",
    img_urls=[
        'https://a-z-animals.com/media/2019/11/Elephant-male-1024x535.jpg',
        f"data:image/jpeg;base64,{_encode_image('logo.png')}"
    ],
    request="Poem based on images",
)
