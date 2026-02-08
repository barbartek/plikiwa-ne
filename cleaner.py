import os
import json
from my import read_readings_from_filepath

def clean_data(filepath):
    readings = read_readings_from_filepath(filepath)
    clean_readings = []

    for r in readings:
        # filtrujemy tylko odczyty z czujnika "outside"
        if r.get("name") != "outside":
            continue

        temp = r.get("temp")
        if temp is None:
            continue

        # filtrujemy tylko temperatury w zakresie -100 do 100
        if not (-100 < temp < 100):
            continue

        clean_readings.append(r)

    # zapisujemy dane
    with open(clean_path, "w", encoding="utf-8") as f:
        for r in clean_readings:
            f.write(json.dumps(r) + "\n")
    
    print(f" Odczytano {len(readings)} rekordów z {filepath}")
    print(f" Po filtrze: {len(clean_readings)} rekordów zostanie zapisanych")


