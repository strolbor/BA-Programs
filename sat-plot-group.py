import os
import csv
import matplotlib.pyplot as plt
import re
from datetime import datetime

# Kurzbeschreibung
# Es wird der Graph über die benötigte ZEit für alle Feature Modell mit dem entsprechenden Solver geplottet.
# Unterteilt in 10 Gruppen

# Ordner erstellen, wenn er nicht existiert
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Funktion zum Plotten der Daten für die neuesten zehn Solver
def plot_latest_solvers(data_dict,piccounter):
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

        # Plotte die Daten und benenne den Graphen entsprechend dem Solver
        plt.plot(versions_sorted, times_sorted, marker='o', label=solver)

    print()
    plt.xlabel('Version')
    plt.ylabel('Benötigte Zeit (ns)')
    plt.title('Ausführungszeit pro Version für zehn Solver')
    plt.xticks(rotation=45*2)
    plt.grid(True)
    plt.tight_layout()
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))  # Legende außerhalb des Diagramms platzieren
    picord = "pics-solvers"
    create_folder_if_not_exists(picord)
    plt.savefig(os.path.join(picord, f'ten_solvers_plot-{piccounter}.png'), bbox_inches='tight')  # bbox_inches='tight' hinzugefügt
    print("saved pic")
    plt.clf()



# Hauptfunktion
def main():
    # Suche nach Ordnern, die mit "solve_sat_" beginnen
    folders = [folder for folder in os.listdir() if folder.startswith("solve_sat-") and os.path.isdir(folder)]

    # Dictionary zum Sammeln der Daten für jeden Solver
    data_dict = {}

    solver_years={}

    # Extrahiere das Jahr aus dem Dateinamen
    for folder in folders:
        year = folder.split('_')[2][:2]  # Extrahiere die ersten beiden Zeichen des zweiten Teils des Ordnernamens
        solver = folder.split('_')[-1]  # Extrahiere den Namen des Solvers
        solver_years[folder] = (year, solver)

    # Sortiere die Ordnernamen nach ihrem Jahr
    folders_sorted = sorted(solver_years.keys(), key=lambda x: int(solver_years[x][0]))

    # Wähle die Daten der ersten zehn Solver aus
    #latest_folders = folders_sorted[-10:]


    firstten = folders_sorted[0:10] # Anzahl 10
    print("1",firstten)

    for folder in firstten:
        csv_path = os.path.join(folder, 'output.csv')
        if os.path.exists(csv_path):
            with open(csv_path, 'r') as file:
                csv_reader = csv.DictReader(file, delimiter=',')
                next(csv_reader) 
                data = list(csv_reader)
                # Füge die Daten dem entsprechenden Solver im Dictionary hinzu
                data_dict[folder] = data

    # Plotte die Daten für die neuesten zehn Solver
    plot_latest_solvers(data_dict,'0')

    data_dict = {}
    #secound = tmp.copy()
    secound = folders_sorted[10:20] # Anzahl 10 
    print("2:" ,secound)
    for folder in secound:
        csv_path = os.path.join(folder, 'output.csv')
        if os.path.exists(csv_path):
            with open(csv_path, 'r') as file:
                csv_reader = csv.DictReader(file, delimiter=',')
                next(csv_reader) 
                data = list(csv_reader)
                # Füge die Daten dem entsprechenden Solver im Dictionary hinzu
                data_dict[folder] = data

    # Plotte die Daten für die neuesten zehn Solver
    plot_latest_solvers(data_dict,'1')

    data_dict = {}
    #secound = tmp.copy()
    third = folders_sorted[20:30]
    print("3:" ,third)

    for folder in third:
        csv_path = os.path.join(folder, 'output.csv')
        if os.path.exists(csv_path):
            with open(csv_path, 'r') as file:
                csv_reader = csv.DictReader(file, delimiter=',')
                next(csv_reader) 
                data = list(csv_reader)
                # Füge die Daten dem entsprechenden Solver im Dictionary hinzu
                data_dict[folder] = data

    # Plotte die Daten für die neuesten zehn Solver
    plot_latest_solvers(data_dict,'2')



if __name__ == "__main__":
    main()
