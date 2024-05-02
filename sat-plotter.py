import os
import csv
import matplotlib.pyplot as plt
import re
import sys
import time

# Kurzbeschreibung
# Es wird der Graph über die benötigte Zeit für alle Feature Modelle mit dem entsprechenden Solver geplottet.


# Static Variablen
ordnerPath = 'sorted_by_SAT'

# Ordner erstellen, wenn er nicht existiert
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


# Funktion zum Plotten der Daten für alle Solver
def plotter_fkt(data_dict, dateiname,title):
    plt.figure(figsize=(10, 6))  # Größe des Diagramms festlegen
    for solver, data in data_dict.items():
        versions = []
        times = []
        for row in data:
            versions.append(row['dimacs-analyzer'].split('/')[-1].split('[')[0])
            times.append(int(row['dimacs-analyzer-time']))

        # Sortiere die Versionen nach ihrem numerischen Wert
        versions_sorted = sorted(versions, key=lambda x: [int(num) if num.isdigit() else num for num in re.split(r'(\d+)', x)])
        # Wende die gleiche Reihenfolge auf die Zeiten an
        times_sorted = [times[versions.index(version)] for version in versions_sorted]

        # Plotte die Daten und benenne den Graphen entsprechend dem Solver
        plt.plot(versions_sorted, times_sorted, marker='o', label=solver)

    plt.xlabel('Version')
    plt.ylabel('Benötigte Zeit (ns)')
    plt.title(title)
    plt.xticks(rotation=45*2)
    plt.grid(True)
    plt.tight_layout()
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))  # Legende außerhalb des Diagramms platzieren
    plt.savefig(os.path.join(f"{dateiname}"), bbox_inches='tight')  # bbox_inches='tight' hinzugefügt
    # plt.show()
    plt.close()


# Hauptfunktion
def all_plotter(filter : str):
    # Neuer Ordner mit allen Daten ist: sorted_by_SAT
    # csvdaten = [datei for datei in os.listdir('sorted_by_SAT') if datei.endswith('-all.csv')]
    dateien = os.listdir(ordnerPath)
    csvdaten = [datei for datei in dateien if datei.endswith(filter)]

    data_dict = {}
    for csvdatei in csvdaten:
        path = os.path.join(ordnerPath, csvdatei)
        with open(path, 'r') as file:
            csv_reader = csv.DictReader(file, delimiter=',')
            next(csv_reader)
            data_dict[csvdatei] = list(csv_reader)

    # Plotte die Daten für alle Solver
    datei = os.path.join(ordnerPath,f"sat-all-{filter}-plot.png")
    title = f'Ausführungszeit pro Version für verschiedene Solver ({filter})'
    plotter_fkt(data_dict, datei,title)

# Für jede Datei wird ein Plot generiert
def separed_plotter(filter : str):
    # Neuer Ordner mit allen Daten ist: sorted_by_SAT
    dateien = os.listdir(ordnerPath)
    csvdaten = [datei for datei in dateien if datei.endswith(filter)]

    for csvdatei in csvdaten:
        path = os.path.join(ordnerPath, csvdatei)
        data_dict = {}
        with open(path, 'r') as file:
            csv_reader = csv.DictReader(file, delimiter=',')
            next(csv_reader)
            data_dict[csvdatei] = list(csv_reader)
        
        solver = csvdatei.split('_')[2] + ".png"
        title = "Solver: " + csvdatei.split('_')[2].split("-all")[0] + f" ({filter})"
        datei = os.path.join(ordnerPath,f"sat-{solver}-{filter}.png")
        plotter_fkt(data_dict, datei,title)

def tenGroup_plotter(filter :str):
    # Neuer Ordner mit allen Daten ist: sorted_by_SAT
    ordnerPath = 'sorted_by_SAT'
    dateien = os.listdir(ordnerPath)
    csvdaten = [datei for datei in dateien if datei.endswith(filter)]

    # Sortiere die CSV-Dateien nach dem Jahr
    csvdaten.sort(key=lambda x: int(x.split('_')[2][:2]))

    # Iteriere über die CSV-Dateien
    for i in range(0, len(csvdaten), 10):
        data_dict = {}
        for csvdatei in csvdaten[i:i+10]:
            path = os.path.join(ordnerPath, csvdatei)
            with open(path, 'r') as file:
                csv_reader = csv.DictReader(file, delimiter=',')
                next(csv_reader)
                data_dict[csvdatei] = list(csv_reader)
        
        # Erzeuge den Dateinamen und den Titel für das Diagramm
        start_index = i + 1
        end_index = min(i + 10, len(csvdaten))
        solver_range = f"{start_index}-{end_index}"
        datei = os.path.join(ordnerPath, f"sat-solver_{solver_range}-{filter}.png")
        title = f"Solver {solver_range} - Graph ({filter})"
        
        # Plotte die Daten für die Gruppe von 10 Solvern
        plotter_fkt(data_dict, datei, title)




# Verfügbare Filter
FILTER_KCONFIG = "-kconfig.csv"
FILTER_KMAX = "-kmax.csv"
FILTER_ALL = "all.sh"

if __name__ == "__main__":
    start_time = time.time()
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <Modus>")
        print("1. Alle Graphen werden in 1 Diagramm geplottet.")
        print("2. Für jeden Datei wird eine Graphen Datei gemacht.")
        print("3. Fasse jeweils 10 Graphen zu einer Datei zusammen.")
        print("9. Führ alles als Batch aus")
        exit()
    if int(sys.argv[1]) == 1:
        all_plotter(FILTER_KCONFIG)
        all_plotter(FILTER_KMAX)
    elif int(sys.argv[1]) == 2:
        separed_plotter(FILTER_KCONFIG)
        separed_plotter(FILTER_KMAX)
    elif int(sys.argv[1]) == 3:
        tenGroup_plotter(FILTER_KCONFIG)
        tenGroup_plotter(FILTER_KMAX)

    elif int(sys.argv[1]) == 9:
        all_plotter(FILTER_KCONFIG)
        separed_plotter(FILTER_KCONFIG)
        tenGroup_plotter(FILTER_KCONFIG)

        all_plotter(FILTER_KMAX)
        separed_plotter(FILTER_KMAX)
        tenGroup_plotter(FILTER_KMAX)
    else:
        print("unbekannter Modus")
    # main()
    end_time = time.time()
    execution_time = end_time - start_time
    print("Ausführungszeit:", execution_time, "Sekunden")
