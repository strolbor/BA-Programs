import argparse
import csv
import re

# SBVA Extractor


def process_file(input_file, output_file):
    # Datei einlesen
    with open(input_file, 'r') as file:
        data = file.read()

    # Entferne die Escape-Sequenzen
    clean_data = re.sub(r'\^\[\[[0-9;]*m', '', data)

    # Extrahiere relevante Informationen
    pattern = re.compile(
        r'sat-competition/23-sbva_cadical.sh: (\S+)\s+evaluate_command=.*\s+BVA needed: ([\d.]+) secounds\s+Solver needed: ([\d.]+) secounds'
    )
    matches = pattern.findall(clean_data)

    # Speichern in einer CSV-Datei
    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['File', 'BVA Time (seconds)', 'Solver Time (seconds)'])

        for match in matches:
            csvwriter.writerow(match)

    print(f"Die Daten wurden erfolgreich in {output_file} gespeichert.")

def main():
    parser = argparse.ArgumentParser(description="Verarbeitet eine Logdatei und extrahiert BVA- und Solver-Zeiten in eine CSV-Datei.")
    parser.add_argument('input_file', help="Pfad zur Eingabedatei")
    parser.add_argument('output_file', help="Pfad zur Ausgabedatei (CSV)")

    args = parser.parse_args()

    process_file(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
