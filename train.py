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

parent_path = 'kaggle/input/colorful-fashion-dataset-for-object-detection/colorful_fashion_dataset_for_object_detection/'
images_path = 'kaggle/input/colorful-fashion-dataset-for-object-detection/colorful_fashion_dataset_for_object_detection/JPEGImages/'
annotations_path = 'kaggle/input/colorful-fashion-dataset-for-object-detection/colorful_fashion_dataset_for_object_detection/Annotations_txt/'


# train custom model

model = YOLO("yolov8m.pt")

model.train(data='train_config.yaml', epochs=5)

model.save("fash.pt")

