---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.16.2
  kernelspec:
    display_name: WhatIsPants
    language: python
    name: whatispants
---

# What is pants?

```python
Description of the project idea, YOLO used
```

## Setting up Google Colab env

```python
!git clone https://github.com/LorenaDerezanin/WhatIsPants.git
!cd WhatIsPants
```

## Install requirements with pip

```python
!pip install -r requirements.txt --no-cache-dir
```

## Prepare dataset


Deep Fashion MultiModal dataset was used: https://github.com/yumingj/DeepFashion-MultiModal
- from 44,096 jpg images, 12,701 are annotated (classes, segmentation masks and bounding boxes)

```python
# Download image files
!wget --header 'Host: drive.usercontent.google.com' \
  --header 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' \
  --header 'Accept-Language: en-US,en;q=0.5' \
  --header 'Upgrade-Insecure-Requests: 1' \
  --header 'Sec-Fetch-Dest: document' \
  --header 'Sec-Fetch-Mode: navigate' \
  --header 'Sec-Fetch-Site: cross-site' \
  --header 'Sec-Fetch-User: ?1' 'https://drive.usercontent.google.com/download?id=1U2PljA7NE57jcSSzPs21ZurdIPXdYZtN&export=download&authuser=0&confirm=t&uuid=115a0cd6-8ddb-427b-9343-62b76c4d939c&at=APZUnTWiXg4LlG3A7QPA5DmjASX8%3A1715537567680' \
  --output-document 'images.zip'
```

```python
# Download annotation labels
!wget --header 'Host: drive.usercontent.google.com' \
  --header 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' \
  --header 'Accept-Language: en-US,en;q=0.5' \
  --header 'Upgrade-Insecure-Requests: 1' \
  --header 'Sec-Fetch-Dest: document' \
  --header 'Sec-Fetch-Mode: navigate' \
  --header 'Sec-Fetch-Site: cross-site' \
  --header 'Sec-Fetch-User: ?1' 'https://drive.usercontent.google.com/download?id=1r-5t-VgDaAQidZLVgWtguaG7DvMoyUv9&export=download&authuser=0&confirm=t&uuid=b445e6d2-634c-4b59-96c8-4455c6f117a5&at=APZUnTV7OltdPbT0OB1lUK1FhJO8%3A1715537716467' \
  --output-document 'segm.zip'
```

### Convert masks to contours format that YOLO can process

```python
!python mask_2_contour.py
```

## Subset data into training, validation and test sets

Dataset containg all 12,701 labelled images was split into:   
    * train 80%   
    * val 10%  
    * test 10%   

```python
!python subset_training_data.py
```

### Inspect annotations by printing 4x4 set of labelled images

```python
!python inspect_annotations.py
```

## Find and prepare a more diverse dataset

To enrich a very uniform initial data set, it was supplemented with LVIS (Large Vocabulary Instance Segmentation) dataset: https://www.lvisdataset.org/dataset   
to create a more diverse set and prevent overfitting.


### Copy LVIS images into dir to be subsetted

```python
cp -r ~/datasets/lvis/images datasets/lvis_pants/
```

### Subset only pants labels

```python
# Training set 
python subset_lvis_pants_labels.py \
  --source_directory "$HOME/datasets/lvis/labels/train2017/" \
  --target_directory "datasets/lvis_pants/labels/train2017/"

# Validation set
python subset_lvis_pants_labels.py \
  --source_directory "$HOME/datasets/lvis/labels/val2017/" \
  --target_directory "datasets/lvis_pants/labels/val2017/"

# Check number of resulting non-empty labels
# Should be 4462 train and 184 val
find datasets/lvis_pants/labels/train2017 -type f -size +0c | wc -l 
find datasets/lvis_pants/labels/val2017 -type f -size +0c | wc -l
```

### Keep only as many pantsless images as there are pantsful images

```python
# Training set
python remove_superfluous_empty_labels.py \
  --labels_directory datasets/lvis_pants/labels/train2017 \
  --images_directory datasets/lvis_pants/images/train2017
  
# Validation set
python remove_superfluous_empty_labels.py \
  --labels_directory datasets/lvis_pants/labels/val2017 \
  --images_directory datasets/lvis_pants/images/val2017
```

### Remove images which have no corresponding label file

We observed that the LVIS dataset contains images with pants where pants are not annotated. For example: 000000096670.jpg shows a baseball player, and the labels include a baseball, a home base, a bat, and a belt, but no pants.

```python
# Training set
python delete_labelless_images.py \
  --images_directory datasets/lvis_pants/images/train2017 \
  --labels_directory datasets/lvis_pants/labels/train2017

# Validation set
python delete_labelless_images.py \
  --images_directory datasets/lvis_pants/images/val2017 \
  --labels_directory datasets/lvis_pants/labels/val2017
```

### Prepare `train` configuration yaml file 

```python
tensorboard: True

# Train/val/test sets as 1) dir: path/to/imgs, 2) file: path/to/imgs.txt, or 3) list: [path/to/imgs1, path/to/imgs2, ..]
path: /Users/lorenaderezanin/PycharmProjects/WhatIsPants/datasets/lvis_pants # dataset root dir
train: images/train2017 # train images (relative to 'path') 100170 images
val: images/val2017 # val images (relative to 'path') 19809 images

names:
  0: This is pants
```

## Run the training


```python
!python lvis_yolo_train.py 50
```

```python
### 
```
