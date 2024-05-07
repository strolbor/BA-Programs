import os
import csv
import sys
import time
import pandas as pd

import matplotlib.pyplot as plt

## Kurzbeschreibung


# Dieses Python-Skript extrahiert und sortiert Daten aus CSV-Dateien nach SAT-Solvern und Feature-Modellen. 
# Es können auch 1 Bulk-Aktion durchgeführt, um alle Daten zu sammeln und zu schreiben.


def get_valid_input(prompt, validation_func):
    while True:
        user_input = input(prompt)
        if validation_func(user_input):
            return user_input
        else:
            print("Ungültige Eingabe. Bitte versuchen Sie es erneut.")

# Beispiel für eine Validierungsfunktion
def is_valid_integer(input_str):
    try:
        int_value = int(input_str)
        return True
    except ValueError:
        return False


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




MODUS_FM = 1
MODUS_SAT = 2

def plot_single_SAT(df, name):
    df['dimacs-file'] = df['dimacs-file'].str.replace('kconfigreader/linux/', '')
    df['dimacs-file'] = df['dimacs-file'].str.replace('kmax/linux/', '')
    df['dimacs-file'] = df['dimacs-file'].str.replace('.dimacs', '',regex=False)
    df['dimacs-analyzer'] = df['dimacs-analyzer'].str.replace('sat-competition/','')


    # Plot erstellen
    plt.figure(figsize=(10, 6))
    for solver, data in df.groupby('dimacs-analyzer'):
        plt.plot(data['dimacs-file'], data['dimacs-analyzer-time'], marker='o', linestyle='-', label=solver)
    plt.xlabel('Feature Modell')
    plt.ylabel('Zeit in ns')
    plt.title("Geordnet nach Solver: " + name.split("/")[1])
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()

    plt.savefig(os.path.join(name))
    plt.close()

def plot_single_FM(df, name):
    df['dimacs-file'] = df['dimacs-file'].str.replace('kconfigreader/linux/', '')
    df['dimacs-file'] = df['dimacs-file'].str.replace('kmax/linux/', '')
    df['dimacs-file'] = df['dimacs-file'].str.replace('.dimacs', '',regex=False)
    df['dimacs-analyzer'] = df['dimacs-analyzer'].str.replace('sat-competition/','')


    # Plot erstellen
    plt.figure(figsize=(10, 6))

    for solver, data in df.groupby('dimacs-file'):
        plt.plot(data['dimacs-analyzer'], data['dimacs-analyzer-time'], marker='o', linestyle='-', label=solver)
    plt.xlabel('dimacs-analyzer')
    plt.ylabel('Zeit in ns')
    plt.title(name.split("/")[1])
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()

    plt.savefig(os.path.join(name))
    plt.close()

def plot_all_SAT(df,name):
        # Plot erstellen
    plt.figure(figsize=(12, 6))

    # Farben für die Linien im Plot definieren
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

    df['dimacs-file'] = df['dimacs-file'].str.replace('kconfigreader/linux/', '', regex=False)
    df['dimacs-file'] = df['dimacs-file'].str.replace('kmax/linux/', '', regex=False)
    df['dimacs-file'] = df['dimacs-file'].str.replace('.dimacs', '', regex=False)
    df['dimacs-analyzer'] = df['dimacs-analyzer'].str.replace('sat-competition/','')

    solver_groups = df.groupby('dimacs-analyzer')

    # Durch jeden SAT-Solver iterieren und Daten plotten
    for i, (solver, data) in enumerate(solver_groups):
        plt.plot(data['dimacs-file'], data['dimacs-analyzer-time'], label=solver, color=colors[i % len(colors)], marker='o', linestyle='-')

    # Achsenbeschriftungen festlegen
    plt.xlabel('Feature Modell')
    plt.ylabel('Benötigte Zeit')
    plt.xticks(rotation=90)  # x-Achsenbeschriftungen vertikal ausrichten
    #plt.yscale('log')  # Logarithmische Skala für die y-Achse verwenden
    plt.grid(True, which="both", ls="--")  # Gitterlinien anzeigen
    plt.title('SAT Solvern Vergleich')  # Titel des Plots festlegen

    # Plot anzeigen
    plt.tight_layout(rect=[0, 0, 0.7, 1])
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Solver")  # Legende anpassen
    plt.savefig(name)  # Plot speichern
    plt.close()

def plot_all_FM(df,name):
        # Plot erstellen
    plt.figure(figsize=(12, 6))

    # Farben für die Linien im Plot definieren
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

    df['dimacs-file'] = df['dimacs-file'].str.replace('kconfigreader/linux/', '')
    df['dimacs-file'] = df['dimacs-file'].str.replace('kmax/linux/', '')
    df['dimacs-file'] = df['dimacs-file'].str.replace('.dimacs', '',regex=False)
    df['dimacs-analyzer'] = df['dimacs-analyzer'].str.replace('sat-competition/','')


    # Durch jeden SAT-Solver iterieren und Daten plotten
    for solver, data in df.groupby('dimacs-file'):
        plt.plot(data['dimacs-analyzer'], data['dimacs-analyzer-time'], marker='o', linestyle='-', label=solver)

    # Achsenbeschriftungen festlegen
    plt.xlabel('Solver')
    plt.ylabel('Benötigte Zeit')
    plt.xticks(rotation=90)  # x-Achsenbeschriftungen vertikal ausrichten
    #plt.yscale('log')  # Logarithmische Skala für die y-Achse verwenden
    plt.grid(True, which="both", ls="--")  # Gitterlinien anzeigen
    plt.title('Feature Modell Vergleich')  # Titel des Plots festlegen

    # Plot anzeigen
    plt.tight_layout(rect=[0, 0, 0.7, 1])
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Solver")  # Legende anpassen
    plt.savefig(name)  # Plot speichern
    plt.close()


