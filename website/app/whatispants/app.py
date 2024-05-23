import base64
import json
from io import BytesIO

from PIL import Image, ImageOps

import inference


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e


    # Decode the input_image from base64
    try:
        base64_image_data = event['body']
        image_data = base64.b64decode(base64_image_data)
        raw_image = Image.open(BytesIO(image_data))
        # This rotates images which have orientation information in the EXIF
        # metadata.
        print("Transposing image...")
        input_image = ImageOps.exif_transpose(raw_image)
        print("Transposed image.")
    except Exception as e:
        print(e)
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Could not decode the image"})
        }

    inference_result = inference.infer(input_image)
    output_image = inference_result.annotated_image

    # output_image.show()

    # Convert to base64
    buffered = BytesIO()
    output_image.save(buffered, format="JPEG")

    base64_encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type",
            "Content-Type": "application/json",
        },
        "body": json.dumps({
            "message": "hello world",
            "result": base64_encoded_image,
            "num_pants_found": inference_result.num_pants_found,
        }),
    }
