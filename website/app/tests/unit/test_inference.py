import base64
from io import BytesIO

from PIL import Image
from ultralytics import YOLO

from whatispants import inference


model = YOLO("models/lvis_fash_m_50.pt")


def test_inference():
    nwa = Image.open("../../../test_images/spice_girls_2.jpg")
    nwa_annotated = Image.open('../tests/unit/test_data/spice_girls_2_annotated.jpg')

    expected_bytes = BytesIO()
    nwa_annotated.save(expected_bytes, format="JPEG")
    expected_base64_encoded_image = base64.b64encode(expected_bytes.getvalue()).decode("utf-8")

    result = inference.infer(nwa, model)

    actual_bytes = BytesIO()
    result.annotated_image.save(actual_bytes, format="JPEG")
    actual_base64_encoded_image = base64.b64encode(actual_bytes.getvalue()).decode("utf-8")


    assert result.num_pants_found == 3
    # TODO fix this assertion
    # assert actual_base64_encoded_image == expected_base64_encoded_image
