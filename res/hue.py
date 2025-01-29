import cv2
import numpy as np


def h(img):
    img = img
    # if img is None:
    #     raise ValueError("Изображение не найдено.")


    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0], None, [180], [0, 180])
    peaks = np.where(hist > 0.1 * hist.max())[0]

    result_img = None
    stru = 0

    for hue in peaks:
        lower = np.array([hue - 10, 50, 50])
        upper = np.array([hue + 10, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        result_img = img.copy()
        cv2.drawContours(result_img, contours, -1, (0, 255, 0), 2)
        stru = len(contours)

    return result_img, stru