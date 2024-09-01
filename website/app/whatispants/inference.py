from dataclasses import dataclass

from PIL import Image
from ultralytics import YOLO


@dataclass(frozen=True, kw_only=True, eq=True)
class InferenceResult:
    num_pants_found: int
    annotated_image: Image


def infer(input_image: Image, model: YOLO) -> InferenceResult:
    print("Running prediction")
    results = model.predict(input_image)
    print("Prediction done")
    # result[0].show()

    # Somehow there's always only one result, even with multiple pants found
    result = results[0]
    bgr_array = result.plot()
    # For some reason, result.plot() returns a BGR array, so we have to invert
    # it like this. I found this in the docstring of plot.
    rgb_array = bgr_array[..., ::-1]
    output_image = Image.fromarray(rgb_array)

    return InferenceResult(
        num_pants_found=len(result.boxes),
        annotated_image=output_image
    )
