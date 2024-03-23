import os
import cv2
import numpy as np

import supervision as sv

# Load your brush labelled mask
image = cv2.imread("segm/MEN-Denim-id_00000080-01_7_additional_segm.png")

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Define the color ranges in RGB
# pants are labelled with 211 (light gray) in DeepFashion Multimodal dataset:
# https://github.com/yumingj/DeepFashion-MultiModal?tab=readme-ov-file

# Note: OpenCV uses BGR format, but we will use grayscale values
light_gray_value = 211

# Create mask for pants in grayscale, both upper and lower bounds are single values
mask_pants = cv2.inRange(gray_image, light_gray_value, light_gray_value)

# Apply the pants mask to the grayscale image
mask = cv2.bitwise_and(gray_image, mask_pants)

# find pants contours
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Now, select the contour with max area or iterate through all contours
# For example:
contour = max(contours, key=cv2.contourArea)

# Simplify contour
epsilon = 0.001 * cv2.arcLength(contour, True)
approx = cv2.approxPolyDP(contour, epsilon, True)

# Convert to normalized coordinates
height, width = mask.shape
normalized_contour = approx.reshape(-1, 2) / [width, height]

# Convert contour array to a single line string
formatted_contour = "0 " + ' '.join([f'{num:.8f}' for row in normalized_contour for num in row])
print(formatted_contour)

os.makedirs("segm_gray", exist_ok=True)

file_path = 'segm_gray/labels/MEN-Denim-id_00000080-01_7_additional.txt'

# Open the file and write the contour
with open(file_path, 'w') as file:
    file.write(formatted_contour)

IMAGES_DIRECTORY_PATH = "images"
ANNOTATIONS_DIRECTORY_PATH = "segm_gray/labels"
DATA_YAML_PATH = "train_yolo_pants.yaml"
SAMPLE_SIZE = 1

dataset = sv.DetectionDataset.from_yolo(
    images_directory_path=IMAGES_DIRECTORY_PATH,
    annotations_directory_path=ANNOTATIONS_DIRECTORY_PATH,
    data_yaml_path=DATA_YAML_PATH)

print(len(dataset))

image_names = list(dataset.images.keys())[:SAMPLE_SIZE]

mask_annotator = sv.MaskAnnotator()
box_annotator = sv.BoxAnnotator()

images = []
for image_name in image_names:
    image = dataset.images[image_name]
    annotations = dataset.annotations[image_name]
    labels = [
        dataset.classes[class_id]
        for class_id
        in annotations.class_id]
    annotates_image = mask_annotator.annotate(
        scene=image.copy(),
        detections=annotations)
    annotates_image = box_annotator.annotate(
        scene=annotates_image,
        detections=annotations,
        labels=labels)
    images.append(annotates_image)

SAMPLE_GRID_SIZE = (1, 1)
SAMPLE_PLOT_SIZE = (1, 1)

sv.plot_image(images[0])

