import os
import random
import shutil
from concurrent.futures import ThreadPoolExecutor

WORKDIR = '.'


def copy_file(file, destination):
    shutil.copy2(file, destination)


segm_source_dir = os.path.join(WORKDIR, '../distill/segm')
dest_dir = os.path.join(WORKDIR, 'images')
num_images = 200
seed = 1234                             # seed for reproducibility

os.makedirs(dest_dir, exist_ok=True)

# List all jpg files in the source directory
all_files = [os.path.join(segm_source_dir, f) for f in os.listdir(segm_source_dir)]

# Set the seed and select random files
random.seed(seed)
selected_files = random.sample(all_files, num_images)

# Use ThreadPoolExecutor for parallel copying
with ThreadPoolExecutor(max_workers=32) as executor:
    for file in selected_files:
        executor.submit(copy_file, file, dest_dir)



