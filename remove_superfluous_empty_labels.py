import os
import random


def count_non_empty_labels(labels_directory):
    non_empty_count = 0
    label_files = [f for f in os.listdir(labels_directory) if f.endswith('.txt')]
    for file in label_files:
        file_path = os.path.join(labels_directory, file)
        if os.path.getsize(file_path) > 0:
            non_empty_count += 1
    return non_empty_count


def remove_empty_labels(labels_directory, images_direcgstory):
    label_files = [f for f in os.listdir(labels_directory) if f.endswith('.txt')]

    # count the number of non-empty label files
    non_empty_count = count_non_empty_labels(labels_directory)

    # filter out empty label files
    empty_label_files = [f for f in label_files if os.path.getsize(os.path.join(labels_directory, f)) == 0]

    # randomly select empty labels to keep
    labels_to_keep = random.sample(empty_label_files, non_empty_count) \
        if len(empty_label_files) > non_empty_count else empty_label_files

    for label_file in label_files:
        label_path = os.path.join(labels_directory, label_file)
        image_file = label_file.replace('.txt', '.jpg')
        image_path = os.path.join(images_directory, image_file)

        # check if label file is empty and corresponding image exists
        if os.path.getsize(label_path) == 0:
            if label_file not in labels_to_keep:
                os.remove(label_path)
                print(f"Removed empty label file: {label_path}")
            elif not os.path.exists(image_path):
                os.remove(label_path)
                print(f"Removed empty label file without corresponding image: {label_path}")
