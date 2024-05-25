import pandas as pd
import matplotlib.pyplot as plt
import os

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

def tenPlot(dateiReadName, prefix):
    # CSV-Datei einlesen
    df = pd.read_csv(dateiReadName)

    # Funktion zum Entfernen des Präfix "kmax/linux/" aus dimacs-file
    def remove_prefix(text, prefix):
        if text.startswith(prefix):
            return text[len(prefix):]
        return text

    # Präfix entfernen und Daten vorbereiten
    df['dimacs-file'] = df['dimacs-file'].apply(lambda x: remove_prefix(x, "kmax/linux/"))
    df['dimacs-file'] = df['dimacs-file'].apply(lambda x: remove_prefix(x, "kconfigreader/linux/"))
    df['dimacs-analyzer'] = df['dimacs-analyzer'].apply(lambda x: remove_prefix(x, "sat-competition/"))
    df['dimacs-file'] = df['dimacs-file'].str.replace('.dimacs', '',regex=False)

    # Nur für SAT
    df.sort_values(by='Year-DIMACS', inplace=True)

    # Gruppenbildung nach dimacs-analyzer
    groups = df.groupby('dimacs-analyzer')

    # Counter für die Anzahl der Plots
    plot_count = 0

    # Iteration über die Gruppen und Erstellung von Diagrammen
    for name, group in groups:
        if plot_count % 10 == 0 and plot_count != 0:
            # Diagramm speichern
            plt.savefig(os.path.join("sorted_by_SAT", f'tengroup-{prefix}-{plot_count}-{plot_count + 9}.png'), bbox_inches='tight')
            plt.close()
            # Neues Diagramm erstellen
            plt.figure(figsize=(10,6))
        
        # dimacs-file == Year-DIMACS
        # dimacs-analyzer == Year-SOLVER  
        plot_x = 'Year-DIMACS' # 'Year-DIMACS' #'dimacs-file'
        plot_y = 'dimacs-analyzer-time'
        # Für SAT
        # - dimacs file / Year-DIMACS
        # - time 
        plt.plot(group[plot_x], group[plot_y], marker='o', label=name) # ist für FM
        
        # Diagrammformatierung
        plt.xlabel('Feature Modell Jahr')
        plt.ylabel('Millisekunden')
        plt.xticks(df[plot_x].unique(),rotation=90) 
        plt.xticks(df[plot_x].unique(),rotation=90) 
        plt.grid(True)
        plt.title(f'Zeit für Sat-Solver ({prefix})')
        
    
        
        # Legende außerhalb des Graphen platzieren
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Solver")
    
        plot_count += 1

    plt.savefig(os.path.join("sorted_by_SAT", f'tengroup-{prefix}-{plot_count}-{plot_count + 9}.png'), bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    print("SAT Plotter")
    tenPlot("sorted_by_SAT/sat-all-kconfigreader-median.csv", 'kconfig')
    tenPlot("sorted_by_SAT/sat-all-kmax-median.csv", 'kmax')
