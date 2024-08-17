import argparse

import torch
from ultralytics import YOLO

# Set up argument parser
parser = argparse.ArgumentParser(description='Train YOLO model on custom dataset.')
parser.add_argument('--epochs', type=int, default=5, help='Number of epochs to train the model.')
parser.add_argument('--model_name', type=str, default="yolov8s-seg.pt", help='Size of the model to train.')
parser.add_argument('--out_dir', type=str, default="", help='Output directory for weights and metrics on trained model')

args = parser.parse_args()

# Check if GPU is working or not
torch_version = torch.__version__
device_name = torch.cuda.get_device_properties(0).name if torch.cuda.is_available() else 'CPU'
print(
    f"Using torch {torch_version} ({device_name})")


# train custom model
print(f"Training on {args.epochs} epochs")
model = YOLO(args.model_name)
model.train(data='train_yolo_pants.yaml', epochs=args.epochs, project=args.out_dir, name=f"{args.model_name}_ep{args.epochs}")
print("done")
