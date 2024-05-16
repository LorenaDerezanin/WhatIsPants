import torch
from ultralytics import YOLO


def train_yolo_model(epochs=5, size='m', yaml='lvis'):
    # check if GPU is available
    torch_version = torch.__version__
    device_name = torch.cuda.get_device_properties(0).name if torch.cuda.is_available() else 'CPU'
    print(f"Using torch {torch_version} ({device_name})")


# train custom model
    model_name = f"yolov8{size}-seg.pt"
    print(f"Training on {yaml} dataset for {epochs} epochs using {model_name}")
    model = YOLO(model_name)
    name = f"{yaml}_{size}_{epochs}_train"
    model.train(data=f"{yaml}.yaml", epochs=epochs, imgsz=640, name=name)
    print("Training done!")
