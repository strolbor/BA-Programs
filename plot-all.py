import os
import csv
import matplotlib.pyplot as plt
import re

# Ordner erstellen, wenn er nicht existiert
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Funktion zum Plotten der Daten für alle Solver
def plot_all_solvers(data_dict):
    plt.figure(figsize=(10, 6))  # Größe des Diagramms festlegen
    for solver, data in data_dict.items():
        versions = []
        times = []
        for row in data:
            versions.append(row['dimacs-file'].split('/')[-1].split('[')[0])
            times.append(int(row['dimacs-analyzer-time']))

        # Sortiere die Versionen nach ihrem numerischen Wert
        versions_sorted = sorted(versions, key=lambda x: [int(num) if num.isdigit() else num for num in re.split(r'(\d+)', x)])
        # Wende die gleiche Reihenfolge auf die Zeiten an
        times_sorted = [times[versions.index(version)] for version in versions_sorted]

        plt.plot(versions_sorted, times_sorted, marker='o', label=solver)

    plt.xlabel('Version')
    plt.ylabel('Benötigte Zeit (ns)')
    plt.title('Ausführungszeit pro Version für verschiedene Solver')
    plt.xticks(rotation=45*2)
    plt.grid(True)
    plt.tight_layout()
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))  # Legende außerhalb des Diagramms platzieren
    picord = "pics-solvers"
    create_folder_if_not_exists(picord)
    plt.savefig(os.path.join(picord, 'all_solvers_plot.png'))

# Hauptfunktion
def main():
    # Suche nach Ordnern, die mit "solve_sat_" beginnen
    folders = [folder for folder in os.listdir() if folder.startswith("solve_sat-") and os.path.isdir(folder)]

    # Dictionary zum Sammeln der Daten für jeden Solver
    data_dict = {}

    for folder in folders:
        print(folder)
        csv_path = os.path.join(folder, 'output.csv')
        if os.path.exists(csv_path):
            with open(csv_path, 'r') as file:
                csv_reader = csv.DictReader(file, delimiter=',')
                next(csv_reader) 
                data = list(csv_reader)
                # Füge die Daten dem entsprechenden Solver im Dictionary hinzu
                data_dict[folder] = data

    # Plotte die Daten für alle Solver
    plot_all_solvers(data_dict)

if __name__ == "__main__":
    main()
