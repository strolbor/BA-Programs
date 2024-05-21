import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import argparse
from scipy.stats import linregress
import os

def TesterSAT(dateiname : str):
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
    linIntercept = model.intercept_[0]
    linSlope = model.coef_[0][0]
    
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

    expoIntercept = model.intercept_[0]
    expoSlope = model.coef_[0][0]


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
        'Dataname': dateiname.split("/")[1],
        'lin_formula': f"{linSlope} * x + {linIntercept}",#linIntercept[0],
        'lin_p_wert': lin_p_value,
        'lin_std_err': lin_std_err,
        'lin_pearson_corr': LinCorrelation,
        
        'expo_formuala': f"{np.exp(expoIntercept)} * e^({expoSlope} * x)",
        'expo_p_value': expo_p_value,
        'expo_std_err':expo_std_err,
        'expo_pearson_corr': expo_correlation
                       
    }


    #
    ## Ergebnisse
    # 

    # Sortieren
    df.sort_values(by='Year-DIMACS', inplace=True)

    # Ergebnisse darstellen
    plt.figure(figsize=(12, 6))
    #plt.scatter(df['Year-DIMACS'], df['dimacs-analyzer-time'], color='blue', label='Actual data')
    plt.plot(df['Year-DIMACS'], df['dimacs-analyzer-time'], color='blue', label='Actual data', marker='o', linestyle='-')
    plt.plot(df['Year-DIMACS'], df['predicted'], color='red', label=f'Fit line (Linear Regression), Pearson r={LinCorrelation:.2f}')
    plt.plot(df['Year-DIMACS'], df['predicted_dimacs-analyzer-time_expo'], color='green', label=f'Fit line (log-linear Regression), Pearson r={expo_correlation:.2f}')
    plt.xlabel('Feature Modell Jahr')
    plt.ylabel('Nanosekunden')
    plt.title(f'Lineare Regression und Korrelationsanalyse ({dateiname.split("/")[1].replace(".csv","")})')
    plt.xticks(df["Year-DIMACS"].unique(),rotation=90)
    plt.grid(True, which="both", ls="--")  # Gitterlinien anzeigen
    plt.legend()

    if dateiname.endswith('-median.csv'):
        plt.savefig(dateiname.replace("-median.csv","-regression-test.png"))  # Plot speichern
    else:
        plt.savefig(dateiname.replace(".csv","-regression-test.png"))  # Plot speichern
    #plt.show()
    plt.close()
    

    #print(series)
    return series

def initDF():
    df = pd.DataFrame(columns=['Dataname', 'lin_formula',
                               'lin_p_wert','lin_std_err','lin_pearson_corr', \
                               'expo_formula', 
                               'expo_p_value', 'expo_std_err', 'expo_pearson_corr'])
    return df

def sat_starter():
    # Liste, um die Pfade aller Dateien mit der Endung 'median.csv' zu speichern
    median_csv_files = []
    df = initDF()


    # Durchlaufe das Verzeichnis und alle Unterverzeichnisse
    for subdir, dirs, files in os.walk("sorted_by_SAT"):
        for file in files:
            if file.endswith('median.csv'):
                median_csv_files.append(os.path.join(subdir, file))

    # Ausgabe der gefundenen Dateien
    for file_path in median_csv_files:
        print(file_path)
        row = TesterSAT(file_path)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    
    # Gucken, welcher r-wert Genauer ist.
    # bedeutet höhere WSK (neben den p-werten) das die Nullhypothese falsch ist
    #df['best-fittest'] = df.apply(lambda row: 'Linear' if row['lin_pearson_corr'] > row['expo_pearson_corr'] else 'Exponential', axis=1)

    df['best-fittest'] = df.apply(lambda row: 'Linear' if abs(row['lin_pearson_corr']) > abs(row['expo_pearson_corr']) else 'Expo', axis=1)


    #print(df)
    df.sort_values(by='Dataname',inplace=True)
    df.to_csv(os.path.join("sorted_by_SAT","Regrssion-result.csv"),index=False)





