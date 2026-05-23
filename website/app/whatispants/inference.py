from dataclasses import dataclass

from PIL import Image


@dataclass(frozen=True, kw_only=True, eq=True)
class InferenceResult:
    num_pants_found: int
    annotated_image: Image


_model = None


def _get_model():
    global _model
    if _model is None:
        from ultralytics import YOLO
        _model = YOLO("lvis_fash_m_50.pt")
    return _model


def warmup() -> None:
    model = _get_model()
    dummy = Image.new("RGB", (64, 64))
    model.predict(dummy, verbose=False)


def infer(input_image: Image) -> InferenceResult:
    model = _get_model()
    print("Running prediction")
    results = model.predict(input_image)
    print("Prediction done")

    # Somehow there's always only one result, even with multiple pants found
    result = results[0]
    # result.plot() returns a BGR array (per its docstring); invert the last
    # axis to get RGB before handing it to PIL.
    bgr_array = result.plot()
    rgb_array = bgr_array[..., ::-1]
    output_image = Image.fromarray(rgb_array)

    return InferenceResult(
        num_pants_found=len(result.boxes),
        annotated_image=output_image
    )
