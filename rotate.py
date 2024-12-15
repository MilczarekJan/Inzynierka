import cv2
import os
import numpy as np

def rotate_image_and_labels(image, labels, angle):
    height, width = image.shape[:2]

    # Rotacja obrazu
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1.0)

    if angle in [90, 270]:
        rotated_image = cv2.warpAffine(image, rotation_matrix, (height, width))
    else:
        rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

    # Aktualizacja etykiet
    rotated_labels = []
    for label in labels:
        class_id, x_center, y_center, box_width, box_height = map(float, label)

        # Konwersja współrzędnych do pikseli
        x_center_pixel = x_center * width
        y_center_pixel = y_center * height
        box_width_pixel = box_width * width
        box_height_pixel = box_height * height

        # Rotacja punktów
        points = np.array([[x_center_pixel, y_center_pixel]])
        rotated_points = cv2.transform(np.array([points]), rotation_matrix)[0]
        new_x_center_pixel, new_y_center_pixel = rotated_points[0]

        # Zamiana szerokości i wysokości dla obrotów o 90 i 270 stopni
        if angle in [90, 270]:
            box_width_pixel, box_height_pixel = box_height_pixel, box_width_pixel

        # Konwersja pikseli na współrzędne względne YOLO
        new_x_center = new_x_center_pixel / (height if angle in [90, 270] else width)
        new_y_center = new_y_center_pixel / (width if angle in [90, 270] else height)

        rotated_labels.append(
            [class_id, new_x_center, new_y_center, box_width_pixel / (height if angle in [90, 270] else width), box_height_pixel / (width if angle in [90, 270] else height)]
        )

    return rotated_image, rotated_labels

def save_image_and_labels(image, labels, output_image_path, output_label_path):
    # Zapis obrazu
    cv2.imwrite(output_image_path, image)

    # Zapis etykiet
    with open(output_label_path, 'w') as f:
        for label in labels:
            f.write(" ".join(map(str, label)) + "\n")

def augment_dataset(base_path):
    images_dir = os.path.join(base_path, "images")
    labels_dir = os.path.join(base_path, "labels")

    for image_file in os.listdir(images_dir):
        if not image_file.endswith(".jpg"):
            continue

        image_path = os.path.join(images_dir, image_file)
        label_path = os.path.join(labels_dir, image_file.replace(".jpg", ".txt"))

        if not os.path.exists(label_path):
            print(f"Brak etykiety dla obrazu: {image_file}")
            continue

        # Wczytanie obrazu i etykiet
        image = cv2.imread(image_path)
        with open(label_path, 'r') as f:
            labels = [line.strip().split() for line in f.readlines()]

        # Obrót o 90, 180 i 270 stopni
        for angle in [90, 180, 270]:
            rotated_image, rotated_labels = rotate_image_and_labels(image, labels, angle)

            # Ścieżki do nowych plików
            output_image_name = image_file.replace(".jpg", f"_rot{angle}.jpg")
            output_label_name = image_file.replace(".jpg", f"_rot{angle}.txt")

            output_image_path = os.path.join(images_dir, output_image_name)
            output_label_path = os.path.join(labels_dir, output_label_name)

            # Zapis nowych plików
            save_image_and_labels(rotated_image, rotated_labels, output_image_path, output_label_path)

# Przykład użycia
base_path = "/home/jan/Documents/Inzynierka/yolov8_3klasy_calosc/valid"
augment_dataset(base_path)