def TesterFM(dateiname):
    """überprüft ob die Daten Linear & exponentiell verteilt sind ist.
    Mithilfe von Pearson
    Für FM-Solver"""
    #print("--- BEIDES ---")

    #df = pd.DataFrame(data)
    df = pd.read_csv(dateiname)

    # Lineare Regression durchführen
    linX = df[["Year-SOLVER"]]
    liny = df[["dimacs-analyzer-time"]]
    
    model = LinearRegression()
    model.fit(linX, liny)
    
    # Regressionskoeffizienten
    linIntercept = model.intercept_[0]
    linSlope = model.coef_[0][0]
    
    # andere Werte
    # Perform linear regression
    linSlope2, linIntercept2, lin_r_value, lin_p_value, lin_std_err = linregress(df['Year-SOLVER'], df['dimacs-analyzer-time'])



    # Ausgleichsgerade berechnen
    df['predicted'] = model.predict(linX)

    # Korrelation berechnen zw. YEAR-Dimacs und Analyse Zeit
    LinCorrelation = df[['Year-SOLVER', 'dimacs-analyzer-time']].corr(method='pearson').iloc[0, 1]
    #print(df[['Year-DIMACS', 'dimacs-analyzer-time','predicted']].corr(method='pearson'))

    #
    ## EXPO Test
    # 

    # Log-Transformation der abhängigen Variable y
    df['log_dimacs-analyzer-time'] = np.log(df['dimacs-analyzer-time'])

    # Lineares Regressionsmodell erstellen und anpassen
    expoX = df[["Year-SOLVER"]].values # Unabhängige Variable (muss 2D-Array sein)
    expoy = df[["log_dimacs-analyzer-time"]].values  # Transformierte abhängige Variable

    model = LinearRegression()
    model.fit(expoX, expoy)

    expoIntercept = model.intercept_[0]
    expoSlope = model.coef_[0][0]

    # Vorhersage der transformierten y-Werte (log_y)
    df['predicted_log_dimacs-analyzer-time'] = model.predict(expoX)

    # Rücktransformation der vorhergesagten Werte
    df['predicted_dimacs-analyzer-time_expo'] = np.exp(df['predicted_log_dimacs-analyzer-time'])

    # Korrelation berechnen zw. YEAR-Dimacs und Analyse Zeit
    expo_correlation = df[['Year-SOLVER', 'predicted_dimacs-analyzer-time_expo']].corr(method='pearson').iloc[0, 1]
    #print(df[['Year-DIMACS', 'dimacs-analyzer-time']].corr(method='pearson'))
    #print(f"corr1: r={expo_correlation}")

    expoSlope2, expoIntercept2, expo_r_value, expo_p_value, expo_std_err = linregress(df['Year-SOLVER'], df['predicted_dimacs-analyzer-time_expo'])

    series = {
        'Dataname': dateiname.split("/")[1],
        'lin_formula': f"{linSlope} * x + {linIntercept}",#linIntercept[0],
        'lin_p_wert': lin_p_value,
        'lin_std_err': lin_std_err,
        'lin_pearson_corr': LinCorrelation,
        
        'expo_formuala': f"{np.exp(expoIntercept)} * e^({expoSlope} * x)",
        'expo_p_value': expo_p_value,
        'expo_std_err':expo_std_err,
        'expo_pearson_corr': expo_correlation
                       
    }


    #
    ## Ergebnisse
    # 

    # Sortieren
    df.sort_values(by='Year-SOLVER', inplace=True)

    # Ergebnisse darstellen
    plt.figure(figsize=(12, 6))
    #plt.scatter(df['Year-SOLVER'], df['dimacs-analyzer-time'], color='blue', label='Actual data')
    #plt.plot(data[plot_x], data[plot_y], marker='o', linestyle='-', label=str(data['Year-DIMACS'].unique()[0]) + "_" + fmmodel)
    plt.plot(df['Year-SOLVER'], df['dimacs-analyzer-time'], color='blue', label=f'Feature Modell Jahr: {df["Year-DIMACS"].unique()[0]}', marker='o', linestyle='-')
    plt.plot(df['Year-SOLVER'], df['predicted'], color='red', label=f'Fit line (Linear Regression), Pearson r={LinCorrelation:.2f}')
    plt.plot(df['Year-SOLVER'], df['predicted_dimacs-analyzer-time_expo'], color='green', label=f'Fit line (log-linear Regression), Pearson r={expo_correlation:.2f}')
    plt.xlabel('Sat Sover Jahr')
    plt.ylabel('Nanosekunden')
    plt.title(f'Lineare Regression und Korrelationsanalyse ({dateiname.split("/")[1].replace(".csv","")})')
    plt.xticks(df["Year-SOLVER"].unique(),rotation=90)
    plt.grid(True, which="both", ls="--")  # Gitterlinien anzeigen
    plt.legend()
    plt.savefig(dateiname.replace("-median.csv","-regression-test.png"))  # Plot speichern
    #plt.show()
    plt.close()
    

    #print(series)
    return series

