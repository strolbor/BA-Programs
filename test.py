import os

ordner_pfad = 'sorted_by_SAT'

if not os.path.exists(ordner_pfad):
    print(f"Der Ordner '{ordner_pfad}' existiert nicht.")
else:
    dateien = os.listdir(ordner_pfad)
    if not dateien:
        print(f"Der Ordner '{ordner_pfad}' ist leer.")
    else:
        csv_dateien = [datei for datei in dateien if datei.endswith('-all.csv')]
        if not csv_dateien:
            print(f"Keine CSV-Dateien mit dem Muster '-all.csv' gefunden.")
        else:
            print("Gefundene CSV-Dateien:")
            for csv_datei in csv_dateien:
                print(os.path.join(ordner_pfad, csv_datei))
