import os
import csv


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


# Funktion um Ordner zu holen
def get_folders():
    folders = []
    folders = [folder for folder in os.listdir() if folder.startswith("solve_sat-") and os.path.isdir(folder)]
    return folders

# Funktion zum Laden der Daten für eine bestimmte Version des Feature-Modells
def load_data_for_feature_model_version(feature_model_version):
    data_dict = {}

    # Suche nach Ordnern, die mit "solve_sat_" beginnen
    folders = get_folders()
    
    for folder in folders:
        csv_path = os.path.join(folder, 'output.csv')
        if os.path.exists(csv_path):
            with open(csv_path, 'r') as file:
                csv_reader = csv.DictReader(file, delimiter=',')
                data = list(csv_reader)
                data_dict[folder] = data


    # Filtern der Daten für die angegebene Version des Feature-Modells
    filtered_data = {}
    for solver, data in data_dict.items():
        for row in data:
            if row['dimacs-file'].startswith(feature_model_version):
                if solver in filtered_data:
                    filtered_data[solver].append(row)
                else:
                    filtered_data[solver] = [row]

    return filtered_data

# Funktion zum Laden der Daten für einen bestimmten SAT-Solver
def load_data_for_solver(solver_name):
    data_dict = {}

    # Suche nach Ordnern, die mit "solve_sat_" beginnen
    folders = get_folders()

    for folder in folders:
        csv_path = os.path.join(folder, 'output.csv')
        if os.path.exists(csv_path):
            with open(csv_path, 'r') as file:
                csv_reader = csv.DictReader(file, delimiter=',')
                data = list(csv_reader)
                data_dict[folder] = data
    
    #print(data_dict)

    # Filtern der Daten für den angegebenen SAT-Solver
    filtered_data = {}
    for solver, data in data_dict.items():
        if str(solver).endswith(solver_name):
            filtered_data[solver_name] =data # data
        

    #print("FD",filtered_data)
    return filtered_data

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

def is_valid_str(input_str):
    return isinstance(input_str, str) and len(input_str) > 0

def find_matching_entry(array, prefix):
    for entry in array:
        if entry.startswith(prefix):
            return entry
    return None

def printerFM(dateiname,feature_model_version,data_for_feature_model):
    file_out = open(dateiname,"w")
    tmp = "FM-Modell: " + feature_model_version
    file_out.write("dimacs-analyzer,dimacs-analyzer-time,statisfiable,"+tmp+"\n")
    for solver,data in data_for_feature_model.items():
        tmpSTR = "{},{},{}".format(data[0]["dimacs-analyzer"].split("/")[1],data[0]["dimacs-analyzer-time"],"satisfiable" if bool(data[0]["model-satisfiable"]) == True else "not satisfiable")
        #tmpSTR = data[0]["dimacs-analyzer"].split("/")[1] +","+ data[0]["dimacs-analyzer-time"] + "satisfiable" if bool(data[0]["model-satisfiable"]) == True else "not satisfiable"
        print("> ",tmpSTR)
        file_out.write(tmpSTR+""+"\n")
    file_out.flush()
    file_out.close()



def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


"""Diese Funktion sucht und schreibt die Sachen für mod_SAT"""
def mod_sat_write(matching,dateinameI368,dateinameX86,dateinameALL):    
    solver_name =matching #= "02-zchaff"
    data_for_solver = load_data_for_solver(solver_name)
    #print("Sat-Solver:",solver_name)

    file = open(dateinameI368,"w")
    file2 = open(dateinameX86,"w")
    file3 = open(dateinameALL,"w")
    toWrite0 = "dimacs-analyzer,version,dimacs-analyzer-time,statisfiable,"+solver_name+"\n"
    file.write(toWrite0)
    file2.write(toWrite0)
    file3.write(toWrite0)

    for solver,data in data_for_solver.items():
        for item in data:
            towrite = ""+ \
                item["dimacs-file"] + "," \
                + str(item["dimacs-file"]).split("/")[2].split(".")[0] + "," \
                + item["dimacs-analyzer-time"] + ","  \
                + "satisfiable\n" if bool(item["model-satisfiable"]) == True else "not satisfiable\n"
            if "[i386]" in item["dimacs-file"]:
                file.write(towrite) 
            elif "[x86]" in item["dimacs-file"]:
                file2.write(towrite)
            else:
                print("unknow typ: "+item["dimacs-file"]) 
            file3.write(towrite)
    file.flush()
    file.close()
    file2.flush()
    file2.close()
    file3.flush()
    file3.close()

