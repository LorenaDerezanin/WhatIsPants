import base64
import json
from io import BytesIO

from PIL import Image, ImageOps

import inference


# CORS headers are NOT added here. The Lambda Function URL has its own CORS
# config (see FunctionUrlConfig.Cors in template.yaml) and adds them itself.
# If you add Access-Control-Allow-* headers here too, browsers will see them
# duplicated in the response and reject the request with "Failed to fetch".
_JSON_HEADERS = {"Content-Type": "application/json"}


def _is_warmup_signal(body: str, is_base64_encoded: bool) -> bool:
    """True if the request body is the warmup ping.

    Function URL passes the body plain for text content-types and
    base64-encoded for binary content-types; check both forms. Only attempt to
    decode when the body is short enough to plausibly be 'warmup' — we don't
    want to base64-decode an entire JPEG just to compare it.
    """
    if body.strip().lower() == 'warmup':
        return True
    if is_base64_encoded and len(body) <= 16:
        try:
            decoded = base64.b64decode(body, validate=True).decode('utf-8')
            return decoded.strip().lower() == 'warmup'
        except Exception:
            return False
    return False


def lambda_handler(event, context):
    """Lambda handler for the whatispants Function URL.

    `event` follows the Lambda Function URL payload format v2.0:
    https://docs.aws.amazon.com/lambda/latest/dg/urls-invocation.html#urls-payloads

    `context` is the standard Lambda context:
    https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    The body is either the literal string ``"warmup"`` (page-load warmup ping)
    or a base64-encoded JPEG to run inference on. Both forms work whether
    Function URL passed the body plain or base64-encoded for transit, because
    `base64.b64decode` on a base64-encoded JPEG string yields the JPEG bytes
    regardless.
    """
    body = event.get('body') or ''

    if _is_warmup_signal(body, event.get('isBase64Encoded', False)):
        inference.warmup()
        return {
            "statusCode": 200,
            "headers": _JSON_HEADERS,
            "body": json.dumps({"status": "warm"}),
        }

    try:
        image_data = base64.b64decode(body)
        raw_image = Image.open(BytesIO(image_data))
        print("Transposing image...")
        input_image = ImageOps.exif_transpose(raw_image)
        print("Transposed image.")
    except Exception as e:
        print(e)
        return {
            "statusCode": 400,
            "headers": _JSON_HEADERS,
            "body": json.dumps({"error": "Could not decode the image"}),
        }

    inference_result = inference.infer(input_image)
    output_image = inference_result.annotated_image

    buffered = BytesIO()
    output_image.save(buffered, format="JPEG")

    base64_encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return {
        "statusCode": 200,
        "headers": _JSON_HEADERS,
        "body": json.dumps({
            "result": base64_encoded_image,
            "num_pants_found": inference_result.num_pants_found,
        }),
    }
