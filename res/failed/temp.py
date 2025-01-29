# from ultralytics import YOLO
import cv2
import os
import csv


MODEL_PATH = "yolov8n.pt"
model = YOLO(MODEL_PATH)

def detect_and_draw_contours(image_path, save_path=None):

    img = cv2.imread(image_path)
    results = model(image_path)

    annotated_image = img.copy()
    for box in results[0].boxes:

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        cropped = img[y1:y2, x1:x2]


        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)


        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:

            contour += [x1, y1]
            cv2.drawContours(annotated_image, [contour], -1, (0, 255, 0), 2)

    if save_path:
        cv2.imwrite(save_path, annotated_image)

    return annotated_image, len(results[0].boxes)

def save_results(data, output_csv, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    csv_data = []

    for i, (filename, image, count) in enumerate(data):
        output_path = os.path.join(output_dir, f"output_{i + 1}.jpg")
        cv2.imwrite(output_path, image)
        csv_data.append([filename, count])

    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(csv_data)

def process_images(input_dir, output_csv, output_dir):
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    results = []

    for img_file in image_files:
        img_path = os.path.join(input_dir, img_file)
        annotated_image, obj_count = detect_and_draw_contours(img_path)
        results.append((img_file, annotated_image, obj_count))

    save_results(results, output_csv, output_dir)

if __name__ == "__main__":
    input_images_folder = "temp"
    output_folder = "results"
    output_csv_file = "results.csv"

    process_images(input_images_folder, output_csv_file, output_folder)

# doesnt work cause uninstall library to decrease weight of .exe