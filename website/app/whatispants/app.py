import base64
import os

import boto3
import json
from io import BytesIO

from PIL import Image, ImageOps
from ultralytics import YOLO

import inference


s3 = boto3.client('s3')


def download_model():
    bucket_name = 'whatispants'
    key = 'lvis_fash_m_50.pt'
    download_path = '/tmp/lvis_fash_m_50.pt'

    if not os.path.exists(download_path):
        s3.download_file(bucket_name, key, download_path)

    return download_path


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

    model_path = download_model()
    model = YOLO(model_path)
    inference_result = inference.infer(input_image, model)
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
