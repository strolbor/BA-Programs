import os
import numpy as np
import time
import pandas as pd

import matplotlib.pyplot as plt

import argparse


## Kurzbeschreibung


# Dieses Python-Skript extrahiert und sortiert Daten aus CSV-Dateien nach SAT-Solvern und Feature-Modellen. 
# Es können auch 1 Bulk-Aktion durchgeführt, um alle Daten zu sammeln und zu schreiben.

remove2024_dimacs = False
remove2023_solver = False
logScale = False

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

def convert_short_year(short_year):
    # Annahme: short_year ist ein String
    # Extrahiere das Jahr aus dem Dateinamen
    year_str = short_year.split("[")[0].split("v")[-1]
    return int(year_str)+2000

def get_year(linux_version):
    return int(linux_versions.get(linux_version, "Unknown"))


def find_matching_entry(array, prefix):
    for entry in array:
        if entry.startswith(prefix):
            return entry
    return None

# -------------------



def load_data_from_csv(csv_path):
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        print("Die Datei {} existiert nicht.".format(csv_path))
        return pd.DataFrame()

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def get_median(df : pd.core.frame.DataFrame,name):
    """Diese Funktion filtert, den Median heraus.
    Tauscht Endung .csv mit -median.csv aus"""
    name = name.replace(".csv","-median.csv")

    # DataFrame nach "dimacs-analyzer-time" sortieren
    sorted_df = df.sort_values(by='dimacs-analyzer-time')

    # Gruppieren nach ['dimacs-analyzer', 'dimacs-file'] und Median berechnen
    median_grouped = sorted_df.groupby(['dimacs-analyzer', 'dimacs-file']).median().reset_index()
    # Spalten erneut konvertieren
    median_grouped['Year-DIMACS'] = median_grouped['Year-DIMACS'].astype('int64')
    median_grouped['Year-SOLVER'] = median_grouped['Year-SOLVER'].astype('int64')

    median_grouped.to_csv(name,index=False)

    return median_grouped

def save_csv(df,name):
    """speichert das DataFrame in eine csv Datei"""
    df.to_csv(name,index=False)

# ----------------------
MODUS_FM = 1
MODUS_SAT = 2

# SAT  
def all_save_SAT(df2,filterReader,ordnername):
    """Diese Funktion plottet alle Diagramme in einem.
    x-Achse: Feature Modell
    y-achse: Millisekunden
    Slave-Fkt zu all_save_SAT"""
    datei_mod = os.path.join(ordnername, "sat-all"+ f"-{filterReader}.csv")
    df2 = df2[df2['dimacs-file'].str.contains(filterReader)]
    if not df2.empty:
        # alle Daten speichern ohne Median Filter
        save_csv(df2,datei_mod)

        # Bild plotten
        #plot_all_SAT(get_median(df,datei_mod),datei_mod.replace(".csv",".png"))
        name = datei_mod.replace(".csv",".png")

        df = get_median(df2,datei_mod)

        # Plot erstellen
        plt.figure(figsize=(12, 6))

        # Farben für die Linien im Plot definieren
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

        # Prefixe entfernen
        df['dimacs-file'] = df['dimacs-file'].str.replace('kconfigreader/linux/', '')
        df['dimacs-file'] = df['dimacs-file'].str.replace('kmax/linux/', '')

        # Suffix entfernen
        df['dimacs-file'] = df['dimacs-file'].str.replace('.dimacs', '',regex=False)

        # sat ENTFERNEN
        df['dimacs-analyzer'] = df['dimacs-analyzer'].str.replace('sat-competition/','')

        # Nur für SAT
        df.sort_values(by='Year-DIMACS', inplace=True)

        solver_groups = df.groupby('dimacs-analyzer')
        plot_x = 'Year-DIMACS' # 'Year-DIMACS' #'dimacs-file'
        plot_y = 'dimacs-analyzer-time'

        # Durch jeden SAT-Solver iterieren und Daten plotten
        for i, (solver, data) in enumerate(solver_groups):
            plt.plot(data[plot_x], data[plot_y], label=solver, color=colors[i % len(colors)], marker='o', linestyle='-')
            #plt.plot(data['Year-DIMACS'], data['dimacs-analyzer-time'], label=solver, color=colors[i % len(colors)], marker='o', linestyle='-')

        
        plt.xlabel('Feature Modell Jahr')
        plt.ylabel('Millisekunden')
        # Achsenbeschriftungen festlegen
        if logScale:
            plt.yscale('log')
            plt.ylabel('Millisekunden (log-scaled)')
        plt.xticks(df[plot_x].unique(),rotation=90) 
        plt.grid(True, which="both", ls="--")  # Gitterlinien anzeigen
        plt.title(f'SAT Solvern Vergleich ({filterReader})')  # Titel des Plots festlegen
        #plt.title("Geordnet nach Solver: " + name.split("/")[1])

        # Plot anzeigen
        plt.tight_layout(rect=[0, 0, 0.7, 1])
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Solver")  # Legende anpassen
        plt.savefig(name)  # Plot speichern
        plt.close()

