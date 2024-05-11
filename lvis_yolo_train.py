from ultralytics import YOLO

# Load a model
model = YOLO('yolov8m.pt')  # load a pretrained model (recommended for training)

# Train the model
results = model.train(data='lvis.yaml', epochs=50, imgsz=640)