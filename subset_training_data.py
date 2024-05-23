import os
import random
import shutil
from concurrent.futures import ThreadPoolExecutor


def copy_file(file, destination):
    shutil.copy2(file, destination)


def setup_dirs(workdir, subset_size):
    basedir = os.path.join(workdir, 'datasets', 'deepfashion')
    labels_source_dir = os.path.join(basedir, 'labels')
    images_source_dir = os.path.join(basedir, 'images_fullres')

    targetdir = 'deepfash'
    train_dir = os.path.join(targetdir, 'train')
    val_dir = os.path.join(targetdir, 'val')
    test_dir = os.path.join(targetdir, 'test')

    for dir_path in [train_dir, val_dir, test_dir]:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
            os.makedirs(os.path.join(dir_path, 'images'))
            os.makedirs(os.path.join(dir_path, 'labels'))

    num_train_labels = 0.8 * subset_size
    num_val_labels = 0.1 * subset_size
    num_test_labels = 0.1 * subset_size

    return labels_source_dir, images_source_dir, train_dir, val_dir, test_dir, num_train_labels, num_val_labels, num_test_labels


# set the seed and select random files
def copy_files_in_parallel(labels_source_dir, images_source_dir, train_dir, val_dir, test_dir, num_train_labels,
                           num_val_labels, num_test_labels, subset_size, seed=1234):
    #list all label files in the source directory
    all_files = [os.path.join(labels_source_dir, f) for f in os.listdir(labels_source_dir)]

    random.seed(seed)
    selected_files = random.sample(all_files, subset_size)

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

            executor.submit(copy_file, source_label_file_path, target_labels_dir)
            executor.submit(copy_file, source_image_file_path, target_images_dir)