import os
import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor

masks_dir = "datasets/deepfashion/segm"
labels_dir = "datasets/deepfashion/labels"

# pants are marked with this light gray color in the mask files
pants_mask_color = np.array([211, 211, 211])


def mask2contour(mask_filename: str):
    mask_file_path = os.path.join(masks_dir, mask_filename)
    clothes_mask = cv2.imread(mask_file_path)
    # Create a boolean mask where the color of each pixel matches the pants color
    binary_mask = np.all(clothes_mask == pants_mask_color, axis=-1)

    if np.any(binary_mask):
        # Extract the coordinates where the binary mask is true
        # true_pixel_coords = np.argwhere(binary_mask)
        # Log or process the coordinates
        # print(f"Coordinates of true pixels in {mask_filename}: {true_pixel_coords}")

        # Convert the boolean mask to an integer mask
        # Multiply by 211 to change True values to 211, False values will be 0
        pants_mask = binary_mask.astype(np.uint8) * 211
        # find pants contours
        contours, _ = cv2.findContours(pants_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # select contour with max area (or iterate through all contours)
        # example:
        contour = max(contours, key=cv2.contourArea)

        if cv2.contourArea(contour) == 0:
            # This avoids identifying "accidental" grey pixels as pants masks
            # An example of accidental grey pixels can be found at the rightmost edges of the
            # skirt on the mask WOMEN-Blouses_Shirts-id_00001443-01_4_full_segm.png
            # at coordinates x=554 y=513
            formatted_contour_label = ""
            print(f"Ignoring 0-area contour found in {mask_filename}")
        else:
            # simplify contour
            epsilon = 0.001 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # convert to normalized coordinates for yolo
            height, width = pants_mask.shape
            normalized_contour = approx.reshape(-1, 2) / [width, height]

            # convert contour array to single line string
            formatted_contour_label = "0 " + ' '.join([f'{num:.8f}' for row in normalized_contour for num in row])
    else:
        # set empty label if no pants found
        formatted_contour_label = ""
        print(f"No pants labelled in {mask_filename}")

    contour_filename = mask_filename.replace("_segm.png", ".txt")
    contour_file_path = os.path.join(labels_dir, contour_filename)
    # write contour to file
    with open(contour_file_path, 'w') as file:
        file.write(formatted_contour_label)


# load labelled mask pngs
# Use ThreadPoolExecutor for parallel copying
with ThreadPoolExecutor(max_workers=10) as executor:
    for mask_filename in os.listdir(masks_dir):
        executor.submit(mask2contour, mask_filename)