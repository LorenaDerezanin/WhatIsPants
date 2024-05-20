import os
import cv2
import numpy as np


def mask2contour(mask_filename: str, masks_dir: str, labels_dir: str, pants_mask_color: np.ndarray):
    mask_file_path = os.path.join(masks_dir, mask_filename)
    clothes_mask = cv2.imread(mask_file_path)
    # create a boolean mask where the color of each pixel matches the pants color
    binary_mask = np.all(clothes_mask == pants_mask_color, axis=-1)

    if np.any(binary_mask):
        # convert boolean mask to an integer mask
        pants_mask = binary_mask.astype(np.uint8) * 211
        # find pants contours
        contours, _ = cv2.findContours(pants_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # select contour with max area
        contour = max(contours, key=cv2.contourArea)

        if cv2.contourArea(contour) == 0:
            formatted_contour_label = ""
            print(f"Ignoring 0-area contour found in {mask_filename}")
        else:
            # simplify contour
            epsilon = 0.001 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # convert to normalized coordinates for YOLO
            height, width = pants_mask.shape
            normalized_contour = approx.reshape(-1, 2) / [width, height]

            # convert contour array to single line string
            formatted_contour_label = "0 " + ' '.join([f'{num:.8f}' for row in normalized_contour for num in row])
    else:
        formatted_contour_label = ""

    contour_filename = mask_filename.replace("_segm.png", ".txt")
    contour_file_path = os.path.join(labels_dir, contour_filename)

    # write contour to file
    with open(contour_file_path, 'w') as file:
        file.write(formatted_contour_label)

