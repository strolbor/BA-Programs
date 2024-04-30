import os
import csv
import matplotlib.pyplot as plt

def plot_csv_files(folder_path):
    # Überprüfen, ob der angegebene Pfad ein Ordner ist
    if not os.path.isdir(folder_path):
        print("Der angegebene Pfad ist kein Ordner.")
        return
    
    # Eine Liste für alle CSV-Dateien im Ordner erstellen
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    
    # Durch jede CSV-Datei iterieren
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        
        # CSV-Datei einlesen und die letzte Spalte ignorieren
        with open(file_path, 'r') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)  # Überspringe die Kopfzeile
            data = [(row[0], int(row[1].split()[0])) for row in csv_reader]  # Nur die ersten beiden Spalten werden berücksichtigt
        
        # Extrahiere die sortierten Daten in separate Listen
        solver_names, dimacs_analyzer_time = zip(*data)
        
        # Sortiere die Daten nach den Anfangszahlen der Solver-Namen
        sorted_data = sorted(zip(solver_names, dimacs_analyzer_time), key=lambda x: int(x[0].split('-')[0]))
        solver_names, dimacs_analyzer_time = zip(*sorted_data)
        
        # Plotten der Daten als Linienplot
        plt.figure(figsize=(12, 6))
        plt.plot(solver_names, dimacs_analyzer_time, marker='o')
        plt.xlabel('Solver Name')
        plt.ylabel('dimacs-analyzer-time (ns)')
        plt.title(f'Plot für {csv_file}')
        plt.xticks(rotation=90)
        plt.tight_layout()
        
        # Speichern des Plots als Bild
        plot_name = csv_file.replace('.csv', '_line_plot.png')
        plt.savefig(os.path.join(folder_path, plot_name))
        plt.close()

# Beispielaufruf des Programms mit dem Ordnerpfad
folder_path = "sorted_by_FM"
plot_csv_files(folder_path)
