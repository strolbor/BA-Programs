import pandas as pd
import matplotlib.pyplot as plt
import os


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

    # Gruppenbildung nach dimacs-analyzer
    groups = df.groupby('dimacs-file')

    # Counter für die Anzahl der Plots
    plot_count = 0

    # Iteration über die Gruppen und Erstellung von Diagrammen
    for name, group in groups:
        if plot_count % 10 == 0:
            # Diagramm speichern
            plt.savefig(os.path.join("sorted_by_SAT", f'sat-{prefix}-tengroup-{plot_count}-{plot_count + 9}.png'), bbox_inches='tight')
            plt.close()
            # Neues Diagramm erstellen
            plt.figure(figsize=(10,6))
        
        plt.plot(group['dimacs-analyzer'], group['dimacs-analyzer-time'], marker='o', label=name)
        
        # Diagrammformatierung
        plt.xlabel('SAT-Solver')
        plt.ylabel('Zeit')
        plt.title(f'Zeit für DIMACS-Analyzer {prefix}')
        plt.xticks(rotation=90)
        
        # Legende außerhalb des Graphen platzieren
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        
        plot_count += 1

    plt.savefig(os.path.join("sorted_by_SAT", f'sat-{prefix}-tengroup-{plot_count}-{plot_count + 9}.png'), bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    tenPlot("sorted_by_SAT/sat-all-kconfigreader-median.csv", 'kconfig')
    tenPlot("sorted_by_SAT/sat-all-kmax-median.csv", 'kmax')
