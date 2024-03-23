import os
import cv2
import numpy as np


# Load your brush labelled mask
image = cv2.imread("segm/MEN-Denim-id_00000080-01_7_additional_segm.png")

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Define the color ranges in RGB
# Note: OpenCV uses BGR format, but we will use grayscale values
black_gray_value = 0
light_gray_value = 211

# Create masks for each color - in grayscale, both upper and lower bounds are single values
mask_0 = cv2.inRange(gray_image, black_gray_value, black_gray_value)
mask_5 = cv2.inRange(gray_image, light_gray_value, light_gray_value)

# Combine masks
combined_mask = cv2.bitwise_or(mask_0, mask_5)

# Apply the combined mask to the grayscale image
result = cv2.bitwise_and(gray_image, gray_image, mask=combined_mask)

os.makedirs("segm_gray", exist_ok=True)

# Save or display the result
cv2.imwrite('segm_gray/MEN-Denim-id_00000080-01_7_additional_segm.png', result)
# cv2.imshow('Result', result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

