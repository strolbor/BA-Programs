import os
import csv
from collections import defaultdict

# Hauptfunktion
def main():
    # Laden der Daten und Gruppierung nach dem Jahr
    data_dict = load_data()
    grouped_data_dict = group_by_year(data_dict)
    print(grouped_data_dict)

    # Hier können Sie weiter mit den gruppierten Daten arbeiten

# Funktion zum Laden der Daten
def load_data():
    # Suche nach Ordnern, die mit "solve_sat_" beginnen
    folders = [folder for folder in os.listdir() if folder.startswith("solve_sat-") and os.path.isdir(folder)]

    # Dictionary zum Sammeln der Daten für jeden Solver
    data_dict = {}

    for folder in folders:
        csv_path = os.path.join(folder, 'output.csv')
        if os.path.exists(csv_path):
            with open(csv_path, 'r') as file:
                csv_reader = csv.DictReader(file, delimiter=',')
                next(csv_reader)
                data = list(csv_reader)
                data_dict[folder] = data

    return data_dict

# Funktion zum Gruppieren der Daten nach dem Jahr
def group_by_year(data_dict):
    grouped_data_dict = defaultdict(dict)

    for solver, data in data_dict.items():
        year = solver.split('_')[2][:2]
        grouped_data_dict[year][solver] = data

    return grouped_data_dict

if __name__ == "__main__":
    main()
