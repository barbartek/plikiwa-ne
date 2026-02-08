import json
import os

def read_readings_from_file(file):
    readings = []

    for line in file:
        line = line.strip()
        if not line:
            continue

        # usuń końcowy przecinek i zamień apostrofy na cudzysłowy
        clean_line = line.rstrip(',').replace("'", '"')

        try:
            readings.append(json.loads(clean_line))
        except json.JSONDecodeError:
            print("❌ Zła linia:", clean_line)

    return readings



def read_readings_from_filepath(filepath):
    with open(filepath, "r", encoding="utf-8") as file:#1. Otwiera plikpath — ścieżka do pliku, np. "./raw-data/2024-12-31.txt""r" — tryb read, czyli tylko do odczytuencoding="utf-8" — mówi Pythonowi, jak interpretować znaki (żeby polskie litery działały poprawnie) Po otwarciu pliku Python tworzy obiekt pliku i przypisuje go do zmiennej file. 
        readings = read_readings_from_file(file)
        return readings
