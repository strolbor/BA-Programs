def find_matching_entry(array, prefix):
    for entry in array:
        if entry.startswith(prefix):
            return entry
    return None

# Beispielaufruf
my_array = ["09-precosat", "05-satelitegti.sh", "07-rsat.sh", "21-kissat", "12-satelite", "16-maplecomsps", "20-kissat-sc2020-sat", "17-maple", "07-rsat", "10-cryptominisat", "12-glucose", "07-satelite", "04-zchaff", "11-glucose", "03-forklift", "11-satelite", "14-lingeling-ayv", "18-maplelcmdistchronobt", "13-lingeling-aqw", "02-zchaff", "12-glucose.sh", "05-satelite", "19-maplelcmdiscchronobt-dl-v3", "06-minisat", "05-minisat", "11-glucose.sh"]
prefix_to_find = "09-"

matching_entry = find_matching_entry(my_array, prefix_to_find)
if matching_entry:
    print("Passender Eintrag gefunden:", matching_entry)
else:
    print("Kein passender Eintrag gefunden.")
