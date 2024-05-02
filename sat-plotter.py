import os
import csv
import matplotlib.pyplot as plt
import re
import sys

# Kurzbeschreibung
# Es wird der Graph über die benötigte Zeit für alle Feature Modelle mit dem entsprechenden Solver geplottet.


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

# Hauptfunktion
def all_plotter():
    # Neuer Ordner mit allen Daten ist: sorted_by_SAT
    # csvdaten = [datei for datei in os.listdir('sorted_by_SAT') if datei.endswith('-all.csv')]
    ordnerPath = 'sorted_by_SAT'
    dateien = os.listdir(ordnerPath)
    csvdaten = [datei for datei in dateien if datei.endswith('-all.csv')]

    data_dict = {}
    for csvdatei in csvdaten:
        path = os.path.join(ordnerPath, csvdatei)
        with open(path, 'r') as file:
            csv_reader = csv.DictReader(file, delimiter=',')
            #print(f"Struktur der CSV-Datei {csvdatei}: {csv_reader.fieldnames}")
            next(csv_reader)
            data_dict[csvdatei] = list(csv_reader)

    # Plotte die Daten für alle Solver
    datei = os.path.join(ordnerPath,"sat-all-plot.png")
    title = 'Ausführungszeit pro Version für verschiedene Solver'
    plotter_fkt(data_dict, datei,title)

# def separed_plotter():
#     # Neuer Ordner mit allen Daten ist: sorted_by_SAT
#     ordnerPath = 'sorted_by_SAT'
#     dateien = os.listdir(ordnerPath)
#     csvdaten = [datei for datei in dateien if datei.endswith('-all.csv')]

#     for csvdatei in csvdaten:
#         path = os.path.join(ordnerPath, csvdatei)
#         with open(path, 'r') as file:
#             csv_reader = csv.DictReader(file, delimiter=',')
#             next(csv_reader)
#             data = list(csv_reader)
        
#         solver = csvdatei.split('-')[0]
#         dateiname = os.path.join(solver,"-plot.png")
#         print(dateiname)
#         plotter_fkt(data, dateiname)

def separed_plotter():
    # Neuer Ordner mit allen Daten ist: sorted_by_SAT
    ordnerPath = 'sorted_by_SAT'
    dateien = os.listdir(ordnerPath)
    csvdaten = [datei for datei in dateien if datei.endswith('-all.csv')]

    for csvdatei in csvdaten:
        path = os.path.join(ordnerPath, csvdatei)
        data_dict = {}
        with open(path, 'r') as file:
            csv_reader = csv.DictReader(file, delimiter=',')
            next(csv_reader)
            data_dict[csvdatei] = list(csv_reader)
        
        solver = csvdatei.split('_')[2] + ".png"
        title = "Solver: " + solver
        datei = os.path.join(ordnerPath,solver)
        plotter_fkt(data_dict, datei,title)



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <Modus>")
        exit()
    if int(sys.argv[1]) == 1:
        all_plotter()
    elif int(sys.argv[1]) == 2:
        separed_plotter()
    else:
        print("unbekannter Modus")
    # main()
