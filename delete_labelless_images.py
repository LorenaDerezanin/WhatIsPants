import os


def delete_unlabeled_images(images_directory, labels_directory):
    image_files = {os.path.splitext(file)[0] for file in os.listdir(images_directory) if file.endswith('.jpg')}
    label_files = {os.path.splitext(file)[0] for file in os.listdir(labels_directory) if file.endswith('.txt')}
    images_without_labels = image_files - label_files

    deleted_files_count = 0
    for image_base_name in images_without_labels:
        image_path = os.path.join(images_directory, image_base_name + '.jpg')
        os.remove(image_path)
        deleted_files_count += 1
    return deleted_files_count
