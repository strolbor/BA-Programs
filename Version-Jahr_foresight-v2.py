import pandas as pd
import matplotlib.pyplot as plt
import os


logScale = True
secDiv = 1000000000 # Sekunden

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
        # Filtere die Daten bis einschließlich des aktuellen Jahres
        df_filtered = df[df['Year-DIMACS'] == year]
        
        # Finde die Zeile mit der minimalen Solverzeit unter den Einträgen bis einschließlich des aktuellen Jahres
        min_time_row = df_filtered.loc[df_filtered['dimacs-analyzer-time'].idxmin()]
        
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

def plotter(df1, df2, label1, label2):
    global ordnername
    plt.figure(figsize=(10, 6))

    solvers1 = df1['dimacs-analyzer'].unique()
    solvers2 = df2['dimacs-analyzer'].unique()
    colors = plt.cm.get_cmap('tab20', len(solvers1) + len(solvers2))
    color_map = {solver: colors(i) for i, solver in enumerate(list(solvers1) + list(solvers2))}
    
    # Zeichne die durchgehende Linie für df1
    plt.plot(df1['Year-DIMACS'], df1['dimacs-analyzer-time'], color='black', linewidth=0.5, linestyle='-', zorder=1, label=f'{label1} - Line')
    
    # Zeichne die Punkte in verschiedenen Farben für df1
    for solver in solvers1:
        solver_df = df1[df1['dimacs-analyzer'] == solver]
        plt.scatter(solver_df['Year-DIMACS'], solver_df['dimacs-analyzer-time'], label=f'{label1} - {solver.split("/")[1]}', color=color_map[solver], zorder=2)
    
    # Zeichne die durchgehende Linie für df2
    plt.plot(df2['Year-DIMACS'], df2['dimacs-analyzer-time'], color='grey', linewidth=0.5, linestyle='-', zorder=1, label=f'{label2} - Line')
    
    # Zeichne die Punkte in verschiedenen Farben für df2
    for solver in solvers2:
        solver_df = df2[df2['dimacs-analyzer'] == solver]
        plt.scatter(solver_df['Year-DIMACS'], solver_df['dimacs-analyzer-time'], label=f'{label2} - {solver.split("/")[1]}', color=color_map[solver], zorder=2)
    
    plt.xlabel('Jahr')
    plt.ylabel('Sekunden')
    if logScale:
        plt.yscale('log')
        plt.ylabel('Sekunden (log_10-scaled)')
    plt.title('Zeit vs. FM & Solver (Foresight)')
    plt.xticks(sorted(set(df1['Year-DIMACS']).union(set(df2['Year-DIMACS']))), rotation=90)  # Ensures all unique years are marked on the x-axis
    plt.legend(title='Solver', loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True)
    plt.savefig(os.path.join(ordnername, 'Version-Jahr-foresight-combined.png'), bbox_inches='tight')
    plt.savefig(os.path.join(ordnername, 'Version-Jahr-foresight-combined.svg'), bbox_inches='tight')

if __name__ == '__main__':
    print("Foresight")
    plotter(filtered_kmax, filtered_kconfig, "kmax", "kconfig")
