import os
import random
import shutil
from concurrent.futures import ThreadPoolExecutor


def copy_file(file, destination):
    shutil.copy2(file, destination)


def set_up_target_dirs(base_dir: str) -> (str, str, str):
    """
    Creates a train, val, and test dir inside base_dir, with an images and labels subdir in each of them.
    The directories are removed and recreated for repeatability.
    :param base_dir:
    :return: The train, val and test directory paths (relative to base_dir).
    """
    train_dir = os.path.join(base_dir, 'train')
    val_dir = os.path.join(base_dir, 'val')
    test_dir = os.path.join(base_dir, 'test')

    for dir_path in [train_dir, val_dir, test_dir]:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs(os.path.join(dir_path, 'images'))
        os.makedirs(os.path.join(dir_path, 'labels'))

    return train_dir, val_dir, test_dir


# set the seed and select random files
def copy_files_in_parallel(
        labels_source_dir: str,
        images_source_dir: str,
        train_dir: str,
        val_dir: str,
        test_dir: str,
        num_train_labels: int,
        num_val_labels: int,
        subset_size: int,
        seed=1234
):
    # list all label files in the source directory
    all_files = [os.path.join(labels_source_dir, f) for f in os.listdir(labels_source_dir)]

    random.seed(seed)
    selected_files = random.sample(all_files, subset_size)

    # Get the number of available CPUs
    num_cpus = os.cpu_count()

    with ThreadPoolExecutor(max_workers=num_cpus) as executor:
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

            executor.submit(copy_file, source_label_file_path, target_labels_dir)
            executor.submit(copy_file, source_image_file_path, target_images_dir)
