from PIL import Image
import numpy as np

image = Image.open("../distill/segm/MEN-Denim-id_00000080-01_7_additional_segm.png")

mask = np.array(image)  # shape: [750, 1101]

print("tenks")
