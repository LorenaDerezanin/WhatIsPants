import argparse

import torch
from ultralytics import YOLO

# Set up argument parser
parser = argparse.ArgumentParser(description='Train YOLO model on custom dataset.')
parser.add_argument('--epochs', type=int, default=5, help='Number of epochs to train the model.')
parser.add_argument('--size', default='m', help='Yolo segmentation model size, one of (n, s, m, l, x)')
parser.add_argument('--yaml', default='lvis', help='Name of the yaml file to use (without extension)')
args = parser.parse_args()

# Check if GPU is working or not
torch_version = torch.__version__
device_name = torch.cuda.get_device_properties(0).name if torch.cuda.is_available() else 'CPU'
print(
    f"Using torch {torch_version} ({device_name})")


# train custom model
model_name = f"yolov8{args.size}-seg.pt"
print(f"Training on lvis dataset on {args.epochs} epochs based on {model_name}")
model = YOLO(model_name)
name = f"{args.yaml}_{args.size}_{args.epochs}_train"
model.train(data=f"{args.yaml}.yaml", epochs=args.epochs, imgsz=640, name=name)
print("done")
