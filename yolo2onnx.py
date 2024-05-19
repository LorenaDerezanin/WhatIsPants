from ultralytics import YOLO
import argparse

argparser = argparse.ArgumentParser(description='Export YOLO model to ONNX')
argparser.add_argument('-m', '--model', help='Model path', required=True)
args = argparser.parse_args()

# load model
model = YOLO(args.model)  # replace with your custom model pt file

# export model
model.export(format="onnx", dynamic=True)
