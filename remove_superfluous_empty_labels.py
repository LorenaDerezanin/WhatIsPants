import os


def remove_empty_labels(labels_directory, images_directory):
    label_files = [f for f in os.listdir(labels_directory) if f.endswith('.txt')]

    for label_file in label_files:
        label_path = os.path.join(labels_directory, label_file)
        image_file = label_file.replace('.txt', '.jpg')
        image_path = os.path.join(images_directory, image_file)

        # Check if the label file is empty and the corresponding image exists
        if os.path.getsize(label_path) == 0 and os.path.exists(image_path):
            os.remove(label_path)
            print(f"Removed empty label file: {label_path}")