# HAupt Funktionen des Programmes

def mod_FM():
    i = 0
    print("Verfügbare FM Models")
    for entry in fmlist:
        print(">",i,entry)
        i+=1
    
    promt = "Bitte wählen sie den Index für das Modell"
    tmp = get_valid_input(promt,is_valid_integer)
    tmp = int(tmp)

    if tmp > len(fmlist):
        print("Zu großer Wert.")
        exit()


    feature_model_version = fmlist[tmp]
    #feature_model_version = "kconfigreader/linux/v2.5.45[i386].dimacs"
    

    data_for_feature_model = load_data_for_feature_model_version(feature_model_version)
    printerFM('FM-sort.csv',feature_model_version,data_for_feature_model)

    print("\n")




def mod_FM_all():
    ordnername = "sorted_by_FM"
    create_folder_if_not_exists(ordnername)

    for entry in fmlist:
        feature_model_version = entry
        data_for_feature_model = load_data_for_feature_model_version(feature_model_version)

        filename = feature_model_version.replace("/","-")
        dateiname = os.path.join(ordnername,f'{filename}.csv')

        printerFM(dateiname,feature_model_version,data_for_feature_model)
        

def mod_SAT():
    ordnername = "sorted_by_SAT"
    create_folder_if_not_exists(ordnername)

    # Sat Solvern suchen
    folders = get_folders()
    print("Verfügbare Sat-Solvern")
    for item in folders:
        print(item.split('_')[2],end=',')
    print("\n")

    # Eingabe vom User erwarten
    promt = "Bitte geben sie den Anfang der Eintrags an (also die zweistellige Jahr)"
    tmp = get_valid_input(promt,is_valid_str)
    find_user_input = "solve_sat-competition_" + tmp

    # MAtching finden
    matching = find_matching_entry(folders,find_user_input)

    print("\n")
    datei1 = os.path.join(ordnername,f"{matching}-i386.csv") # Datei für i386
    datei2 = os.path.join(ordnername,f"{matching}-x86.csv") # Datei für x86
    datei3 = os.path.join(ordnername,f"{matching}-all.csv") # Datei für alles
    mod_sat_write(matching,datei1,datei2,datei3)

def mod_SAT_all():
    ordnername = "sorted_by_SAT"
    create_folder_if_not_exists(ordnername)
    # Sat Solvern suchen
    folders = get_folders()
    for folder in folders:
        datei1 = os.path.join(ordnername,f"{folder}-i386.csv") # Datei für i386
        datei2 = os.path.join(ordnername,f"{folder}-x86.csv") # Datei für x86
        datei3 = os.path.join(ordnername,f"{folder}-all.csv") # Datei für alles
        mod_sat_write(folder,datei1,datei2,datei3)







def main():
    # Entscheiden was gesucht wird
    print("Willkommen im PArt Picker")
    print("1. Modus: nach FM sortieren")
    print("2. Modus: nach SAT-Solver sortieren")
    print("3. Batch für FM Sorted")
    print("4. BAtch für SAT Sorted")
    print("0. zum Beenden")

    prompt = "Bitte geben Sie ein Moduscharakter ein: "
    user_input = int(get_valid_input(prompt, is_valid_integer))
    if int(user_input) == 0:
        exit()
    elif user_input == 1:
        # FM soprtierung
        mod_FM()
    elif user_input == 2:
        # SAT sortierung
        mod_SAT()
    elif user_input == 3:
        mod_FM_all()
    elif user_input == 4:
        mod_SAT_all()
    else:
        print("Bitte was verständliches eingeben.")
        main()

        
# Beispielaufrufe der Funktionen
if __name__ == "__main__":
    main()

       

   