def fm_starter():
    # Liste, um die Pfade aller Dateien mit der Endung 'median.csv' zu speichern
    median_csv_files = []
    df = initDF()


    # Durchlaufe das Verzeichnis und alle Unterverzeichnisse
    for subdir, dirs, files in os.walk("sorted_by_FM"):
        for file in files:
            if file.endswith('median.csv'):
                median_csv_files.append(os.path.join(subdir, file))

    # Ausgabe der gefundenen Dateien
    for file_path in median_csv_files:
        print(file_path)
        row = TesterFM(file_path)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    
    # Gucken, welcher r-wert Genauer ist.
    # bedeutet höhere WSK (neben den p-werten) das die Nullhypothese falsch ist
    #df['best-fittest'] = df.apply(lambda row: 'Linear' if row['lin_pearson_corr'] > row['expo_pearson_corr'] else 'Exponential', axis=1)

    df['best-fittest'] = df.apply(lambda row: 'Linear' if abs(row['lin_pearson_corr']) > abs(row['expo_pearson_corr']) else 'Expo', axis=1)

    


    #print(df)
    df.sort_values(by='Dataname',inplace=True)
    df.to_csv(os.path.join("sorted_by_FM","Regrssion-result.csv"),index=False)

def verlauf_starter():
    # Liste, um die Pfade aller Dateien mit der Endung 'median.csv' zu speichern
    median_csv_files = []
    df = initDF()


    # Durchlaufe das Verzeichnis und alle Unterverzeichnisse
    for subdir, dirs, files in os.walk("sorted_by_verlauf"):
        for file in files:
            if file.endswith('.csv'):
                median_csv_files.append(os.path.join(subdir, file))

    # Ausgabe der gefundenen Dateien
    for file_path in median_csv_files:
        print(file_path)
        row = TesterSAT(file_path)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    
    # Gucken, welcher r-wert Genauer ist.
    # bedeutet höhere WSK (neben den p-werten) das die Nullhypothese falsch ist
    
    df['best-fittest'] = df.apply(lambda row: 'Linear' if row['lin_pearson_corr'] > row['expo_pearson_corr'] else 'Exponential', axis=1)

  

    #print(df)
    df.sort_values(by='Dataname',inplace=True)
    df.to_csv(os.path.join("sorted_by_verlauf","Regrssion-result.csv"),index=False)



def main2():

    parser = argparse.ArgumentParser(description='Perform linar/exponential regression on -median.csv data from picker.py.')
    parser.add_argument('-op',"--options", type=int, nargs='+', choices=[1, 2,3 ], help="1 für geordnet nach Feature Modell, 2 für geordnet nach SAT-Solver, 3 für geordnet nach Jahr")
    #parser.add_argument('-s','--suffix', nargs='?', type=str, help='Den Filterprefix (endswith) ändern', default='median.csv') # Optionales Argument

    args = parser.parse_args()

    for option in args.options:
        if option == 2:
            sat_starter()
        if option == 1:
            fm_starter()
        if option == 3:
            verlauf_starter()

    


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