def get_median(df : pd.core.frame.DataFrame,name):
    """Diese Funktion filtert, den Median heraus.
    Tauscht Endung .csv mit -median.csv aus"""
    name = name.replace(".csv","-median.csv")
    # Alte Variante
    # df = df.sort_values(by=['dimacs-analyzer','dimacs-file'])
    # #df = df[df['iteration'] == 3]
    # # # TODO: nach den mathematischen Median suchen - ohne die Iteration spalte beachten
    # name = name.replace(".csv","-median.csv")

    # save_csv(df,name)
    # return df

    # DataFrame nach "dimacs-analyzer-time" sortieren
    sorted_df = df.sort_values(by='dimacs-analyzer-time')

    # Gruppieren nach ['dimacs-analyzer', 'dimacs-file'] und Median berechnen
    median_grouped = sorted_df.groupby(['dimacs-analyzer', 'dimacs-file']).median()
    median_grouped.to_csv(name)
    # man muss es neu einlesen, sonst kommt ein Fehler
    # kp warum
    turn_df = pd.read_csv(name)
    return turn_df


def save_csv(df,name):
    """speichert das DataFrame in eine csv Datei"""
    df.to_csv(name,index=False)



# Hauptfunktionen

def all_save_SAT(df,filterReader,ordnername):
    datei_mod = os.path.join(ordnername, "sat-all"+ f"-{filterReader}.csv")
    df = df[df['dimacs-file'].str.contains(filterReader)]
    if not df.empty:
        # alle Daten speichern ohne Median Filter
        save_csv(df,datei_mod)

        # Bild plotten
        plot_all_SAT(get_median(df,datei_mod),datei_mod.replace(".csv",".png"))

def save_single_entry_SAT(df,filterReader, filterVersion, ordnername):
    df = df[df['dimacs-file'].str.contains(filterReader) & (df['dimacs-analyzer'] == filterVersion)]
    # sat-competition/07-RSat
    datei_mod = os.path.join(ordnername, filterVersion.split("/")[1]+ f"-{filterReader}.csv")
    df = df.sort_values(by='dimacs-file')
    if not df.empty:
        save_csv(df,datei_mod)
        plot_single_SAT(get_median(df,datei_mod),datei_mod.replace(".csv",".png"))

def mod_SAT_all():
    print("Modus SAT_all")
    ordnername = "sorted_by_SAT"
    create_folder_if_not_exists(ordnername)

    # Die Feature Modell dynamisch laden
    data = load_data_from_csv("solve_model-satisfiable/output.csv")
    df2 = data.groupby('dimacs-analyzer').apply(lambda x: x['dimacs-analyzer'].unique())

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
    

def all_save_FM(df,filterarg,ordnername):
    """Hilfs Funktion um all-Plots zu saven"""
    df_datei = os.path.join(ordnername, "fm-all"+ f"-{filterarg}.csv")
    df = df[df['dimacs-file'].str.contains(filterarg)]
    if not df.empty:
        save_csv(df,df_datei)
        plot_all_FM(get_median(df,df_datei),df_datei.replace(".csv",".png"))

def save_single_entry_FM(df,filterREADER,filterVersion,ordnername):
    """Hilfsfunktion um einen einzelnen Graph zu speichern als plot und csv"""
    df_mod = df[df['dimacs-file'].str.contains(filterREADER) & (df['dimacs-file'] == filterVersion)]
    datei_mod = os.path.join(ordnername, filterVersion.split("/")[2].replace(".dimacs","") + f"-{filterREADER}.csv")
    
    df_mod = df_mod.sort_values(by='dimacs-analyzer')
    if not df_mod.empty:
        save_csv(df_mod,datei_mod)
        plot_all_FM(get_median(df_mod,datei_mod),datei_mod.replace(".csv",".png"))

def mod_FM_all():
    print("Modus FM_all")
    ordnername = "sorted_by_FM"
    create_folder_if_not_exists(ordnername)



    # Die Feature Modell dynamisch laden
    data = load_data_from_csv("solve_model-satisfiable/output.csv")
    df2 = data.groupby('dimacs-file').apply(lambda x: x['dimacs-file'].unique())

    zahler = 0

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
        zahler +=1

        # KMAX logic
        save_single_entry_FM(data,'kmax',feature_model_version,ordnername)

        # KCONFIG logic
        save_single_entry_FM(data,'kconfigreader',feature_model_version,ordnername)

    print("zahler",zahler)


def main_manuell():
    # Entscheiden was gesucht wird
    print("Willkommen im PArt Picker")
    print("1. Batch für FM Sorted")
    print("2. Batch für SAT Sorted")
    print("0. zum Beenden")

    prompt = "Bitte geben Sie ein Moduscharakter ein: "
    user_input = int(get_valid_input(prompt, is_valid_integer))
    if int(user_input) == 0:
        exit()

    elif user_input == 1:
        mod_FM_all()
    elif user_input == 2:
        mod_SAT_all()
    else:
        print("Bitte was verständliches eingeben.")
        main_manuell()

        
# Beispielaufrufe der Funktionen
if __name__ == "__main__":
    if len(sys.argv) != 2:
        main_manuell()
    else:
        start_time = time.time()
        if int(sys.argv[1]) == 1:
            mod_FM_all()
        elif int(sys.argv[1]) == 2:
            pass
            mod_SAT_all()
        elif int(sys.argv[1]) == 9:
            mod_FM_all()
            mod_SAT_all()
        end_time = time.time()
        execution_time = end_time - start_time
        print("Ausführungszeit:", execution_time, "Sekunden")



       

   
