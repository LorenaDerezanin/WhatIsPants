# choose random image from dataset
import os
import random

from matplotlib import pyplot as plt
from ultralytics import YOLO

model = YOLO("fash.pt")

images_path = 'kaggle/input/colorful-fashion-dataset-for-object-detection/colorful_fashion_dataset_for_object_detection/JPEGImages/'

plt.figure(figsize=(20, 20))
imgs = random.sample(os.listdir(images_path), 6)
c = 1

for img in imgs:
    i = model.predict(source=images_path + img, conf=0.4, save=True, line_thickness=2, project="kaggle/inferences")
    #
    # im = plt.imread(f'predict{c}/' + img)
    # plt.subplot(2, 3, c)
    # plt.axis('off')
    # plt.imshow(im)
    # c += 1
