import os
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

import argparse


# Function to process each file
def process_file(filename):
    file_path = os.path.join(source_directory, filename)
    output_path = os.path.join(target_directory, filename)
    with open(file_path, 'r') as file:
        lines = file.readlines()
    with open(output_path, 'w') as output_file:
        for line in lines:
            parts = line.strip().split()
            if parts[0] in labels_of_interest:
                parts[0] = '0'  # Change the label to '0'
                output_file.write(' '.join(parts) + '\n')


parser = argparse.ArgumentParser(description="Subset pants labels")

# Add arguments
parser.add_argument("--source_directory", help="The path to the source directory containing the label files.")
parser.add_argument("--target_directory", help="The path to the target directory where filtered files will be stored.")

# Parse arguments
args = parser.parse_args()

# Access the directory paths
source_directory = args.source_directory
target_directory = args.target_directory


# Ensure the target directory exists
if not os.path.exists(target_directory):
    os.makedirs(target_directory)


# Classes in the LVIS dataset that represent pants
# 950: short pants/shorts/shorts clothing/trunks/trunks clothing
# 1039: sweat pants
# 1121: trousers/pants/pants clothing
labels_of_interest = {'950', '1039', '1121'}

# Get the number of CPUs available
num_cpus = multiprocessing.cpu_count()

# Using ThreadPoolExecutor to process files in parallel
with ThreadPoolExecutor(max_workers=num_cpus) as executor:
    # List only .txt files from the directory
    txt_files = [file for file in os.listdir(source_directory) if file.endswith('.txt')]
    # Submit tasks to the executor
    futures = [executor.submit(process_file, file) for file in txt_files]

    # Wait for all futures to complete
    for future in futures:
        future.result()

print("Files have been processed and labels adjusted successfully.")
