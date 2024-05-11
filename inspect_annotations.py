import supervision as sv


# inspect annotated image
IMAGES_DIRECTORY_PATH = "datasets/lvis_pants/images/train2017"
ANNOTATIONS_DIRECTORY_PATH = "datasets/lvis_pants/labels/train2017"
DATA_YAML_PATH = "lvis.yaml"
SAMPLE_SIZE = 16

dataset = sv.DetectionDataset.from_yolo(
    images_directory_path=IMAGES_DIRECTORY_PATH,
    annotations_directory_path=ANNOTATIONS_DIRECTORY_PATH,
    data_yaml_path=DATA_YAML_PATH)

print(len(dataset))

# Note: this will include images for which no label files exist
# This is not easy to filter out, because there's also many images
# for which there are label files, but contain no labels, so both
# appear as empty annotations.
image_names = list(dataset.images.keys())[:SAMPLE_SIZE]

mask_annotator = sv.MaskAnnotator()
label_annotator = sv.LabelAnnotator()
box_annotator = sv.BoundingBoxAnnotator()

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
        detections=annotations)
    annotates_image = label_annotator.annotate(
        scene=annotates_image,
        detections=annotations,
        labels=labels)
    images.append(annotates_image)

SAMPLE_GRID_SIZE = (4, 4)
SAMPLE_PLOT_SIZE = (16, 16)

sv.plot_images_grid(
    images=images,
    titles=image_names,
    grid_size=SAMPLE_GRID_SIZE,
    size=SAMPLE_PLOT_SIZE)