import pandas as pd
import matplotlib.pyplot as plt
import os

## TODO: 
# Standpunkt: 2010
# min. Zeit nehmen aus den Vorjahren

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


def plotter(df, suffix):
    global ordnername
    plt.figure(figsize=(12, 6))
    plt.scatter(df['Year-DIMACS'], df['dimacs-analyzer-time'], label='Verlauf', color='blue')
    plt.plot(df['Year-DIMACS'], df['dimacs-analyzer-time'], marker='o')
    plt.xlabel('Jahr')
    plt.ylabel('Millisekunden')
    plt.title('Zeit vs. FM & Solver aus dem gleichen Jahr')
    plt.xticks(df['Year-DIMACS'].unique(), rotation=90)  # This ensures all unique years are marked on the x-axis
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True)
    plt.savefig(os.path.join(ordnername, f'Version-Jahr-{suffix}.png'), bbox_inches='tight')

# def plotter(df, suffix):
#     global ordnername
#     plt.figure(figsize=(12, 6))
#     solvers = df['dimacs-file'].unique()
#     colors = plt.cm.get_cmap('tab20', len(solvers))
#     color_map = {solver: colors(i) for i, solver in enumerate(solvers)}
    
#     for solver in solvers:
#         solver_df = df[df['dimacs-file'] == solver]
#         plt.scatter(solver_df['Year-DIMACS'], solver_df['dimacs-analyzer-time'], label=solver_df['Year-DIMACS'].item(), color=color_map[solver])
#         plt.plot(solver_df['Year-DIMACS'], solver_df['dimacs-analyzer-time'], marker='o', linestyle='-', color=color_map[solver])
    
#     plt.xlabel('Jahr')
#     plt.ylabel('Millisekunden')
#     plt.title('Zeit vs. FM & Solver aus dem besten Vor- und Nachjahr')
#     plt.xticks(df['Year-DIMACS'].unique(), rotation=90)  # This ensures all unique years are marked on the x-axis
#     plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#     plt.grid(True)
#     plt.savefig(os.path.join(ordnername, f'Version-Jahr-{suffix}.png'), bbox_inches='tight')


if __name__ == '__main__':
    print("punkt-punkt")
    plotter(filtered_kmax,"kmax")
    plotter(filtered_kconfig,"kconfig")