def save_single_entry_SAT(df2,filterReader, filterVersion, ordnername):
    """Diese Funktion plottet einzelne Diagramme.
    x-Achse: Feature Modell Jahr
    y-achse: Millisekunden"""
    df2 = df2[df2['dimacs-file'].str.contains(filterReader) & (df2['dimacs-analyzer'] == filterVersion)]
    # sat-competition/07-RSat
    datei_mod = os.path.join(ordnername, filterVersion.split("/")[1]+ f"-{filterReader}.csv")

    if not df2.empty:
        save_csv(df2,datei_mod)

        name = datei_mod.replace(".csv",".png")
        # Median berechnen und speichern
        df = get_median(df2,datei_mod)


        # Nur für SAT
        df.sort_values(by='Year-DIMACS', inplace=True)

        

        # Prefixe entfernen
        df['dimacs-file'] = df['dimacs-file'].str.replace('kconfigreader/linux/', '')
        df['dimacs-file'] = df['dimacs-file'].str.replace('kmax/linux/', '')

        # Suffix entfernen
        df['dimacs-file'] = df['dimacs-file'].str.replace('.dimacs', '',regex=False)

        # sat ENTFERNEN
        df['dimacs-analyzer'] = df['dimacs-analyzer'].str.replace('sat-competition/','')


        # Plot erstellen
        plt.figure(figsize=(10, 6))       
        
        
        df_group  = df.groupby('dimacs-analyzer')
        plot_x = 'Year-DIMACS' # 'Year-DIMACS' #'dimacs-file'
        plot_y = 'dimacs-analyzer-time'

        

        for solver, data in df_group:
            plt.plot(data[plot_x], data[plot_y], marker='o', linestyle='-', label=solver)


        plt.xlabel('Feature Modell Jahr')
        plt.ylabel('Millisekunden')
        if logScale:
            plt.yscale('log')
            plt.ylabel('Millisekunden (log-scaled)')
        plt.title("Solver: " + name.split("/")[1].split(".")[0])
        plt.xticks(df[plot_x].unique(),rotation=90) #
        plt.grid(True)
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Solver")
        plt.tight_layout()

        plt.savefig(os.path.join(name))
        plt.close()

