import pandas as pd
import matplotlib.pyplot as plt
import os

logScale = True

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

ordnername = "sorted_by_verlauf"
create_folder_if_not_exists(ordnername)

# Lese die Daten aus den CSV-Dateien
sat_kconfigreader = pd.read_csv("sorted_by_SAT/sat-all-kconfigreader-median.csv")
sat_kmax = pd.read_csv("sorted_by_SAT/sat-all-kmax-median.csv")

filtered_kmax = sat_kmax[sat_kmax['Year-DIMACS'] == sat_kmax['Year-SOLVER']]
filtered_kconfig = sat_kconfigreader[sat_kconfigreader['Year-DIMACS'] == sat_kconfigreader['Year-SOLVER']]

# Speichern als csv
filtered_kconfig.to_csv(os.path.join(ordnername,"Version-Jahr-kconfig.csv"),index=False)
filtered_kmax.to_csv(os.path.join(ordnername,"Version-Jahr-kmax.csv"),index=False)

def plotter_combined(df1, df2, suffix1, suffix2):
    global ordnername
    plt.figure(figsize=(12, 6))

    plt.scatter(df1['Year-DIMACS'], df1['dimacs-analyzer-time'], label=f'Verlauf KMAX', color='blue')
    plt.plot(df1['Year-DIMACS'], df1['dimacs-analyzer-time'], marker='o', color='blue')

    plt.scatter(df2['Year-DIMACS'], df2['dimacs-analyzer-time'], label=f'Verlauf KConfigReader', color='red')
    plt.plot(df2['Year-DIMACS'], df2['dimacs-analyzer-time'], marker='o', color='red')

    plt.xlabel('Jahr')
    plt.ylabel('Sekunden')
    if logScale:
        plt.yscale('log')
        plt.ylabel('Sekunden (log_10-scaled)')
    plt.title('Zeit vs. FM & Solver aus dem gleichen Jahr')
    plt.xticks(df1['Year-DIMACS'].unique(), rotation=90)  # Assuming both dataframes have the same years
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True)
    plt.savefig(os.path.join(ordnername, f'Version-Jahr-punktpunkt-{suffix1}-{suffix2}-combined.png'), bbox_inches='tight')
    plt.savefig(os.path.join(ordnername, f'Version-Jahr-punktpunkt-{suffix1}-{suffix2}-combined.svg'), bbox_inches='tight')

if __name__ == '__main__':
    print("punkt-punkt")
    plotter_combined(filtered_kmax, filtered_kconfig, "kmax", "kconfig")
