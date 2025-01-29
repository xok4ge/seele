import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color, measure, morphology
from skimage.filters import threshold_otsu


def process_image(image_path):
    image = io.imread(image_path)
    hsv_image = color.rgb2hsv(image)

    lower_blue = np.array([0.5, 0.5, 0])
    upper_blue = np.array([0.67, 1, 1])

    mask = (hsv_image[..., 0] >= lower_blue[0]) & (hsv_image[..., 0] <= upper_blue[0])
    cleaned_mask = morphology.remove_small_objects(mask, min_size=100)
    labeled_mask = measure.label(cleaned_mask)
    contours = measure.regionprops(labeled_mask)


    num_structures = len(contours)
    contour_image = image.copy()

    for region in contours:
        if region.area > 100:
            minr, minc, maxr, maxc = region.bbox
            r, c = region.centroid
            for i in range(minr, maxr):
                for j in range(minc, maxc):
                    if labeled_mask[i, j] == region.label:
                        contour_image[i, j] = [0, 255, 0]

    output_image_path = 'contour_image.jpg'
    io.imsave(output_image_path, contour_image)
    return contour_image, output_image_path, num_structures

#  deprecated