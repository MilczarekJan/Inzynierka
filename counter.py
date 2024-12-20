import os
from collections import Counter

def count_classes_in_txt_files(folder_path):
    class_counter = Counter()
    file_count = 0  # Licznik plików
    
    # Przejdź przez wszystkie pliki w folderze
    for filename in os.listdir(folder_path):
        # Sprawdź, czy plik ma rozszerzenie .txt
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            try:
                file_count += 1  # Zliczanie plików
                # Otwórz plik i zlicz klasy
                with open(file_path, 'r') as file:
                    for line in file:
                        parts = line.strip().split()
                        if parts:  # Upewnij się, że linia nie jest pusta
                            class_id = parts[0]  # Pierwsza liczba w linii to klasa
                            class_counter[class_id] += 1
            except Exception as e:
                print(f"Nie udało się przetworzyć pliku {filename}: {e}")
    
    # Posortuj klasy malejąco według liczby wystąpień
    sorted_classes = sorted(class_counter.items(), key=lambda x: x[1], reverse=True)
    
    # Wyświetl wyniki
    print(f"Liczba przetworzonych plików: {file_count}")
    print("Statystyki klas:")
    for class_id, count in sorted_classes:
        print(f"Klasa {class_id}: {count} wystąpień")
        
# Przykładowe użycie:
folder_path = "/home/jan/Documents/Inzynierka/yolov8_3klasy_calosc_przejrzana/test/labels"  # Podaj ścieżkę do folderu z plikami .txt
count_classes_in_txt_files(folder_path)
