import csv
import numpy as np
import cv2
# from scipy.ndimage import binary_closing, binary_opening, generate_binary_structure, label
import os


# Преобразование изображения в HSV и маскирование
def preprocess_image(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([100, 150, 50])  # low
    upper_blue = np.array([140, 255, 255])  # high

    mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

    # Улучшенная морфология: больше итераций и структур
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=3)
    mask_cleaned = cv2.morphologyEx(mask_cleaned, cv2.MORPH_OPEN, kernel, iterations=2)

    # Применение Gaussian Blur для сглаживания и сохранения более точных границ
    mask_cleaned = cv2.GaussianBlur(mask_cleaned, (3, 3), 0)

    return mask_cleaned
# Обнаружение контуров с использованием cv2.findContours
def detect_contours(mask):
    # Преобразуем маску обратно в формат 8-битного изображения
    mask = np.uint8(mask * 255)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

# Рисование только границ контуров на изображении
def draw_contours(image, contours):
    contoured_image = image.copy()
    # Рисуем только контуры (тонкими линиями)
    cv2.drawContours(contoured_image, contours, -1, (0, 0, 255), thickness=1)
    return contoured_image


def save_image(image, output_path):
    cv2.imwrite(output_path, image)


# Загрузка и обработка изображения
def load_image(img_path):
    im_name = str(img_path).split("/")[-1]
    image = cv2.imread(img_path)

    if image is None:
        raise ValueError(f"Не удалось загрузить изображение из пути: {img_path}")

    mask_cleaned = preprocess_image(image)

    contours = detect_contours(mask_cleaned)

    contoured_image = draw_contours(image, contours)

    return [im_name, len(contours), contoured_image]

# Сохранение результатов в CSV и файл
def save_results(lst, path):
    csvv= []
    for i in lst:
        i[0] = i[0].split('.')[0]
        # Сохранение обработанных изображений
        save_image(i[-1], f'{path}/{i[0]}_result.jpg')
        csvv.append([i[0], i[1]])
    with open(f"{path}/out.csv", mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for i in csvv:
            writer.writerow([f"{i[0]}.jpg", i[1]])


# image_path = "templates/template_in_2.jpg"
# output_csv = "output.csv"
# dest = "templates"
#
# result = load_image(image_path)
#
# save_results([result], output_csv, dest)