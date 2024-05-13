import pandas as pd
import matplotlib.pyplot as plt
import os


def tenPlot(dateiReadName,prefix):
    # CSV-Datei einlesen
    #df = pd.read_csv("")

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

    # Nur für FM
    df.sort_values(by='Year-SOLVER', inplace=True)


    # Gruppenbildung nach dimacs-analyzer
    groups = df.groupby('dimacs-file')

    # Counter für die Anzahl der Plots
    plot_count = 0

    # Iteration über die Gruppen und Erstellung von Diagrammen
    for name, group in groups:
        if plot_count % 10 == 0 and plot_count != 0:
            # Diagramm speichern
            plt.savefig(os.path.join("sorted_by_FM",f'tengroup-{plot_count}-{plot_count + 9}-{prefix}.png'), bbox_inches='tight')
            plt.close()
            # Neues Diagramm erstellen
            plt.figure(figsize=(10,6))


        # dimacs-file == Year-DIMACS
        # dimacs-analyzer == Year-SOLVER  
        plot_x = 'Year-SOLVER'
        plot_y = 'dimacs-analyzer-time'
        # Für FM:
        # - dimacs analyzer / Year-SOLVER 
        # - Time
        #plt.plot(group['Year-DIMACS'], group['dimacs-analyzer-time'], marker='o', label=name)
        plt.plot(group[plot_x], group[plot_y], marker='o', label=name) # ist für SAT


        # Diagrammformatierung
        plt.xlabel('Feature Modell Jahr')
        plt.ylabel('Nanosekunden')
        plt.title(f'Zeit für SAT-Solver ({prefix})')
        plt.xticks(df[plot_x].unique(),rotation=90) 
        plt.grid(True)
        
        # Legende außerhalb des Graphen platzieren
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Solver")
        
        plot_count += 1

    plt.savefig(os.path.join("sorted_by_FM",f'tengroup-{plot_count}-{plot_count + 9}-{prefix}.png'), bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    tenPlot("sorted_by_FM/fm-all-kconfigreader-median.csv",'kconfig')
    tenPlot("sorted_by_FM/fm-all-kmax-median.csv",'kmax')