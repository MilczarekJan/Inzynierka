import cv2
import os
import numpy as np

def add_noise(image, noise_level=0.01):
    """Dodaje subtelny szum gaussowski do obrazu."""
    noise = np.random.normal(0, 255 * noise_level, image.shape).astype(np.float32)
    noisy_image = np.clip(image.astype(np.float32) + noise, 0, 255).astype(np.uint8)
    return noisy_image

def apply_gaussian_blur(image, kernel_size=5):
    """Nakłada rozmycie Gaussa na obraz."""
    blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    return blurred_image

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

        # Dodanie szumu
        noisy_image = add_noise(image, noise_level=0.05)
        noisy_image_name = image_file.replace(".jpg", "_noisy.jpg")
        noisy_label_name = image_file.replace(".jpg", "_noisy.txt")
        noisy_image_path = os.path.join(images_dir, noisy_image_name)
        noisy_label_path = os.path.join(labels_dir, noisy_label_name)
        save_image_and_labels(noisy_image, labels, noisy_image_path, noisy_label_path)

        # Rozmycie Gaussa
        blurred_image = apply_gaussian_blur(image)
        blurred_image_name = image_file.replace(".jpg", "_blurred.jpg")
        blurred_label_name = image_file.replace(".jpg", "_blurred.txt")
        blurred_image_path = os.path.join(images_dir, blurred_image_name)
        blurred_label_path = os.path.join(labels_dir, blurred_label_name)
        save_image_and_labels(blurred_image, labels, blurred_image_path, blurred_label_path)

# Przykład użycia
base_path = "/home/jan/Documents/Inzynierka/yolov8_3klasy_calosc/valid"
augment_dataset(base_path)
