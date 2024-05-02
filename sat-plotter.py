import os
import csv
import matplotlib.pyplot as plt
import re
import sys

# Kurzbeschreibung
# Es wird der Graph über die benötigte ZEit für alle Feature Modell mit dem entsprechenden Solver geplottet.


# Ordner erstellen, wenn er nicht existiert
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


# Funktion zum Plotten der Daten für alle Solver
def plot_all_solvers(data_dict,dateiname):
    plt.figure(figsize=(10, 6))  # Größe des Diagramms festlegen
    for solver, data in data_dict:
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

    plt.xlabel('Version')
    plt.ylabel('Benötigte Zeit (ns)')
    plt.title('Ausführungszeit pro Version für verschiedene Solver')
    plt.xticks(rotation=45*2)
    plt.grid(True)
    plt.tight_layout()
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))  # Legende außerhalb des Diagramms platzieren
    print(os.path.join(f"{dateiname}-sa.png"))
    plt.savefig(os.path.join(f"{dateiname}-sa.png"), bbox_inches='tight')  # bbox_inches='tight' hinzugefügt
    #plt.show()


# 'all_solvers_plot.png'


# Filterfunktion definieren
def filter_entries(entry):
    return '[i386]' not in entry['dimacs-file']

# Hauptfunktion
def all_plotter():
    # Neuer Ordner mit allen Daten ist: sorted_by_SAT
    #csvdaten = [datei for datei in os.listdir('sorted_by_SAT') if datei.endswith('-all.csv')]
    ordnerPath = 'sorted_by_SAT'
    dateien = os.listdir(ordnerPath)
    csvdaten = [datei for datei in dateien if datei.endswith('-all.csv')]
    print(csvdaten)


    data_dict = {}
    for csvdatei in csvdaten:
        path = os.path.join(ordnerPath,csvdatei)
        with open(path,'r') as file:
            
            csv_reader = csv.DictReader(file, delimiter=',')
            next(csv_reader) 
            data_dict = list(csv_reader)

    # Plotte die Daten für alle Solver
    data_dict = data_dict[0]
    print("\n")
    print(data_dict)
    plot_all_solvers(data_dict,"test.pnng")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <Modus>")
        exit()
    if int(sys.argv[1]) == 1:
        all_plotter()
    else:
        print("unbekannter Modus")
     #main()