def mod_SAT_all():
    """Diese Funktion startet in den Prozess der Datenanalyse.
    1. leiest Daten ein.
    2. Fügt die Jahreszahlen hinzu.
    3. Unique-Liste der Solver
    4. all-Plots speichern
    5. Single Plots speichern"""

    print("Modus SAT_all")
    ordnername = "sorted_by_SAT"
    create_folder_if_not_exists(ordnername)

    # Die Feature Modell dynamisch laden
    data = load_data_from_csv("solve_model-satisfiable/output.csv")

    #  Füge den Solver das Jahr hinzu                                                                           #.astype('int64')
    data['Year-SOLVER'] = data['dimacs-analyzer'].apply(lambda x: convert_short_year(x.split("/")[1].split("-")[0])).astype('int64')

    # Füge eine neue Spalte 'Year' hinzu, um das Jahr zu speichern
    # kconfigreader/linux/v2.5.45[i386].dimacs
    data['Year-DIMACS'] = data['dimacs-file'].apply(lambda x: get_year(x.split("/")[2].split("[")[0])).astype('int64')

    # Exponenten 
    data['analyzer_Exponent'] = data['dimacs-analyzer-time'].apply(lambda x: np.floor(np.log10(x))).astype(int)

    # Speicher n der Millisekunden
    data['dimacs-analyzer-time_orig'] = data['dimacs-analyzer-time']

    # Zeit in Millisekunden
    data['dimacs-analyzer-time'] = data['dimacs-analyzer-time'].apply(lambda x: np.divide(x,1000000))

    # Alle Salver auflisten
    df2 = data.groupby('dimacs-analyzer').apply(lambda x: x['dimacs-analyzer'].unique())

    # Remove FM des Jahres 2024
    if remove2024_dimacs:
        data = data[data['Year-DIMACS'] != 2024]
    
    # Remove SAT des Jahres 2023
    if remove2023_solver:
        data = data[data['Year-SOLVER'] != 2023]

    zahler = 0

    # Alle Plots zusammen fassen
    all_save_SAT(data,'kmax',ordnername)
    all_save_SAT(data,'kconfigreader',ordnername)

    # Durchlaufe jeden Solver
    # Speichere zu jeden Feature Modell die entsprechenden Solver
    
    for entry in df2:
        sat_program = entry[0]
        zahler +=1

         # KMAX logic
        save_single_entry_SAT(data,'kmax',sat_program,ordnername)
        # KCONFIG logic
        save_single_entry_SAT(data,'kconfigreader',sat_program,ordnername)

# FM

def plot_all_FM(df,name,ReaderStr):
    """Speichert die Daten als Plot."""
    # Plot erstellen
    plt.figure(figsize=(12, 6))

    # Farben für die Linien im Plot definieren
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

    # Prefixe entfernen
    df['dimacs-file'] = df['dimacs-file'].str.replace('kconfigreader/linux/', '')
    df['dimacs-file'] = df['dimacs-file'].str.replace('kmax/linux/', '')

    # Suffix entfernen
    df['dimacs-file'] = df['dimacs-file'].str.replace('.dimacs', '',regex=False)

    df['dimacs-analyzer'] = df['dimacs-analyzer'].str.replace('sat-competition/','')

    # Nur für FM
    df.sort_values(by='Year-SOLVER', inplace=True)

    plot_x = 'Year-SOLVER' # 'dimacs-analyzer'  'Year-SOLVER'
    plot_y = 'dimacs-analyzer-time'

    i = 0
    tmp = ""
    # Durch jeden SAT-Solver iterieren und Daten plotten
    for fmmodel, data in df.groupby('dimacs-file'):
        plt.plot(data[plot_x], data[plot_y], marker='o', linestyle='-', label=str(data['Year-DIMACS'].unique()[0]) + "_" + fmmodel)
        i +=1
        tmp = str(data['Year-DIMACS'].unique()[0])

    # Achsenbeschriftungen festlegen
    plt.xlabel('Solver')
    plt.ylabel('Millisekunden')
    plt.xticks(df[plot_x].unique(),rotation=90) 
    if logScale:
        plt.yscale('log')
        plt.ylabel('Millisekunden (log-scaled)')

    plt.grid(True, which="both", ls="--")  # Gitterlinien anzeigen
    plt.title(f'Feature Modell Vergleich ({ReaderStr})')  # Titel des Plots festlegen
    if i == 1:
        plt.title(f"Feature Modell aus Jahr: {tmp}")

    # Plot anzeigen
    plt.tight_layout(rect=[0, 0, 0.7, 1])
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Feature Modell")  # Legende anpassen
    plt.savefig(name)  # Plot speichern
    plt.close()

def all_save_FM(df,filterarg,ordnername):
    """Hilfs Funktion um all-Plots zu saven"""
    df_datei = os.path.join(ordnername, "fm-all"+ f"-{filterarg}.csv")
    df = df[df['dimacs-file'].str.contains(filterarg)]
    if not df.empty:
        # Speichere das Diagramm als csv Datei
        save_csv(df,df_datei)
        plot_all_FM(get_median(df,df_datei),df_datei.replace(".csv",".png"),filterarg)

