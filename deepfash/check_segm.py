from PIL import Image
import numpy as np

image = Image.open("segm/MEN-Denim-id_00006117-01_4_full_segm.png")

mask = np.array(image)  # shape: [750, 1101]

print("tenks")
