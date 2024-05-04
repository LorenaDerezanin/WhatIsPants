import os
import random
import shutil
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

WORKDIR = '.'
# 12702 is the full set of available lables
subset_size = 12702


def copy_file(file, destination):
    shutil.copy2(file, destination)


def check_and_copy(source_label_file_path, source_image_file_path, target_labels_dir, target_images_dir):
    try:
        with Image.open(source_image_file_path) as img:
            if img.size != (750, 1101):
                print(f"Skipping {source_image_file_path} due to resolution mismatch: {img.size}")
                return
    except IOError:
        print(f"Failed to open image {source_image_file_path}")
        return

    # If resolution is correct, proceed to copy files
    copy_file(source_label_file_path, target_labels_dir)
    copy_file(source_image_file_path, target_images_dir)


labels_source_dir = os.path.join(WORKDIR, 'labels')
images_source_dir = os.path.join(WORKDIR, 'images_fullres')

train_dir = os.path.join(WORKDIR, 'train')
val_dir = os.path.join(WORKDIR, 'val')
test_dir = os.path.join(WORKDIR, 'test')

if os.path.exists(train_dir):
    shutil.rmtree(train_dir)
os.makedirs(os.path.join(train_dir, 'images'))
os.makedirs(os.path.join(train_dir, 'labels'))

if os.path.exists(val_dir):
    shutil.rmtree(val_dir)
os.makedirs(os.path.join(val_dir, 'images'))
os.makedirs(os.path.join(val_dir, 'labels'))

if os.path.exists(test_dir):
    shutil.rmtree(test_dir)
os.makedirs(os.path.join(test_dir, 'images'))
os.makedirs(os.path.join(test_dir, 'labels'))


num_train_labels = 0.8 * subset_size
num_val_labels = 0.1 * subset_size
num_test_labels = 0.1 * subset_size


# List all label files in the source directory
all_files = [os.path.join(labels_source_dir, f) for f in os.listdir(labels_source_dir)]

# Set the seed and select random files
seed = 1234          # seed for reproducibility
random.seed(seed)
selected_files = random.sample(all_files, subset_size)

# Use ThreadPoolExecutor for parallel label and image matching and copying to target dirs
with ThreadPoolExecutor(max_workers=10) as executor:
    for index, source_label_file_path in enumerate(selected_files):
        image_filename = os.path.basename(source_label_file_path).replace(".txt", ".jpg")
        source_image_file_path = os.path.join(images_source_dir, image_filename)

        if index < num_train_labels:
            target_dir = train_dir
        elif index < num_train_labels + num_val_labels:
            target_dir = val_dir
        else:
            target_dir = test_dir

        target_labels_dir = os.path.join(target_dir, 'labels')
        target_images_dir = os.path.join(target_dir, 'images')

        # Submit the task to executor
        executor.submit(check_and_copy, source_label_file_path, source_image_file_path, target_labels_dir,
                        target_images_dir)
