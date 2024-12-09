import re
import csv
import sys

def parse_log(file_path):
    data_list = []
    current_data = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('evaluate_command'):
                if current_data:
                    data_list.append(current_data)
                    current_data = {}
                current_data['evaluate_command'] = line.split('=')[1].strip()
            elif line.startswith('c all_cubes='):
                match = re.search(r'c all_cubes=(\d+), max_base_size=(\d+),final_cubes_nb=(\d+)', line)
                if match:
                    current_data['all_cubes'] = int(match.group(1))
                    current_data['max_base_size'] = int(match.group(2))
                    current_data['final_cubes_nb'] = int(match.group(3))
            elif line.startswith('c nb_BCPs='):
                match = re.search(r'c nb_BCPs=(\d+), nb_left_subst=(\d+), nb_right_subst=(\d+)', line)
                if match:
                    current_data['nb_BCPs'] = int(match.group(1))
                    current_data['nb_left_subst'] = int(match.group(2))
                    current_data['nb_right_subst'] = int(match.group(3))
            elif line.startswith('evaluate_time='):
                match = re.search(r'evaluate_time=([\d.]+)', line)
                if match:
                    current_data['time'] = float(match.group(1))
        if current_data:
            data_list.append(current_data)

    return data_list

def write_to_csv(data_list, csv_file_path):
    fieldnames = ['evaluate_command', 'all_cubes', 'max_base_size', 'final_cubes_nb', 'nb_BCPs', 'nb_left_subst', 'nb_right_subst', 'time']
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in data_list:
            writer.writerow({
                'evaluate_command': data.get('evaluate_command', 'N/A'),
                'all_cubes': data.get('all_cubes', 'N/A'),
                'max_base_size': data.get('max_base_size', 'N/A'),
                'final_cubes_nb': data.get('final_cubes_nb', 'N/A'),
                'nb_BCPs': data.get('nb_BCPs', 'N/A'),
                'nb_left_subst': data.get('nb_left_subst', 'N/A'),
                'nb_right_subst': data.get('nb_right_subst', 'N/A'),
                'time': data.get('time', 'N/A')
            })

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_log_file>")
        sys.exit(1)

    log_file_path = sys.argv[1]
    csv_file_path = sys.argv[1].replace(".log","-re.csv")

    # Daten aus der Logdatei extrahieren
    parsed_data_list = parse_log(log_file_path)

    # Extrahierte Daten in eine CSV-Datei schreiben
    write_to_csv(parsed_data_list, csv_file_path)

    print(f'Daten wurden erfolgreich in {csv_file_path} geschrieben.')
