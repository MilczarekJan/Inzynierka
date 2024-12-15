import cv2
import os

def visualize_yolo8(image_path, label_path):
    # Sprawdzenie czy pliki istnieją
    if not os.path.exists(image_path):
        print(f"Nie znaleziono obrazu: {image_path}")
        return

    if not os.path.exists(label_path):
        print(f"Nie znaleziono pliku etykiet: {label_path}")
        return

    # Wczytanie obrazu
    image = cv2.imread(image_path)
    if image is None:
        print(f"Nie udało się wczytać obrazu: {image_path}")
        return

    height, width, _ = image.shape

    # Wczytanie etykiet YOLOv8
    with open(label_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        elements = line.strip().split()
        if len(elements) != 5:
            print(f"Nieprawidłowy format etykiety: {line}")
            continue

        class_id, x_center, y_center, box_width, box_height = map(float, elements)

        # Konwersja współrzędnych YOLO na współrzędne pikselowe
        x_center_pixel = int(x_center * width)
        y_center_pixel = int(y_center * height)
        box_width_pixel = int(box_width * width)
        box_height_pixel = int(box_height * height)

        x_min = int(x_center_pixel - box_width_pixel / 2)
        y_min = int(y_center_pixel - box_height_pixel / 2)
        x_max = int(x_center_pixel + box_width_pixel / 2)
        y_max = int(y_center_pixel + box_height_pixel / 2)

        # Rysowanie prostokąta na obrazie
        color = (0, 255, 0)  # Zielony kolor prostokąta
        thickness = 2  # Grubość linii prostokąta
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, thickness)

        # Dodanie ID klasy na obrazie
        text = f"ID: {int(class_id)}"
        cv2.putText(image, text, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)

    # Wyświetlenie obrazu
    cv2.imshow('YOLOv8 Visualization', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Przykład użycia
# Podaj ścieżki do obrazu i etykiety poniżej
image_path = '/home/jan/Documents/Inzynierka/yolov8_3klasy_calosc/train/images/20241119_155634_2_jpg.rf.272f11f08b85ca58d1cc2359d57ac9b6.jpg'
label_path = '/home/jan/Documents/Inzynierka/yolov8_3klasy_calosc/train/labels/20241119_155634_2_jpg.rf.272f11f08b85ca58d1cc2359d57ac9b6.txt'
visualize_yolo8(image_path, label_path)
