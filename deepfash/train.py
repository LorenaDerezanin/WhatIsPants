import os
import shutil

import torch
import tqdm
from ultralytics import YOLO

# Check if GPU is working or not

torch_version = torch.__version__
device_name = torch.cuda.get_device_properties(0).name if torch.cuda.is_available() else 'CPU'
print(
    f"Using torch {torch_version} ({device_name})")


# train custom model

model = YOLO("yolov8m-seg.pt")

model.train(data='train_yolo_pants.yaml', epochs=5)



