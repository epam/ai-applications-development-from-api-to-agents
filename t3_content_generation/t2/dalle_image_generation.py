from constants import OPENAI_HOST
from t3_content_generation._openai_client import OpenAIClientT3


class Size:
    """
    The size of the generated image.
    """
    square: str = '1024x1024'
    height_rectangle: str = '1024x1792'
    width_rectangle: str = '1792x1024'


class Style:
    """
    The style of the generated image. Must be one of vivid or natural.
     - Vivid causes the model to lean towards generating hyper-real and dramatic images.
     - Natural causes the model to produce more natural, less hyper-real looking images.
    """
    natural: str = "natural"
    vivid: str = "vivid"


class Quality:
    """
    The quality of the image that will be generated.
     - ‘hd’ creates images with finer details and greater consistency across the image.
    """
    standard: str = "standard"
    hd: str = "hd"


# https://developers.openai.com/api/reference/resources/images/methods/generate
# Request:
# curl https://api.openai.com/v1/images/generations \
#   -H "Content-Type: application/json" \
#   -H "Authorization: Bearer $OPENAI_API_KEY" \
#   -d '{
#     "model": "dall-e-3",
#     "prompt": "smiling catdog",
#     "size": "1024x1024",
#     "style": "natural",
#     "quality": "standard"
#   }'

def main(model_name: str, request: str, size: Size = Size.square, style: Style = Style.natural, quality: Quality = Quality.standard):
    #TODO:
    # 1. Create OpenAIClientT3 with OPENAI_HOST + /v1/images/generations as endpoint
    # 2. Call client with:
    #   - model=model_name
    #   - prompt=request
    #   - size=size
    #   - style=style
    #   - quality=quality
    raise NotImplementedError


main(
    #TODO:
    # - model_name dall-e-3
    # - request="Smiling catdog"
    # Play with configurations (size, style, quality)
)

