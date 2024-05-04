# What is Pants?

### add banner

### add description

### setting up conda env `whatispants` in specified `yolo_train` dir 
```bash
conda create --prefix /.../yolo_train/conda/whatispants python=3.10

conda activate /.../yolo_train/conda/whatispants   
```

### install requirements in conda env
```bash
pip install -r requirements.txt
```

### TO DO:
- [x] find bug in mask2contour - pants are found but not there, color issue?
  - faulty file: WOMEN-Blouses_Shirts-id_00001443-01_4_full_segm.png
- [x] random select 2000 png files from segm dir  
- [x] based on selected segm pngs - select image files from images_fullres dir that match segm png filename