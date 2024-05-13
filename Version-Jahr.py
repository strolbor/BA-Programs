import pandas as pd
import matplotlib.pyplot as plt
import os

# # Funktion zum Zuordnen des Jahres basierend auf der Linux-Version
# def get_year(linux_version):
#     return int(linux_versions.get(linux_version, "Unknown"))

# def convert_short_year(short_year):
#     # Annahme: short_year ist ein String
#     # Extrahiere das Jahr aus dem Dateinamen
#     year_str = short_year.split("[")[0].split("v")[-1]
#     return int(year_str)+2000

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

ordnername = "sorted_by_verlauf"
create_folder_if_not_exists(ordnername)

# linux_versions = {
#     'v2.5.45': '2002',
#     'v2.5.54': '2003',
#     'v2.6.1': '2004',
#     'v2.6.11': '2005',
#     'v2.6.15': '2006',
#     'v2.6.20': '2007',
#     'v2.6.24': '2008',
#     'v2.6.29': '2009',
#     'v2.6.33': '2010',
#     'v2.6.37': '2011',
#     'v3.2': '2012',
#     'v3.8': '2013',
#     'v3.13': '2014',
#     'v3.19': '2015',
#     'v4.4': '2016',
#     'v4.10': '2017',
#     'v4.15': '2018',
#     'v5.0': '2019',
#     'v5.5': '2020',
#     'v5.11': '2021',
#     'v5.16': '2022',
#     'v6.2': '2023',
#     'v6.7': '2024'
# }

# Lese die Daten aus den CSV-Dateien
sat_kconfigreader = pd.read_csv("sorted_by_SAT/sat-all-kconfigreader-median.csv")
sat_kmax = pd.read_csv("sorted_by_SAT/sat-all-kmax-median.csv")

## Obsulet geworden, weil picker.py das schon macht

# Füge eine neue Spalte 'Year' hinzu, um das Jahr zu speichern
# kconfigreader/linux/v2.5.45[i386].dimacs
# sat_kconfigreader['Year-DIMACS'] = sat_kconfigreader['dimacs-file'].apply(lambda x: get_year(x.split("/")[2].split("[")[0]))
# sat_kmax['Year-DIMACS'] = sat_kmax['dimacs-file'].apply(lambda x: get_year(x.split("/")[2].split("[")[0]))


# #  Füge den Solver das Jahr hinzu
# sat_kconfigreader['Year-SOLVER'] = sat_kconfigreader['dimacs-analyzer'].apply(lambda x: convert_short_year(x.split("/")[1].split("-")[0]))
# sat_kmax['Year-SOLVER'] = sat_kmax['dimacs-analyzer'].apply(lambda x: convert_short_year(x.split("/")[1].split("-")[0]))

# Filter nach JAhr DIMAXs == Jahr Solver

filtered_kmax = sat_kmax[sat_kmax['Year-DIMACS'] == sat_kmax['Year-SOLVER']]
filtered_kconfig = sat_kconfigreader[sat_kconfigreader['Year-DIMACS'] == sat_kconfigreader['Year-SOLVER']]

# Speichern als csv
filtered_kconfig.to_csv(os.path.join(ordnername,"Version-Jahr-kconfig.csv"),index=False)
filtered_kmax.to_csv(os.path.join(ordnername,"Version-Jahr-kmax.csv"),index=False)

# Plot
# def plotter(df,suffix):
#     global ordnername
#     plt.figure(figsize=(10, 6))
#     plt.scatter(df['Year-DIMACS'], df['dimacs-analyzer-time'], label='Verlauf', color='blue')
#     plt.plot(df['Year-DIMACS'], df['dimacs-analyzer-time'], marker='o')
#     plt.xlabel('Jahr')
#     plt.ylabel('Zeit')
#     plt.title('Zeit vs. FM & Solver aus dem gleichen Jahr')
#     plt.xticks(rotation=90)
#     plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#     plt.grid(True)
#     plt.savefig(os.path.join(ordnername,f'Version-Jahr-{suffix}.png'), bbox_inches='tight')

def plotter(df, suffix):
    global ordnername
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Year-DIMACS'], df['dimacs-analyzer-time'], label='Verlauf', color='blue')
    plt.plot(df['Year-DIMACS'], df['dimacs-analyzer-time'], marker='o')
    plt.xlabel('Jahr')
    plt.ylabel('Nanosekunden')
    plt.title('Zeit vs. FM & Solver aus dem gleichen Jahr')
    plt.xticks(df['Year-DIMACS'].unique(), rotation=90)  # This ensures all unique years are marked on the x-axis
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True)
    plt.savefig(os.path.join(ordnername, f'Version-Jahr-{suffix}.png'), bbox_inches='tight')


#filtered_kmax = filtered_kmax[filtered_kmax['Year-DIMACS'] == filtered_kmax['Year-SOLVER']]
plotter(filtered_kmax,"kmax")
plotter(filtered_kconfig,"kconfig")