def save_single_entry_FM(df,filterREADER,filterVersion,ordnername):
    """Hilfsfunktion um einen einzelnen Graph zu speichern als plot und csv"""
    df_mod = df[df['dimacs-file'].str.contains(filterREADER) & (df['dimacs-file'] == filterVersion)]

    #datei_mod = os.path.join(ordnername, filterVersion.split("/")[2].replace(".dimacs","") + f"-{filterREADER}.csv")
    #v6.2[x86]-kconfigreader.csv
    
    
    
    df_mod = df_mod.sort_values(by='dimacs-analyzer')
    if not df_mod.empty:
        tmp = df_mod['Year-DIMACS'].unique()
        datei_mod = os.path.join(ordnername, str(tmp[0]) + f"-{filterREADER}.csv")
        
        save_csv(df_mod,datei_mod)
        plot_all_FM(get_median(df_mod,datei_mod),datei_mod.replace(".csv",".png"),filterREADER)

def mod_FM_all():
    print("Modus FM_all")
    ordnername = "sorted_by_FM"
    create_folder_if_not_exists(ordnername)



    # Die Feature Modell dynamisch laden
    data = load_data_from_csv("solve_model-satisfiable/output.csv")

    #  Füge den Solver das Jahr hinzu
    data['Year-SOLVER'] = data['dimacs-analyzer'].apply(lambda x: convert_short_year(x.split("/")[1].split("-")[0]))

    # Füge eine neue Spalte 'Year' hinzu, um das Jahr zu speichern
    # kconfigreader/linux/v2.5.45[i386].dimacs
    data['Year-DIMACS'] = data['dimacs-file'].apply(lambda x: get_year(x.split("/")[2].split("[")[0]))

    # Exponenten 
    data['analyzer_Exponent'] = data['dimacs-analyzer-time'].apply(lambda x: np.floor(np.log10(x))).astype(int)

   
    # Speicher n der Millisekunden
    data['dimacs-analyzer-time_orig'] = data['dimacs-analyzer-time']

    # Zeit in Millisekunden
    data['dimacs-analyzer-time'] = data['dimacs-analyzer-time'].apply(lambda x: np.divide(x,1000000))

    # FM Modell zu 2024 entfernen
    if remove2024_dimacs:
        data = data[data['Year-DIMACS'] != 2024]
    
    # Remove SAT des Jahres 2023
    if remove2023_solver:
        data = data[data['Year-SOLVER'] != 2023]

    # Einzelne FM Finden
    df2 = data.groupby('dimacs-file').apply(lambda x: x['dimacs-file'].unique())
    # plot_all_FM

    # Alle Solver
    # Alle Plots zusammen fassen
    all_save_FM(data,'kmax',ordnername)
    all_save_FM(data,'kconfigreader',ordnername)

    
    # Durchlaufe jeden Feature Modell
    # Speichere zu jeden Feature Modell die entsprechenden Solver
    # Plotte die dabei erstellte csv Datei als Plot ab. 
    for entry in df2:
        feature_model_version = entry[0]

        # KMAX logic
        save_single_entry_FM(data,'kmax',feature_model_version,ordnername)

        # KCONFIG logic
        save_single_entry_FM(data,'kconfigreader',feature_model_version,ordnername)


        
# Aufruffunktion

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auswahl von Optionen für die Batch-Konvertierung.")
    parser.add_argument("options", type=int, nargs='+', choices=[1, 2], help="1 für geordnet nach Feature Modell, 2 für geordnet nach SAT-Solver")
    parser.add_argument("-rm2024",nargs='?', type=int,help="Soll das FM des Jahr 2024 entfernt werden? True (1) or False (0)")
    parser.add_argument("-rm2023",nargs='?', type=int,help="Soll das SAT-Solver des Jahr 2023 entfernt werden? True (1) or False (0)")
    parser.add_argument("-logscale",nargs='?', type=int,help="Soll die Y-Achse der Diagramm log-scaled sein? True (1) or False (0)")

    args = parser.parse_args()

    start_time = time.time()

    if args.rm2024 is not None:
        if args.rm2024 == 1:
            remove2024_dimacs = True
    
    if args.rm2023 is not None:
        if args.rm2023 == 1:
            remove2023_solver = True
    
    if args.logscale is not None:
        if args.logscale == 1:
            logScale = True


    if args.options is not None:
        for option in args.options:
            if option == 1:
                mod_FM_all()
            elif option == 2:
                mod_SAT_all()

    end_time = time.time()
    execution_time = end_time - start_time
    print("Ausführungszeit:", execution_time, "Sekunden")
 
