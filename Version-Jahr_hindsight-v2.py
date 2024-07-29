import pandas as pd
import matplotlib.pyplot as plt
import os

logScale = True

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

ordnername = "sorted_by_verlauf_handsight"
create_folder_if_not_exists(ordnername)

# Lese die Daten aus den CSV-Dateien
sat_kconfigreader = pd.read_csv("sorted_by_SAT/sat-all-kconfigreader-median.csv")
sat_kmax = pd.read_csv("sorted_by_SAT/sat-all-kmax-median.csv")

def get_best_solver_times(df):
    best_times_list = []
    df = df.sort_values(by=['Year-DIMACS', 'Year-SOLVER'])
    for year in df['Year-DIMACS'].unique():
        df_filtered = df[df['Year-DIMACS'] == year]
        df_filtered = df_filtered[df_filtered['Year-SOLVER'] <= year]
        df_filtered.reset_index().sort_values(by='dimacs-analyzer-time')
        min_time_row = df_filtered.loc[df_filtered['dimacs-analyzer-time'].idxmin()]
        min_time_row['Year-DIMACS'] = year
        best_times_list.append(min_time_row)
    best_times_df = pd.DataFrame(best_times_list)
    return best_times_df

filtered_kmax = get_best_solver_times(sat_kmax)
filtered_kconfig = get_best_solver_times(sat_kconfigreader)

filtered_kconfig.to_csv(os.path.join(ordnername, "Version-Jahr-kconfig.csv"), index=False)
filtered_kmax.to_csv(os.path.join(ordnername, "Version-Jahr-kmax.csv"), index=False)

def combined_plotter(df1, df2, label1, label2):
    plt.figure(figsize=(12, 8))

    solvers1 = df1['dimacs-analyzer'].unique()
    solvers2 = df2['dimacs-analyzer'].unique()
    colors1 = plt.cm.get_cmap('tab20', len(solvers1))
    colors2 = plt.cm.get_cmap('tab20', len(solvers2))

    color_map1 = {solver: colors1(i) for i, solver in enumerate(solvers1)}
    color_map2 = {solver: colors2(i) for i, solver in enumerate(solvers2)}

    plt.plot(df1['Year-DIMACS'], df1['dimacs-analyzer-time'], color='black', linewidth=0.5, linestyle='-', zorder=1, label=f'{label1} line')
    plt.plot(df2['Year-DIMACS'], df2['dimacs-analyzer-time'], color='gray', linewidth=0.5, linestyle='-', zorder=1, label=f'{label2} line')

    for solver in solvers1:
        solver_df = df1[df1['dimacs-analyzer'] == solver]
        plt.scatter(solver_df['Year-DIMACS'], solver_df['dimacs-analyzer-time'], label=f'{label1} - {solver.split("/")[1]}', color=color_map1[solver], zorder=2)

    for solver in solvers2:
        solver_df = df2[df2['dimacs-analyzer'] == solver]
        plt.scatter(solver_df['Year-DIMACS'], solver_df['dimacs-analyzer-time'], label=f'{label2} - {solver.split("/")[1]}', color=color_map2[solver], zorder=2)

    plt.xlabel('Jahr')
    plt.ylabel('Sekunden')
    if logScale:
        plt.yscale('log')
        plt.ylabel('Sekunden (log_10-scaled)')
    plt.title('Zeit vs. FM & Solver aus dem besten Nachjahr')
    plt.xticks(list(set(df1['Year-DIMACS'].unique()).union(set(df2['Year-DIMACS'].unique()))), rotation=90)
    plt.legend(title='Solver', loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True)
    plt.savefig(os.path.join(ordnername, 'Version-Jahr-handsight-combined.png'), bbox_inches='tight')
    plt.savefig(os.path.join(ordnername, 'Version-Jahr-handsight-combined.svg'), bbox_inches='tight')
    #plt.show()

if __name__ == '__main__':
    print("Handsight")
    combined_plotter(filtered_kmax, filtered_kconfig, "kmax", "kconfig")
