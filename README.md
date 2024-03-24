# What is Pants?

### setting up conda env `whatispants` in `scratch/yolo_train` dir cause work dir disk quota limited
```bash
conda create --prefix /.../scratch/yolo_train/conda/whatispants python=3.10

conda activate /.../scratch/yolo_train/conda/whatispants   
```

### install requirements in conda env
```bash
pip install -r requirements.txt
```

### TO DO:
[x] random select 2000 png files from segm dir
[x] based on selected segm pngs - select image files from images_fullres dir that match segm png filename