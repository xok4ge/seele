from hue import *
import os
import pandas as pd

def processing(image_path):
    image = cv2.imread(image_path)
    try:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([100, 150, 0])
        upper_blue = np.array([140, 255, 255])

        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        Z = image.reshape((-1, 3))
        Z = np.float32(Z)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        K = 2
        _, labels, centers = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        labels = labels.flatten()
        segmented_image = centers[labels].reshape(image.shape).astype(np.uint8)
        final_mask = cv2.bitwise_and(segmented_image, segmented_image, mask=mask)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        nums = len(contours)
        if 0 == nums or nums >= 10:
            # print('sry nt sry')
            raise ValueError
        contour_image = image.copy()
        cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)

    except ValueError as e:
        contour_image, nums = (h(image))

    return [nums, contour_image]


def save_image(image, output_path):
    cv2.imwrite(output_path, image)

def save_results(results, path):
    output_csv_path = os.path.join(path, "out.csv")
    csv_data = []

    for im_name, contour_count, contoured_image in results:
        im_name = im_name.split('/')[-1]
        save_image(contoured_image, os.path.join(path, f'{im_name}_result.jpg'))
        csv_data.append([f"{im_name}.jpg", contour_count])


    df = pd.DataFrame(csv_data, columns=['Image Name', 'Contour Count'])
    df.to_csv(output_csv_path, sep=';', index=False)