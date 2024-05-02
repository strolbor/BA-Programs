import csv
import os
from datetime import datetime

# Funktion zur Extraktion der Feature-Modell-Version basierend auf dem Datum
def get_fm_version(date):
    versions = {
        datetime(2002, 1, 1): 'v2.5.45',
        datetime(2003, 1, 1): 'v2.5.54',
        datetime(2004, 1, 1): 'v2.6.1',
        datetime(2005, 1, 1): 'v2.6.11',
        datetime(2006, 1, 1): 'v2.6.15',
        datetime(2007, 1, 1): 'v2.6.20',
        datetime(2008, 1, 1): 'v2.6.24',
        datetime(2009, 1, 1): 'v2.6.29',
        datetime(2010, 1, 1): 'v2.6.33',
        datetime(2011, 1, 1): 'v2.6.37',
        datetime(2012, 1, 1): 'v3.2',
        datetime(2013, 1, 1): 'v3.8',
        datetime(2014, 1, 1): 'v3.13',
        datetime(2015, 1, 1): 'v3.19',
        datetime(2016, 1, 1): 'v4.4',
        datetime(2017, 1, 1): 'v4.10',
        datetime(2018, 1, 1): 'v4.15',
        datetime(2019, 1, 1): 'v5.0',
        datetime(2020, 1, 1): 'v5.5',
        datetime(2021, 1, 1): 'v5.11',
        datetime(2022, 1, 1): 'v5.16',
        datetime(2023, 1, 1): 'v6.2',
        datetime(2024, 1, 1): 'v6.7',
    }
    fm_version = None
    for key in sorted(versions.keys()):
        if date >= key:
            fm_version = versions[key]
    if fm_version is None:
        raise ValueError("No FM version found for the given date.")
    return fm_version

# Hauptfunktion zum Durchsuchen der Ausgangsdaten und Erstellen der CSV-Dateien
def generate_csv():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    output_folders = [folder for folder in os.listdir(script_dir) if os.path.isdir(os.path.join(script_dir, folder)) and folder.startswith("solve_sat-competition_")]
    
    for folder in output_folders:
        folder_path = os.path.join(script_dir, folder)
        output_filename = os.path.join(folder_path, "output.csv")
        
        if not os.path.exists(output_filename):
            continue
        
        # Lesen der Ausgangsdaten
        with open(output_filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                dimacs_file = row['dimacs-file']
                dimacs_analyzer = row['dimacs-analyzer']
                
                # Extrahieren des Jahres aus dem dimacs-analyzer
                year = dimacs_analyzer.split('/')[1].split('-')[0]
                
                # Extrahieren der SAT-Solver-Version
                sat_solver_version = dimacs_analyzer.split('/')[1].split('-')[1]
                
                # Extrahieren der Feature-Modell-Version basierend auf dem Jahr
                print(year)
                print(datetime(int(year)+2000, 1, 1))
                fm_version = get_fm_version(datetime(int(year), 1, 1))
                
                # CSV-Datei für jedes Jahr erstellen und abspeichern
                csv_data = [["Year", "FM Model", "SAT Solver"]]
                csv_data.append([year, fm_version, sat_solver_version])
                
                csv_filename = os.path.join(folder_path, f"{year}-model.csv")
                with open(csv_filename, "w", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(csv_data)
                
                print(f"CSV for year {year} in folder {folder} created successfully.")

# Hauptprogramm
if __name__ == "__main__":
    generate_csv()
