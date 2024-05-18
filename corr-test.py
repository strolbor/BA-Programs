import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import argparse
from scipy.stats import linregress
import os

def Tester(dateiname):
    """überprüft ob die Daten Linear & exponentiell verteilt sind ist.
    Mithilfe von Pearson
    Für SAT-Solver"""
    #print("--- BEIDES ---")

    #df = pd.DataFrame(data)
    df = pd.read_csv(dateiname)

    # Lineare Regression durchführen
    linX = df[["Year-DIMACS"]]
    liny = df[["dimacs-analyzer-time"]]
    
    model = LinearRegression()
    model.fit(linX, liny)
    
    # Regressionskoeffizienten
    linIntercept = model.intercept_
    linSlope = model.coef_[0]
    
    # andere Werte
    # Perform linear regression
    linSlope2, linIntercept2, lin_r_value, lin_p_value, lin_std_err = linregress(df['Year-DIMACS'], df['dimacs-analyzer-time'])



    # Ausgleichsgerade berechnen
    df['predicted'] = model.predict(linX)

    # Korrelation berechnen zw. YEAR-Dimacs und Analyse Zeit
    LinCorrelation = df[['Year-DIMACS', 'dimacs-analyzer-time']].corr(method='pearson').iloc[0, 1]
    #print(df[['Year-DIMACS', 'dimacs-analyzer-time','predicted']].corr(method='pearson'))

    #
    ## EXPO Test
    # 

    # Log-Transformation der abhängigen Variable y
    df['log_dimacs-analyzer-time'] = np.log(df['dimacs-analyzer-time'])

    # Lineares Regressionsmodell erstellen und anpassen
    expoX = df[["Year-DIMACS"]].values # Unabhängige Variable (muss 2D-Array sein)
    expoy = df[["log_dimacs-analyzer-time"]].values  # Transformierte abhängige Variable

    model = LinearRegression()
    model.fit(expoX, expoy)

    expoIntercept = model.intercept_
    expoSlope = model.coef_[0]

    # Vorhersage der transformierten y-Werte (log_y)
    df['predicted_log_dimacs-analyzer-time'] = model.predict(expoX)

    # Rücktransformation der vorhergesagten Werte
    df['predicted_dimacs-analyzer-time_expo'] = np.exp(df['predicted_log_dimacs-analyzer-time'])

    # Korrelation berechnen zw. YEAR-Dimacs und Analyse Zeit
    expo_correlation = df[['Year-DIMACS', 'predicted_dimacs-analyzer-time_expo']].corr(method='pearson').iloc[0, 1]
    #print(df[['Year-DIMACS', 'dimacs-analyzer-time']].corr(method='pearson'))
    #print(f"corr1: r={expo_correlation}")

    expoSlope2, expoIntercept2, expo_r_value, expo_p_value, expo_std_err = linregress(df['Year-DIMACS'], df['predicted_dimacs-analyzer-time_expo'])

    series = {
        'Dataname': dateiname,
        'lin_intercept': linIntercept[0],
        'lin_slope': linSlope[0],
        #'lin_r_value': lin_r_value,
        'lin_p_wert': lin_p_value,
        'lin_std_err': lin_std_err,
        'lin_pearson_corr': LinCorrelation,
        
        'expoIntercept': expoIntercept[0],
        'expoSlope': expoSlope[0],
        #'expo_r_value': expo_r_value,
        'expo_p_value': expo_p_value,
        'expo_std_err':expo_std_err,
        'expo_pearson_corr': expo_correlation
                       
    }


    #
    ## Ergebnisse
    # 

    # Ergebnisse darstellen
    plt.figure(figsize=(10, 5))
    plt.scatter(df['Year-DIMACS'], df['dimacs-analyzer-time'], color='blue', label='Actual data')
    plt.plot(df['Year-DIMACS'], df['predicted'], color='red', label=f'Fit line (Linear Regression), Pearson r={LinCorrelation:.2f}')
    plt.plot(df['Year-DIMACS'], df['predicted_dimacs-analyzer-time_expo'], color='green', label=f'Fit line (log-linear Regression), Pearson r={expo_correlation:.2f}')
    plt.xlabel('Year-DIMACS')
    plt.ylabel('dimacs-analyzer-time')
    plt.title('Lineare Regression und Korrelationsanalyse')
    plt.xticks(df["Year-DIMACS"].unique(),rotation=90)
    plt.legend()
    plt.savefig(dateiname.replace("-median.csv","-regression-test.png"))  # Plot speichern
    #plt.show()
    plt.close()
    

    #print(series)
    return series


def main():
    parser = argparse.ArgumentParser(description='Perform linar/exponential regression on -median.csv data from picker.py.')
    parser.add_argument('csv_path', type=str, help='The path to the folder containing the csv files.')

    args = parser.parse_args()
    #linTester(args.csv_path)
    #expoTester(args.csv_path)
    Tester(args.csv_path)


