import argparse
import os
import random

import multiprocessing
from concurrent.futures import ThreadPoolExecutor


def delete_file_and_image(file_path, images_directory):
    # Delete the text file
    os.remove(file_path)
    print(f"Deleted text file: {file_path}")

    # Find and delete the corresponding image file
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    image_file_path = os.path.join(images_directory, f"{base_name}.jpg")
    if os.path.exists(image_file_path):
        os.remove(image_file_path)
        print(f"Deleted corresponding image file: {image_file_path}")


def manage_files(directory, images_directory):
    # Lists to store paths of non-empty and empty files
    non_empty_files = []
    empty_files = []

    # Walk through all files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Ensure it's a file
        if os.path.isfile(file_path):
            # Check if the file is non-empty
            if os.stat(file_path).st_size > 0:
                non_empty_files.append(file_path)
            else:
                empty_files.append(file_path)

    # Number of non-empty files
    non_empty_count = len(non_empty_files)

    # Select a random subset of empty files equal to the number of non-empty files
    if len(empty_files) > non_empty_count:
        selected_empty_files = random.sample(empty_files, non_empty_count)
    else:
        selected_empty_files = empty_files

    # Files to delete are those empty files not in the selected subset
    files_to_delete = set(empty_files) - set(selected_empty_files)

    num_cpus = multiprocessing.cpu_count()

    # Using ThreadPoolExecutor to delete files in parallel
    with ThreadPoolExecutor(max_workers=num_cpus) as executor:
        # Submit deletion tasks to the executor
        futures = [executor.submit(delete_file_and_image, file_path, images_directory) for file_path in files_to_delete]

        # Wait for all futures to complete
        for future in futures:
            future.result()

    # Output results
    print(f"Non-empty files: {non_empty_count}")
    print(f"Kept empty files: {len(selected_empty_files)}")
    print(f"Deleted empty files and corresponding images: {len(files_to_delete)}")


parser = argparse.ArgumentParser(description="Keep as many empty labels as there are non-empty and delete the rest "
                                             "along with their corresponding images")

# Add arguments
parser.add_argument("--labels_directory", help="The path to the directory containing the label files.")
parser.add_argument("--images_directory", help="The path to the directory containing the image files.")

# Parse arguments
args = parser.parse_args()

# Specify the directory path here
manage_files(args.labels_directory, args.images_directory)
