import os
from concurrent.futures import ThreadPoolExecutor
import multiprocessing


def process_file(source_directory, target_directory, labels_of_interest, filename):
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


def subset_labels(source_directory, target_directory):
    # ensure the target directory exists
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # classes in the LVIS dataset that represent pants
    labels_of_interest = {'950', '1039', '1121'}

    # get the number of CPUs available
    num_cpus = multiprocessing.cpu_count()

    # using ThreadPoolExecutor to process files in parallel
    with ThreadPoolExecutor(max_workers=num_cpus) as executor:
        # List only .txt files from the directory
        txt_files = [file for file in os.listdir(source_directory) if file.endswith('.txt')]
        # Submit tasks to the executor
        futures = [executor.submit(process_file, source_directory, target_directory, labels_of_interest, file) for file in txt_files]

        # wait for all futures to complete
        for future in futures:
            future.result()

    print("Files have been processed and labels adjusted successfully.")
