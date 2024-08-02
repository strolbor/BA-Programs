import argparse

def search_and_save(file_path, search_strings, output_file):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Datei {file_path} nicht gefunden.")
        return

    matched_lines = []

    for line in lines:
        if any(search_string in line for search_string in search_strings):
            matched_lines.append(line)

    if matched_lines:
        with open(output_file, 'w') as file:
            file.writelines(matched_lines)
        print(f"Gefundene Zeilen wurden in {output_file} gespeichert.")
    else:
        print("Keine Übereinstimmungen gefunden.")

def main():
    parser = argparse.ArgumentParser(description="Suche nach bestimmten Strings in einer Datei und speichere die gefundenen Zeilen in einer anderen Datei.")
    parser.add_argument('input_file', help="Pfad zur Eingabedatei")
    parser.add_argument('output_file', help="Pfad zur Ausgabedatei")
    
    args = parser.parse_args()

    search_strings = ["kconfigreader", "kmax", "BVA", "Solver"]

    search_and_save(args.input_file, search_strings, args.output_file)

if __name__ == "__main__":
    main()
