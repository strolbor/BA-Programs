# Datenanalyser für Bachelorarbeit

## 1 Schritt

Führe Torte Experiment durch.
Und schmecke sie ab (solver_moell_satifiction).
```sh ```

## 2 Schritt

Führe meinen ```sh python3 picker.py``` aus, um die Daten nach:
- median
zu filtern.
Und erstelle dabei die Plots für:
- alle Graphen
    - geordnet nach
        - Feature Modell (FM)
        - SAT-Solver (SAT)
- einzelne Graphen
    - Feature Modell (FM)
    - SAT-Solver (SAT)
zu erhalten.

## 3 Schritt

Führe: 
- ```sh python3 tenPlotterSAT.py && python3 tenPlotterFM.py && python3 Version-Jahr.py ```
um weitere Plots zu den SAT & FM zu erhalten:
- 10-Plots 
    - FM
    - SAT
- FM Jahr == SAT Jahr Plot


## 4 Schritt

Führe: 
```sh corr-test.py``` 
aus um Informationen zu den Wachstumgradizent zu erhalten:
- Lineare Regression
- log-lineare Regression (um exponentielles Wachstum nachzu weisen).
- Den Wert mit den höchsten pearson Wachstumgradienten ist das Ding der Wahl
- Für QQ Plots Analyse haben wir zu wenige Daten


- Pandas (persons korrelations quoeffizenten )
  - https://stackoverflow.com/questions/25571882/pandas-columns-correlation-with-statistical-significance