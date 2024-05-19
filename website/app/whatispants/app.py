import base64
import cv2
import json
from io import BytesIO

from PIL import Image
from yolo_onnx.yolov8_onnx import YOLOv8

_yolov8_detector = YOLOv8("lvis_fash_m_50.onnx")


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

    result = _yolov8_detector(input_image)

    detections = result.json()['detections']
    print(detections)

    # display detections
    img = cv2.imread(input_image)
    for det in detections:
        x0, y0, x1, y1 = det['bbox']
        img = cv2.rectangle(img, (x0, y0), (x1, y1), (255, 0, 0), 4)
    cv2.imwrite('./output.jpg', img)

    # result[0].show()

    # TODO: use all results, not just the first one
    output_image = Image.fromarray(results[0].plot())

    # Convert to base64
    buffered = BytesIO()
    output_image.save(buffered, format="JPEG")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            "result": str(base64.b64encode(buffered.getvalue())),
        }),
    }
