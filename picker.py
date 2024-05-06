import os
import csv
import sys
import time
import pandas as pd


## Kurzbeschreibung


# Dieses Python-Skript extrahiert und sortiert Daten aus CSV-Dateien nach SAT-Solvern und Feature-Modellen. 
# Es können auch 1 Bulk-Aktion durchgeführt, um alle Daten zu sammeln und zu schreiben.

fmlist = [
        "kconfigreader/linux/v2.5.45[i386].dimacs",
        "kconfigreader/linux/v2.5.54[i386].dimacs",
        "kconfigreader/linux/v2.6.1[i386].dimacs",
        "kconfigreader/linux/v2.6.11[i386].dimacs",
        "kconfigreader/linux/v2.6.15[i386].dimacs",
        "kconfigreader/linux/v2.6.20[i386].dimacs",
        "kconfigreader/linux/v2.6.24[x86].dimacs",
        "kconfigreader/linux/v2.6.29[x86].dimacs",
        "kconfigreader/linux/v2.6.33[x86].dimacs",
        "kconfigreader/linux/v2.6.37[x86].dimacs",
        "kconfigreader/linux/v3.2[x86].dimacs",
        "kconfigreader/linux/v3.8[x86].dimacs",
        "kconfigreader/linux/v3.13[x86].dimacs",
        "kconfigreader/linux/v3.19[x86].dimacs",
        "kconfigreader/linux/v4.4[x86].dimacs",
        "kconfigreader/linux/v4.10[x86].dimacs",
        "kconfigreader/linux/v4.15[x86].dimacs",
        "kconfigreader/linux/v5.0[x86].dimacs",
        "kconfigreader/linux/v5.5[x86].dimacs",
        "kconfigreader/linux/v5.11[x86].dimacs",
        "kconfigreader/linux/v5.16[x86].dimacs",
        "kconfigreader/linux/v6.2[x86].dimacs",
        "kconfigreader/linux/v6.7[x86].dimacs",
        "kmax/linux/v2.5.45[i386].dimacs",
        "kmax/linux/v2.5.54[i386].dimacs",
        "kmax/linux/v2.6.1[i386].dimacs",
        "kmax/linux/v2.6.11[i386].dimacs",
        "kmax/linux/v2.6.15[i386].dimacs",
        "kmax/linux/v2.6.20[i386].dimacs",
        "kmax/linux/v2.6.24[x86].dimacs",
        "kmax/linux/v2.6.29[x86].dimacs",
        "kmax/linux/v2.6.33[x86].dimacs",
        "kmax/linux/v2.6.37[x86].dimacs",
        "kmax/linux/v3.2[x86].dimacs",
        "kmax/linux/v3.8[x86].dimacs",
        "kmax/linux/v3.13[x86].dimacs",
        "kmax/linux/v3.19[x86].dimacs",
        "kmax/linux/v4.4[x86].dimacs",
        "kmax/linux/v4.10[x86].dimacs",
        "kmax/linux/v4.15[x86].dimacs",
        "kmax/linux/v5.0[x86].dimacs",
        "kmax/linux/v5.5[x86].dimacs",
        "kmax/linux/v5.11[x86].dimacs",
        "kmax/linux/v5.16[x86].dimacs",
        "kmax/linux/v6.2[x86].dimacs",
        "kmax/linux/v6.7[x86].dimacs"
    ]

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

def is_kconfigreader(file_path):
    return 'kconfigreader' in file_path

def mod_FM_all():
    print("Modus FM_all")
    ordnername = "sorted_by_FM"
    create_folder_if_not_exists(ordnername)

    data = load_data_from_csv("solve_model-satisfiable/output.csv")

    zahler = 0
    for feature_model_version in fmlist:
        zahler +=1
        # Daten vor der Filterung anzeigen
        print("Daten vor der Filterung:", feature_model_version)

        # KMAX logik
        df_kmax = data[data['dimacs-file'].str.contains('kmax') & (data['dimacs-file'] == feature_model_version)]
        datei_kmax = os.path.join(ordnername, feature_model_version.split("/")[2].replace(".dimacs","") + "-kmax.csv")
        df_kmax = df_kmax.sort_values(by='dimacs-analyzer')
        df_kmax.to_csv(datei_kmax, index=False)

        # KCONFIG logic
        df_kconfigreader = data[data['dimacs-file'].str.contains('kconfigreader') & (data['dimacs-file'] == feature_model_version)]
        datei_kconfig = os.path.join(ordnername, feature_model_version.split("/")[2].replace(".dimacs","") + "-kconfig.csv")
        df_kconfigreader = df_kconfigreader.sort_values(by='dimacs-analyzer')
        df_kconfigreader.to_csv(datei_kconfig, index=False)

    print(zahler)

    # df_sorted = data.sort_values(by=['dimacs-analyzer', 'dimacs-file'])
    # print(df_sorted)


    

    # for feature_model_version in fmlist:
    #     print(feature_model_version)
    #     sorted_data = data.sort_values(by=['dimacs-analyzer','dimacs-file'])
    #     print(sorted_data.head())


 






def main_manuell():
    # Entscheiden was gesucht wird
    print("Willkommen im PArt Picker")
    print("3. Batch für FM Sorted")
    print("4. Batch für SAT Sorted")
    print("0. zum Beenden")

    prompt = "Bitte geben Sie ein Moduscharakter ein: "
    user_input = int(get_valid_input(prompt, is_valid_integer))
    if int(user_input) == 0:
        exit()

    elif user_input == 3:
        mod_FM_all()
    elif user_input == 4:
        pass
        #mod_SAT_all()
    else:
        print("Bitte was verständliches eingeben.")
        main_manuell()

        
# Beispielaufrufe der Funktionen
if __name__ == "__main__":
    if len(sys.argv) != 2:
        main_manuell()
    else:
        start_time = time.time()
        if int(sys.argv[1]) == 3:
            mod_FM_all()
        elif int(sys.argv[1]) == 4:
            pass
            #mod_SAT_all()
        elif int(sys.argv[1]) == 9:
            mod_FM_all()
            #mod_SAT_all()
        end_time = time.time()
        execution_time = end_time - start_time
        print("Ausführungszeit:", execution_time, "Sekunden")



       

   