def main2():

    parser = argparse.ArgumentParser(description='Perform linar/exponential regression on -median.csv data from picker.py.')
    parser.add_argument('ordner', type=str, help='The path to the folder containing the csv files.r')

    args = parser.parse_args()

    # Liste, um die Pfade aller Dateien mit der Endung 'median.csv' zu speichern
    median_csv_files = []
    df = pd.DataFrame(columns=['Dataname', 'lin_intercept','lin_slope',
                               #'lin_r_value',
                               'lin_p_wert','lin_std_err','lin_pearson_corr', \
                               'expoIntercept', 'expoSlope', 
                               #'expo_r_value', 
                               'expo_p_value', 'expo_std_err', 'expo_pearson_corr'])
    print(df)




    # Durchlaufe das Verzeichnis und alle Unterverzeichnisse
    for subdir, dirs, files in os.walk(args.ordner):#"."):
        for file in files:
            if file.endswith('median.csv'):
                median_csv_files.append(os.path.join(subdir, file))

    # Ausgabe der gefundenen Dateien
    for file_path in median_csv_files:
        print(file_path)
        row = Tester(file_path)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    
    # Gucken, welcher r-wert Genauer ist.
    # bedeutet höhere WSK (neben den p-werten) das die Nullhypothese falsch ist
    df['best-fittest'] = df.apply(lambda row: 'Linear' if row['lin_pearson_corr'] > row['expo_pearson_corr'] else 'Exponential', axis=1)


    #print(df)
    df.to_csv(os.path.join(args.ordner,"Regrssion-result.csv"),index=False)


if __name__ == "__main__":
    main2()


def notizen():
    """
    Ein \( P \)-Wert von \( 3.939858388198921 \times 10^{-13} \) (oder \( 3.939858388198921e-13 \)) ist ein extrem kleiner Wert. Dies hat spezifische Implikationen in der Statistik:

### Bedeutung des \( P \)-Werts

1. **Sehr kleine Wahrscheinlichkeit**: Ein \( P \)-Wert von \( 3.939858388198921e-13 \) bedeutet, dass die Wahrscheinlichkeit, dass die beobachtete Beziehung zwischen den Variablen durch Zufall zustande gekommen ist, extrem gering ist. Mit anderen Worten, es gibt fast keinen Zweifel daran, dass die Beziehung, die du beobachtet hast, tatsächlich existiert und nicht das Ergebnis zufälliger Variation ist.

2. **Statistische Signifikanz**: Da dieser \( P \)-Wert weit unter den üblichen Signifikanzniveaus von 0.05 oder 0.01 liegt, kannst du mit sehr hoher Sicherheit sagen, dass die Nullhypothese (die besagt, dass es keine Beziehung gibt) abgelehnt werden kann. Dies deutet darauf hin, dass die Beziehung zwischen den untersuchten Variablen statistisch signifikant ist.

3. **Interpretation**: In praktischen Begriffen bedeutet ein so kleiner \( P \)-Wert, dass es eine sehr starke Evidenz dafür gibt, dass die unabhängige Variable einen echten Einfluss auf die abhängige Variable hat.

### Beispiel

Angenommen, du hast eine lineare Regression durchgeführt und dieser \( P \)-Wert bezieht sich auf die Steigung der Regressionslinie. Ein \( P \)-Wert von \( 3.939858388198921e-13 \) würde dann bedeuten, dass es eine extrem starke Evidenz dafür gibt, dass die unabhängige Variable \( x \) tatsächlich einen Einfluss auf die abhängige Variable \( y \) hat.

### Kontext in der wissenschaftlichen Praxis

- **Hypothesenprüfung**: In der Hypothesenprüfung hilft dir ein so kleiner \( P \)-Wert, die Nullhypothese zu verwerfen. Das bedeutet, dass das Ergebnis deiner Analyse nicht nur durch Zufall zustande gekommen ist.
- **Vertrauen in die Ergebnisse**: Du kannst mit sehr hoher Sicherheit darauf vertrauen, dass die Beziehung zwischen den Variablen real ist und dass die Effekte, die du beobachtet hast, nicht zufällig sind.

### Zusammenfassung

Ein \( P \)-Wert von \( 3.939858388198921e-13 \) bedeutet, dass die Wahrscheinlichkeit, dass die beobachtete Beziehung zufällig ist, extrem gering ist. Dies deutet auf eine sehr starke statistische Signifikanz hin, was bedeutet, dass die Beziehung zwischen den untersuchten Variablen sehr wahrscheinlich real und nicht zufällig ist. Solch ein kleiner \( P \)-Wert gibt dir also hohe Sicherheit in den Ergebnissen deiner Analyse.
    """
    pass