from autodistill_yolov8 import YOLOv8

DATA_YAML_PATH = f"dataset/data.yaml"

target_model = YOLOv8("yolov8l.pt")
target_model.train(DATA_YAML_PATH, epochs=100)

