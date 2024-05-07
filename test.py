import pandas as pd


df = pd.read_csv("solve_model-satisfiable/output.csv")


# DataFrame nach "dimacs-analyzer-time" sortieren
sorted_df = df.sort_values(by='dimacs-analyzer-time')

# Gruppieren nach ['dimacs-analyzer', 'dimacs-file'] und Median berechnen
median_grouped = sorted_df.groupby(['dimacs-analyzer', 'dimacs-file']).median()


median_grouped.to_csv("test.csv")
median_grouped.to_csv("testindex.csv",index=False)
