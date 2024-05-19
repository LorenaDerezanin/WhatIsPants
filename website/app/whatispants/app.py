import base64
import json
from io import BytesIO

from PIL import Image
from ultralytics import YOLO

model = YOLO("lvis_fash_m_50.pt")


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
        print(event)
        image_data = base64.b64decode(event['body'])
        input_image = Image.open(BytesIO(image_data))
    except Exception as e:
        print(e)
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Could not decode the image"})
        }

    print("Running prediction")

    result = model.predict(input_image)

    print("Prediction done")

    # result[0].show()

    # TODO: use all results, not just the first one
    output_image = Image.fromarray(result[0].plot())

    # Convert to base64
    buffered = BytesIO()
    output_image.save(buffered, format="JPEG")

    base64_encoded_image = str(base64.b64encode(buffered.getvalue()))
    print(f"Returning base64 image: {base64_encoded_image}")
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            "result": base64_encoded_image,
        }),
    }
