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
        # if pants are occluded and contour interrupted, choose the largest area for the pants label
        contour = max(contours, key=cv2.contourArea)

        # some images have antialiasing artifacts in the same color as the pants mask
        # this filters them out
        if cv2.contourArea(contour) == 0:
            formatted_contour_label = ""
            print(f"Ignoring 0-area contour found in {mask_filename}")
        else:
            # simplify contour
            epsilon = 0.001 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # convert to normalized coordinates for YOLO
            # E.g. if the input image is 400x600, the x, y coordinates of
            # the contours will be something like x=200, y=400, etc.
            # Normalization converts them to x=0.5, y=0.66 (i.e. from the range of x=[1,400], y=[1,600]
            # to the range of x=[0.0, 1.0], y=[0.0, 1.0])
            height, width = pants_mask.shape
            normalized_contour = approx.reshape(-1, 2) / [width, height]

            # normalized_contour is a list of x, y tuples, e.g. [(0.4, 0.2), (0.41, 0.22)]
            # Convert it to a flat list of strings with 8 decimals, e.g.
            # ["0.4000000", "0.2000000", "0.41000000", "0.22000000"]
            xy_coordinates = [
                # Print each x or y coordinate with 8 decimals
                f'{coordinate:.8f}'
                for xy_tuple in normalized_contour
                for coordinate in xy_tuple
            ]
            # convert contour array to a single line string, prepending "0 " as the class index
            # 0 is the index (number) of the pants class - our only class
            # E.g. "0 0.4000000 0.2000000 0.41000000 0.22000000"
            coordinates_string = ' '.join(xy_coordinates)
            formatted_contour_label = "0 " + coordinates_string
    else:
        formatted_contour_label = ""

    contour_filename = mask_filename.replace("_segm.png", ".txt")
    contour_file_path = os.path.join(labels_dir, contour_filename)

    # write contour to file
    with open(contour_file_path, 'w') as file:
        file.write(formatted_contour_label)
