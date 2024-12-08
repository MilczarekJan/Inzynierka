import os

# Ścieżki do folderów
labels_dir = "/home/jan/Documents/Inzynierka/yolov8_3klasy/test/labels"  # Katalog z plikami etykiet
images_dir = "/home/jan/Documents/Inzynierka/yolov8_3klasy/test/images"  # Katalog z obrazami
output_dir = "/home/jan/Documents/Inzynierka/yolov8_3klasy/test/labels2"  # Katalog dla przekształconych etykiet
os.makedirs(output_dir, exist_ok=True)

# Mapowanie starej klasy na nową klasę
class_mapping = {
    0: 0,  # 0 - układ scalony
    10: 1, # 10 - kondensator
    5: 2  # 5 - opornik
}

# Funkcja przekształcająca etykiety
def filter_and_remap_labels(input_path, output_path, mapping):
    with open(input_path, "r") as infile, open(output_path, "w") as outfile:
        lines = infile.readlines()
        
        # Usuń puste linie (po usunięciu pustych etykiet)
        lines = [line for line in lines if line.strip()]
        
        if not lines:  # Jeśli po usunięciu pustych linii plik jest pusty
            return False  # Zwracamy False, aby wskazać, że plik etykiety jest pusty
        for line in lines:
            parts = line.strip().split()
            if parts:
                class_id = int(parts[0])
                if class_id in mapping:
                    new_class_id = mapping[class_id]
                    outfile.write(f"{new_class_id} {' '.join(parts[1:])}\n")
        return True  # Plik nie jest pusty, więc zapisujemy go

# Iteracja przez pliki etykiet i przekształcenie ich
for label_file in os.listdir(labels_dir):
    if label_file.endswith(".txt"):
        input_file_path = os.path.join(labels_dir, label_file)
        output_file_path = os.path.join(output_dir, label_file)
        
        # Zmień plik etykiety, jeśli jest niepusty
        filter_and_remap_labels(input_file_path, output_file_path, class_mapping)

print(f"Etykiety zostały przekształcone i zapisane w katalogu: {output_dir}")

# Teraz sprawdzimy pliki w katalogu 'labels2' i usuniemy te puste oraz powiązane obrazy
usuniete_etykiety = 0
usuniete_obrazy = 0

for label_file in os.listdir(output_dir):
    if label_file.endswith(".txt"):
        label_file_path = os.path.join(output_dir, label_file)
        
        # Sprawdzamy, czy plik etykiety jest pusty
        with open(label_file_path, "r") as f:
            lines = f.readlines()
        
        # Jeśli plik etykiety jest pusty, usuwamy go oraz powiązany obraz
        if not lines:  # Plik jest pusty
            image_name = label_file.replace(".txt", ".jpg")  # Zakładamy, że obrazy mają rozszerzenie .jpg
            image_path = os.path.join(images_dir, image_name)
            
            # Usuwamy plik etykiety
            if os.path.exists(label_file_path):
                os.remove(label_file_path)
                usuniete_etykiety += 1
                #print(f"Usunięto pusty plik etykiety: {label_file_path}")
            
            # Usuwamy powiązany obraz
            if os.path.exists(image_path):
                os.remove(image_path)
                usuniete_obrazy += 1
                #print(f"Usunięto powiązany obraz: {image_path}")

print("Czyszczenie pustych etykiet i obrazów zakończone.")
print(f"Usuniete etykiety: {usuniete_etykiety}")
print(f"Usuniete obrazy: {usuniete_obrazy}")
