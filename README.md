# What is Pants?

### setting up conda env `whatispants` in `scratch/yolo_train` dir cause work dir disk quota limited
```bash
conda create --prefix /data/gpfs-1/users/lode10_c/scratch/yolo_train/conda/whatispants python=3.10

conda activate /data/gpfs-1/users/lode10_c/scratch/yolo_train/conda/whatispants   
```

### install requirements in conda env
```bash
pip install -r requirements.txt
```

### TO DO:
* random select 400 png files from segm dir
* based on selected segm pngs - select image files from images_fullres dir that match segm png filename