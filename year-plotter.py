import os
import csv
import matplotlib.pyplot as plt

def plot_csv_files(folder_path):
    if not os.path.isdir(folder_path):
        print("Der angegebene Pfad ist kein Ordner.")
        return
    
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    
    # Durch jede CSV-Datei iterieren
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        
        with open(file_path, 'r') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)
            data = [(int(row[0]), int(row[3])) for row in csv_reader]  # Nur Jahr und dimacs-analyzer-time
        
        # Sortiere die Daten nach Jahren
        data.sort(key=lambda x: x[0])
        years, dimacs_analyzer_time = zip(*data)
        
        # Plot erstellen
        plt.figure(figsize=(10, 6))
        plt.plot(years, dimacs_analyzer_time, marker='o', color='b', linestyle='-')
        plt.grid(True)
        plt.xlabel('Year')
        plt.ylabel('dimacs-analyzer-time (ns)')
        plt.title('dimacs-analyzer-time über die Jahre - {}'.format(csv_file.split(".dimacs")[0]))
        plt.xticks(years)  # Alle Jahre anzeigen
        plt.tight_layout()
        
        # Speichern des Plots als Bild
        plot_name = csv_file.replace('.csv', '_dimacs_analyzer_time_over_years.png')
        plt.savefig(os.path.join(folder_path, plot_name))
        plt.close()

# Beispielaufruf des Programms mit dem Ordnerpfad
folder_path = "verlauf"
plot_csv_files(folder_path)
