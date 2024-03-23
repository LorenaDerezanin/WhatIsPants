import os
import cv2
import numpy as np

masks_dir = "segm"

# pants are marked with this light gray color in the mask files
pants_mask_color = np.array([211, 211, 211])

# load labelled mask pngs
for mask_filename in os.listdir(masks_dir):
    mask_file_path = os.path.join(masks_dir, mask_filename)
    clothes_mask = cv2.imread(mask_file_path)

    # Create a boolean mask where the color of each pixel matches the pants color
    binary_mask = np.all(clothes_mask == pants_mask_color, axis=-1)

    # initialize empty label if no pants found
    formatted_contour_label = ""
    if np.any(binary_mask):
        # Convert the boolean mask to an integer mask
        # Multiply by 211 to change True values to 211, False values will be 0
        pants_mask = binary_mask.astype(np.uint8) * 211
        # find pants contours
        contours, _ = cv2.findContours(pants_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # select contour with max area (or iterate through all contours)
        # example:
        contour = max(contours, key=cv2.contourArea)

        # simplify contour
        epsilon = 0.001 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # convert to normalized coordinates for yolo
        height, width = pants_mask.shape
        normalized_contour = approx.reshape(-1, 2) / [width, height]

        # convert contour array to single line string
        formatted_contour_label = "0 " + ' '.join([f'{num:.8f}' for row in normalized_contour for num in row])

    contour_filename = mask_filename.replace("_segm.png", ".txt")
    contour_file_path = os.path.join("labels", contour_filename)

    # write contour to file
    with open(contour_file_path, 'w') as file:
        file.write(formatted_contour_label)



