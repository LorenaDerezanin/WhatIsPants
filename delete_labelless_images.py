import argparse
import os


def delete_unlabeled_images(images_directory, labels_directory):
    # Gather all image file names without the extension
    image_files = {os.path.splitext(file)[0] for file in os.listdir(images_directory) if file.endswith('.jpg')}

    # Gather all label file names without the extension
    label_files = {os.path.splitext(file)[0] for file in os.listdir(labels_directory) if file.endswith('.txt')}

    # Find images without corresponding label files
    images_without_labels = image_files - label_files

    # Delete these images
    for image_base_name in images_without_labels:
        image_path = os.path.join(images_directory, image_base_name + '.jpg')
        os.remove(image_path)
        print(f"Deleted image: {image_path}")


parser = argparse.ArgumentParser(description="Delete images which don't have a label file")

# Add arguments
parser.add_argument("--images_directory", help="The path to the directory containing the image files.")
parser.add_argument("--labels_directory", help="The path to the directory containing the label files.")

# Parse arguments
args = parser.parse_args()

delete_unlabeled_images(args.images_directory, args.labels_directory)
