import supervision as sv


def load_and_annotate_images(images_directory_path, annotations_directory_path, data_yaml_path, sample_size=16):
    # read in the dataset
    dataset = sv.DetectionDataset.from_yolo(
        images_directory_path=images_directory_path,
        annotations_directory_path=annotations_directory_path,
        data_yaml_path=data_yaml_path
    )

    # print the number of images in the dataset
    print(f"Number of images in dataset: {len(dataset)}")

    # Note: this will include images for which no label files exist
    # This is not easy to filter out, because there's also many images
    # for which there are label files, but contain no labels, so both
    # appear as empty annotations.
    image_names = list(dataset.images.keys())[:sample_size]

    # initialize annotators
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

    return images, image_names


def plot_image_grid(images, titles, grid_size=(4, 4), size=(16, 16)):
    sv.plot_images_grid(
        images=images,
        titles=titles,
        grid_size=grid_size,
        size=size
    )

