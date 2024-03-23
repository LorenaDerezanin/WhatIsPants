import os
import random
import shutil
from concurrent.futures import ThreadPoolExecutor

WORKDIR = '/data/gpfs-1/users/lode10_c/scratch/yolo_train/distill/'


def copy_file(file, destination):
    shutil.copy2(file, destination)


def main():
    source_dir = WORKDIR + 'images_resized'
    dest_dir = WORKDIR + 'images_subset'
    num_images = 2000
    seed = 1234                             # Seed for reproducibility

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # List all jpg files in the source directory
    all_files = [os.path.join(source_dir, f) for f in os.listdir(source_dir)]

    # Set the seed and select random files
    random.seed(seed)
    selected_files = random.sample(all_files, num_images)

    # Use ThreadPoolExecutor for parallel copying
    with ThreadPoolExecutor(max_workers=32) as executor:
        for file in selected_files:
            executor.submit(copy_file, file, dest_dir)


if __name__ == "__main__":
    main()


