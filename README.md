# Datenanalyser für Bachelorarbeit

## 1 Schritt

Führe Torte Experiment durch.
Und schmecke sie ab (solver_moell_satifiction).

```bash 
bash linux-history-yerarly-v2.sh 

```

## 2 Schritt

Führe meinen 

```sh 
python3 picker.py -rm2024 1 1 2

``` 
aus, um die Daten nach:
- median
zu filtern.
Und erstelle dabei die Plots für:
- alle Graphen
    - geordnet nach
        - Feature Modell (FM) (op 1)
        - SAT-Solver (SAT) (op 2)
- einzelne Graphen
    - Feature Modell (FM)
    - SAT-Solver (SAT)
zu erhalten.

## 3 Schritt

Führe: 

```sh 

python3 tenPlotterSAT.py && \ 
python3 tenPlotterFM.py && \
python3 Version-Jahr_punktpunkt.py &&\
python3 Version-Jahr_handsight.py && \
python3 Version-Jahr_foresight.py 

```

um weitere Plots zu den SAT & FM zu erhalten:
- 10-Plots 
    - FM
    - SAT
- FM Jahr == SAT Jahr Plot


## 4 Schritt

Führe: 

```sh 
python3 corr-test-qq.py -op 1 2 3
``` 


aus um Informationen zu den Wachstumgradizent zu erhalten:
- Lineare Regression
- log-lineare Regression (um exponentielles Wachstum nachzu weisen).
- Den Wert mit den höchsten pearson Wachstumgradienten ist das Ding der Wahl
- Für QQ Plots Analyse haben wir zu wenige Daten


- Pandas (persons korrelations quoeffizenten )
  - https://stackoverflow.com/questions/25571882/pandas-columns-correlation-with-statistical-significance


## Log minimierer:

```sh
grep '^[cs]' output.log > tmp && grep -v '^v' output.log >> tmp && mv tmp output.min.log

```


## Git Log Betrachter

## Datei Details in allen Versionen anzeigen lassen
- Wie weise ich was nach, wann ich was gemacht habe.

```sh
git log --stat

```

```text
commit 8f6e1431721e90b1e45d54bb023bf6f41d190861
Author: Urs <57560299+ubb21@users.noreply.github.com>
Date:   Mon Jun 10 16:18:05 2024 +0200

    rnik

 files_all/fm-all-kconfigreader.png            | Bin 159903 -> 0 bytes
 files_all/fm-all-kmax.png                     | Bin 140941 -> 0 bytes
 files_all/sat-all-kconfigreader.png           | Bin 128725 -> 0 bytes
 files_all/sat-all-kmax.png                    | Bin 114904 -> 0 bytes
 files_log/Version-Jahr-kconfig-foresight.png  | Bin 0 -> 48229 bytes
 files_log/Version-Jahr-kconfig-handsight.png  | Bin 0 -> 52254 bytes
 files_log/Version-Jahr-kconfig-punktpunkt.png | Bin 0 -> 43801 bytes
 files_log/Version-Jahr-kmax-foresight.png     | Bin 0 -> 47994 bytes
 files_log/Version-Jahr-kmax-handsight.png     | Bin 0 -> 53190 bytes
 files_log/Version-Jahr-kmax-punktpunkt.png    | Bin 0 -> 45517 bytes
 files_log/fm-all-kconfigreader.png            | Bin 0 -> 324986 bytes
 files_log/fm-all-kmax.png                     | Bin 0 -> 354263 bytes
 files_log/sat-03-Forklift-kconfigreader.png   | Bin 0 -> 47331 bytes
 ```

## Alle Veränderungen anzeigen lassen

```sh
git log -p

```

Das, wenn man jedemanden leiden lassen will.

## Beispiel für ein nützliches, detailliertes Log:

```sh
git log --graph --pretty=format:'%h - %an, %ar : %s' --stat
```