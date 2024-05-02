import os
import csv

# Dictionary, um die Zuordnung von Linux-Versionen zu Jahren zu speichern
# SAT Solver  aus Jahr 2005 wird mit dem Feature Modell aus 2005 miteinander Verbunden
# somit soll die Entwicklung gezeigt werden
# VGL: SAT-Solver == FM


linux_versions = {
    'v2.5.45': '2002',
    'v2.5.54': '2003',
    'v2.6.1': '2004',
    'v2.6.11': '2005',
    'v2.6.15': '2006',
    'v2.6.20': '2007',
    'v2.6.24': '2008',
    'v2.6.29': '2009',
    'v2.6.33': '2010',
    'v2.6.37': '2011',
    'v3.2': '2012',
    'v3.8': '2013',
    'v3.13': '2014',
    'v3.19': '2015',
    'v4.4': '2016',
    'v4.10': '2017',
    'v4.15': '2018',
    'v5.0': '2019',
    'v5.5': '2020',
    'v5.11': '2021',
    'v5.16': '2022',
    'v6.2': '2023',
    'v6.7': '2024'
}

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Funktion zum Auslesen der Output-CSV-Datei
def read_output_csv(file_path):
    data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

# Funktion zum Extrahieren von FM (Linux-Version) und SAT-Solver aus dem Dateipfad
def extract_fm_and_solver(file_path):
    parts = file_path.split('/')
    return parts[1], parts[0]

# Funktion zum Zuordnen des Jahres basierend auf der Linux-Version
def get_year(linux_version):
    return linux_versions.get(linux_version, "Unknown")

def convert_short_year(short_year):
    # Annahme: short_year ist ein String
    # Extrahiere die letzten zwei Ziffern des Jahres
    year_last_two_digits = int(short_year)
    # Annahme: wenn die letzten zwei Ziffern kleiner oder gleich 21 sind, beziehen sie sich auf das 21. Jahrhundert, andernfalls auf das 20. Jahrhundert
    if year_last_two_digits <= 21:
        return 2000 + year_last_two_digits
    else:
        return 1900 + year_last_two_digits


# Hauptfunktion zur Erstellung der Auflistung
def generate_yearly_list(output_data):
    yearly_data = []
    for row in output_data:
        dimacs_file = row['dimacs-file']
        dimacs_analyzer = row['dimacs-analyzer']
        dimacs_analyzer_time = row['dimacs-analyzer-time']
        model_satisfiable = row['model-satisfiable']
        #print(row)
        fm_version = dimacs_file.split("/")[2].split("[")[0]
        fm_year = get_year(fm_version)
        sat_version = dimacs_analyzer.split("/")[1] ## 'sat-competition/09-precosat' -> 09-precosat
        sat_year = convert_short_year(sat_version.split("-")[0])
        #print(fm_year,sat_year)
        if int(fm_year) == int(sat_year):
            yearly_data.append({
                    'Year': fm_year,
                    'FM': dimacs_file,
                    'SAT Solver': sat_version,
                    'dimacs-analyzer-time': dimacs_analyzer_time,
                    'model-satisfiable': model_satisfiable
                })

    return yearly_data

# Hauptprogramm
if __name__ == "__main__":
    output_csv_path = "output.csv"  # Passe den Pfad entsprechend an
    folders = [folder for folder in os.listdir() if folder.startswith("solve_sat-") and os.path.isdir(folder)]

    output_data = []
    for folder in folders:
        path = os.path.join(folder, output_csv_path)
        output_data += read_output_csv(path)

    #print(output_data)
    yearly_list = generate_yearly_list(output_data)

    # yearly_list nach Jahr sortieren
    sorted_yearly_list = sorted(yearly_list, key=lambda x: x['Year'])

    #print(yearly_list)

    # Ausgabe der Ergebnisse
    fields = ["Year", "FM", "SAT Solver",'dimacs-analyzer-time','model-satisfiable']

    # Dateiname der CSV-Datei
    ordnerpath = "sorted_verlauf"
    create_folder_if_not_exists(ordnerpath)
    csv_file1 = os.path.join(ordnerpath,"Version-Year-kmax.csv")
    csv_file2 = os.path.join(ordnerpath,"Version-Year-kconfig.csv")

    # files open 
    file1 = open(csv_file1,"w") # kmax
    file2 = open(csv_file2,"w")

    # CSV-Dateien schreiben
    with open(csv_file1, "w", newline='') as file1, open(csv_file2, "w", newline='') as file2:
        writer1 = csv.DictWriter(file1, fieldnames=fields)
        writer2 = csv.DictWriter(file2, fieldnames=fields)

        # Schreibe die Spaltenüberschriften
        writer1.writeheader()
        writer2.writeheader()

        # Schreibe die Daten
        for row in sorted_yearly_list:
            if 'kmax' in row["FM"]:
                writer1.writerow(row)
            elif 'kconfigreader' in row["FM"]:
                writer2.writerow(row)
    file2.close()
    file1.close()

