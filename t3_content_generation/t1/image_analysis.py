import base64

from constants import OPENAI_HOST
from t3_content_generation._openai_client import OpenAIClientT3


# https://developers.openai.com/api/docs/guides/images-vision?format=url&lang=curl
# https://developers.openai.com/api/docs/guides/images-vision?format=base64-encoded

def _encode_image(image_path):
    #TODO:
    # Function to encode image to base64 you can find in documentation
    # https://developers.openai.com/api/docs/guides/images-vision?lang=python&format=base64-encoded#analyze-images
    raise NotImplementedError


def main(model_name: str, img_urls: list[str], request: str = "What's in this image/s?"):
    #TODO:
    # 1. Create OpenAIClientT3 with OPENAI_HOST + /v1/chat/completions as endpoint
    # 2. Prepare img_content:
    #   - iterate through img_urls and generate list of dicts {"type": "image_url", "image_url": {"url": img_url}}
    # 3. Call client with:
    #   - model=model_name
    #   - messages=[{"role": "user","content": [{"type": "text", "text": request}, *img_content]}]
    raise NotImplementedError


main(
    #TODO:
    # - model_name gpt-4o-mini
    # - img_urls:
    #   - https://a-z-animals.com/media/2019/11/Elephant-male-1024x535.jpg
    #   or
    #   - f"data:image/jpeg;base64,{_encode_image('banner.png')}"
)

#TODO:
# In the end load both images (url and base64 encoded 'banner.png'), ask "Generate poem based on images" and se what will happen?
