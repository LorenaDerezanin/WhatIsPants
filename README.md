# What is Pants?

### add banner

### add description

### setting up conda env `whatispants` in specified `yolo_train` dir 
```bash
conda create -n whatispants python=3.11.9

conda activate whatispants   
```

### install requirements in conda env
```bash
pip install -r requirements.txt --no-cache-dir
```

### Install jupyter lab if not already installed:
```bash
pip install jupyterlab==4.2.0
```

### Create kernel based on conda env for Jupyter notebook
```bash
ipython kernel install --user --name=whatispants 
```

### Start Jupyter lab
```bash
jupyter lab
```
In Jupyter lab open `WhatIsPants.ipynb` and select the `whatispants` kernel
in the top-right corner.

## After training, to run segmentation inference:
Get the trained model file `best.pt` from the training output, and
then run
```bash
yolo segment predict model=best.pt source='test_images/*'
```

## Preparing LVIS
### Copy all images into folder to be subsetted:
```bash
cp -r ~/datasets/lvis/images datasets/lvis_pants/
```

### Subset only pants labels:
```bash
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
```bash
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
```bash
# Training set
python delete_labelless_images.py \
  --images_directory datasets/lvis_pants/images/train2017 \
  --labels_directory datasets/lvis_pants/labels/train2017

# Validation set
python delete_labelless_images.py \
  --images_directory datasets/lvis_pants/images/val2017 \
  --labels_directory datasets/lvis_pants/labels/val2017
```

# Captain's Log
## 2024-05-11: LVIS bad pants labels
We observed that the LVIS dataset contains images with pants where the pants are not annotated.
For example: 000000096670.jpg shows a baseball player, and the labels include a baseball,
a home base, a bat, and a belt, but no pants.


### TO DO:
- [x] run yolo small and xl model (epochs: 5, 20, 50, 100)
- [x] run yolo test run (yolov8l-seg.pt used)
- [x] find bug in mask2contour - pants are found but not there, color issue?
  - faulty file: WOMEN-Blouses_Shirts-id_00001443-01_4_full_segm.png
- [x] random select 2000 png files from segm dir  
- [x] based on selected segm pngs - select image files from images_fullres dir that match segm png filename
