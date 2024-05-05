import argparse

import torch
from ultralytics import YOLO

# Set up argument parser
parser = argparse.ArgumentParser(description='Train YOLO model on custom dataset.')
parser.add_argument('--epochs', type=int, default=5, help='Number of epochs to train the model.')
args = parser.parse_args()

# Check if GPU is working or not
torch_version = torch.__version__
device_name = torch.cuda.get_device_properties(0).name if torch.cuda.is_available() else 'CPU'
print(
    f"Using torch {torch_version} ({device_name})")


# train custom model
print(f"Training on {args.epochs} epochs")
model = YOLO("yolov8x-seg.pt")
model.train(data='train_yolo_pants.yaml', epochs=args.epochs)
print("done")
