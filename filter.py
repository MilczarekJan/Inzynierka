import os

# Ścieżki do katalogów z etykietami i obrazami
labels_dir = "/home/jan/Documents/Inzynierka/yolov8_3klasy_calosc_przejrzana/valid/labels"
images_dir = "/home/jan/Documents/Inzynierka/yolov8_3klasy_calosc_przejrzana/valid/images"

# Funkcja usuwająca plik, jeśli istnieje
def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Usunięto: {file_path}")
    else:
        print(f"Plik nie istnieje: {file_path}")

# Przeglądanie plików w katalogu z etykietami
for label_file in os.listdir(labels_dir):
    label_path = os.path.join(labels_dir, label_file)

    # Sprawdzamy, czy plik jest plikiem tekstowym
    if os.path.isfile(label_path) and label_file.endswith('.txt'):
        with open(label_path, 'r') as file:
            lines = file.readlines()

        # Jeśli plik ma więcej niż 100 linijek, usuwamy go oraz powiązany plik obrazu
        if len(lines) > 100:
            print(f"Plik {label_file} ma {len(lines)} linijek. Usuwanie...")
            
            # Usuń plik etykiety
            delete_file(label_path)

            # Usuń odpowiadający plik obrazu
            image_file = os.path.splitext(label_file)[0] + ".jpg"
            image_path = os.path.join(images_dir, image_file)
            delete_file(image_path)

print("Proces usuwania zakończony.")
