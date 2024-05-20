import base64
import json
from io import BytesIO

from PIL import Image, ImageOps
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

    print("Running prediction")

    result = model.predict(input_image)

    print("Prediction done")

    # result[0].show()

    # TODO: use all results, not just the first one
    bgr_array = result[0].plot()
    # For some reason, result.plot() returns a BGR array, so we have to invert
    # it like this. I found this in the docstring of plot.
    rgb_array = bgr_array[..., ::-1]
    output_image = Image.fromarray(rgb_array)

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
        }),
    }
