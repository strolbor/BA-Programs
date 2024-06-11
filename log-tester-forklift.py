import pandas as pd
import re

# Pfad zur Eingabedatei
input_file = 'Forklift-output.min.log'
output_file = 'extracted_sat_data.csv'

# Datenstrukturen zum Speichern der extrahierten Informationen
data = {
    "evaluate_command": [],
    "year": [],
    "number_of_variables": [],
    "max_tree_depth": [],
    "max_cub_gen": [],
    "nb_BCPs": [],
    "nb_left_subst": [],
    "nb_right_subst": []
}

# Regex-Muster zur Extraktion der gewünschten Informationen
patterns = {
    "evaluate_command": r'evaluate_command=([^\n]+)',
    "number_of_variables": r'number of variables=(\d+)',
    "max_tree_depth": r'max_tree_depth=(\d+), max_cub_gen=(\d+)',
    "nb_BCPs": r'nb_BCPs=(\d+), nb_left_subst=(\d+), nb_right_subst=(\d+)'
}

# Mapping von Linux-Versionen zu Jahren
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

# Funktion zur Extraktion der Version aus dem evaluate_command
def extract_version(command):
    match = re.search(r'v\d+\.\d+(\.\d+)?', command)
    if match:
        return match.group(0)
    return None

# Datei einlesen und Zeilenweise verarbeiten
with open(input_file, 'r') as file:
    content = file.read()
    evaluate_commands = re.findall(patterns["evaluate_command"], content)
    variables = re.findall(patterns["number_of_variables"], content)
    tree_depths = re.findall(patterns["max_tree_depth"], content)
    subst_info = re.findall(patterns["nb_BCPs"], content)

    for command in evaluate_commands:
        version = extract_version(command)
        year = linux_versions.get(version, 'Unknown')
        data["evaluate_command"].append(command)
        data["year"].append(year)
        
    data["number_of_variables"].extend(variables)
    for depth, cub_gen in tree_depths:
        data["max_tree_depth"].append(depth)
        data["max_cub_gen"].append(cub_gen)
    for bcp, left_subst, right_subst in subst_info:
        data["nb_BCPs"].append(bcp)
        data["nb_left_subst"].append(left_subst)
        data["nb_right_subst"].append(right_subst)

# DataFrame erstellen
df = pd.DataFrame(data)

# Konvertiere 'year' Spalte zu numerisch für die Korrelationsberechnung
df['year'] = pd.to_numeric(df['year'], errors='coerce')

# Berechne den Pearson-Korrelationskoeffizienten
correlation_matrix = df[['year', 'nb_BCPs', 'nb_left_subst', 'nb_right_subst']].corr(method='pearson')

# Speichere die Ergebnisse als CSV und LaTeX Dateien
df.to_csv(output_file, index=False)
df.to_latex("output.tex", index=False)

# Entferne die 'evaluate_command' Spalte und speichere die modifizierten Daten
df = df.drop(columns=["evaluate_command"])
df.to_latex("output-ohne-eval.tex", index=False)

# Speichere die Korrelationsmatrix als CSV und LaTeX Dateien
correlation_matrix.to_csv('correlation_matrix.csv')
correlation_matrix.to_latex('correlation_matrix.tex')

# Ausgabe der Korrelationsmatrix
print(correlation_matrix)
