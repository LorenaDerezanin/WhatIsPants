# create train and test dirs
import os
import shutil

import tqdm

parent_path = 'kaggle/input/colorful-fashion-dataset-for-object-detection/colorful_fashion_dataset_for_object_detection/'
images_path = 'kaggle/input/colorful-fashion-dataset-for-object-detection/colorful_fashion_dataset_for_object_detection/JPEGImages/'
annotations_path = 'kaggle/input/colorful-fashion-dataset-for-object-detection/colorful_fashion_dataset_for_object_detection/Annotations_txt/'

os.mkdir('kaggle/working/train')
os.mkdir('kaggle/working/train/images')
os.mkdir('kaggle/working/train/labels')

os.mkdir('kaggle/working/test')
os.mkdir('kaggle/working/test/images')
os.mkdir('kaggle/working/test/labels')

train_path = 'kaggle/working/train/'
test_path = 'kaggle/working/test/'

# prepare dataset
train = []
with open(parent_path + 'ImageSets/Main/trainval.txt', 'r') as f:
    for line in f.readlines():
        if line[-1] == '\n':
            line = line[:-1]
        train.append(line)

test = []
with open(parent_path + 'ImageSets/Main/test.txt', 'r') as f:
    for line in f.readlines():
        if line[-1] == '\n':
            line = line[:-1]
        test.append(line)

print(f"Training set length:{len(train)}, Test set length: {len(test)}")


print('Copying Train Data..!!')
for i in tqdm.tqdm(train):
    shutil.copyfile(images_path + i + '.jpg', train_path + 'images/' + i + '.jpg')
    shutil.copyfile(annotations_path + i + '.txt', train_path + 'labels/' + i + '.txt')

print('Copying Test Data..!!')
for i in tqdm.tqdm(test):
    shutil.copyfile(images_path + i + '.jpg', test_path + 'images/' + i + '.jpg')
    shutil.copyfile(annotations_path + i + '.txt', test_path + 'labels/' + i + '.txt')
