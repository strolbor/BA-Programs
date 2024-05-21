import pandas as pd
import matplotlib.pyplot as plt
import os

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

ordnername = "sorted_by_verlauf_foresight"
create_folder_if_not_exists(ordnername)

# Lese die Daten aus den CSV-Dateien
sat_kconfigreader = pd.read_csv("sorted_by_SAT/sat-all-kconfigreader-median.csv")
sat_kmax = pd.read_csv("sorted_by_SAT/sat-all-kmax-median.csv")

def get_best_solver_times(df):
    # Initialisiere eine leere Liste für die besten Zeiten
    best_times_list = []
    
    # Sortiere den DataFrame nach Year-DIMACS und Year-SOLVER
    df = df.sort_values(by=['Year-DIMACS', 'Year-SOLVER'])
    
    # Iteriere über die einzigartigen Jahre der DIMACS-Daten
    for year in df['Year-DIMACS'].unique():
        # Filtere die Daten bis zum aktuellen Jahr
        print(year)


        # Wir erhalten alle Ergebnisse zu einen FM-Modell
        df_filtered = df[df['Year-DIMACS'] == year]
        
        # Wir filtern Ergebnisse nach den SOLVER bis zum JAhr x
        #df_filtered = df_filtered[df_filtered['Year-SOLVER'] <= year]

        df_filtered.reset_index().sort_values(by='dimacs-analyzer-time')
        
        # Finde die Zeile mit der minimalen Solverzeit
        min_time_row = df_filtered.loc[df_filtered['dimacs-analyzer-time'].idxmin()]
        
        
        # Aktualisiere das Jahr des DIMACS mit dem aktuellen Jahr
        min_time_row['Year-DIMACS'] = year
        
        # Füge diese Zeile der Liste hinzu
        best_times_list.append(min_time_row)
    
    # Erstelle einen DataFrame aus der Liste der besten Zeiten
    best_times_df = pd.DataFrame(best_times_list)
    
    return best_times_df

# Wende die Funktion auf die beiden DataFrames an
filtered_kmax = get_best_solver_times(sat_kmax)
filtered_kconfig = get_best_solver_times(sat_kconfigreader)

# Speichern als CSV
filtered_kconfig.to_csv(os.path.join(ordnername, "Version-Jahr-kconfig.csv"), index=False)
filtered_kmax.to_csv(os.path.join(ordnername, "Version-Jahr-kmax.csv"), index=False)

def plotter(df, suffix):
    global ordnername
    plt.figure(figsize=(12, 6))
    plt.scatter(df['Year-DIMACS'], df['dimacs-analyzer-time'], label='Verlauf', color='blue')
    plt.plot(df['Year-DIMACS'], df['dimacs-analyzer-time'], marker='o')
    plt.xlabel('Jahr')
    plt.ylabel('Nanosekunden')
    plt.title('Zeit vs. FM & Solver aus dem besten Vorjahr')
    plt.xticks(df['Year-DIMACS'].unique(), rotation=90)  # This ensures all unique years are marked on the x-axis
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True)
    plt.savefig(os.path.join(ordnername, f'Version-Jahr-{suffix}.png'), bbox_inches='tight')

plotter(filtered_kmax, "kmax")
plotter(filtered_kconfig, "kconfig")
