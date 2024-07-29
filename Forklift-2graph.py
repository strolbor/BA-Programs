import pandas as pd
import matplotlib.pyplot as plt
import os

logScale = True


# Lese die Daten aus den CSV-Dateien
df1 = pd.read_csv("sorted_by_SAT/03-Forklift-kconfigreader-median.csv")
df2 = pd.read_csv("sorted_by_SAT/03-Forklift-kmax-median.csv")

df1 = df1.sort_values(by=['Year-DIMACS', 'Year-SOLVER'])
df2 = df2.sort_values(by=['Year-DIMACS', 'Year-SOLVER'])



def plotter():
    global df1, df2
    plt.figure(figsize=(12, 6))
    



    plt.scatter(df1['Year-DIMACS'], df1['dimacs-analyzer-time'], label='KConfigReader', color='blue')
    plt.plot(df1['Year-DIMACS'], df1['dimacs-analyzer-time'], marker='o', color='blue')

    plt.scatter(df2['Year-DIMACS'], df2['dimacs-analyzer-time'], label='KMAX', color='red')
    plt.plot(df2['Year-DIMACS'], df2['dimacs-analyzer-time'], marker='o', color='red')


    plt.xlabel('Jahr')
    plt.ylabel('Sekunden')
    if logScale:
        plt.yscale('log')
        plt.ylabel('Sekunden (log_10-scaled)')
    plt.title('Forklift')
    plt.xticks(df1['Year-DIMACS'].unique(), rotation=90)  # This ensures all unique years are marked on the x-axis
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True)
    plt.savefig(os.path.join("sorted_by_SAT",f'forklift.png'), bbox_inches='tight')
    plt.savefig(os.path.join("sorted_by_SAT",f'forklift.svg'), bbox_inches='tight')


if __name__ == '__main__':
    print("forklift")
    plotter()



