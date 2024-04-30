 
import os
import csv
import matplotlib.pyplot as plt
import re

# Kurzbeschreibung
# Es wird der Graph über die benötigte ZEit für alle Feature Modell mit dem entsprechenden Solver geplottet.

# Ordner erstelle, wenn er nicht existiert
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Funktion zum Plotten der Daten
def plot_data(folder_path, data):
    versions = []
    times = []
    for row in data:
        versions.append(row['dimacs-file'].split('/')[-1].split('[')[0])
        times.append(int(row['dimacs-analyzer-time']))

    # Sortiere die Versionen nach ihrem numerischen Wert
    versions_sorted = sorted(versions, key=lambda x: [int(num) if num.isdigit() else num for num in re.split(r'(\d+)', x)])
    # Wende die gleiche Reihenfolge auf die Zeiten an
    times_sorted = [times[versions.index(version)] for version in versions_sorted]

    plt.figure()
    plt.plot(versions_sorted, times_sorted, marker='o')
    plt.xlabel('Version')
    plt.ylabel('Benötigte Zeit (ns)')
    plt.title(f'Solver: {folder_path.split("_")[2]}')
    plt.xticks(rotation=45*2)
    plt.grid(True)
    plt.tight_layout()
    picord = "pics-solvers"
    create_folder_if_not_exists(picord)
    plt.savefig(os.path.join(picord, f'{folder_path}-plot.png'))

# Filterfunktion definieren
def filter_entries(entry):
    return '[i386]' not in entry['dimacs-file']

# Hauptfunktion
def main():
    # Suche nach Ordnern, die mit "solve_sat_" beginnen
    folders = [folder for folder in os.listdir() if folder.startswith("solve_sat-") and os.path.isdir(folder)]

    for folder in folders:
        csv_path = os.path.join(folder, 'output.csv')
        if os.path.exists(csv_path):
            with open(csv_path, 'r') as file:
                csv_reader = csv.DictReader(file, delimiter=',')
                next(csv_reader) 
                data = list(csv_reader)
                filtered_data = list(filter(filter_entries, data))
                print(filtered_data)
                plot_data(folder, filtered_data)

if __name__ == "__main__":
    main()
