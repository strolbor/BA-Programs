import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import argparse
from scipy.stats import linregress


# Daten erstellen
data = {
    "Year-DIMACS": [2002, 2003, 2005, 2006, 2004, 2007, 2008, 2009, 2010, 2011, 2014, 2015, 2012, 2013, 2017, 2018, 2016, 2019, 2021, 2022, 2020, 2023, 2024],
    "dimacs-analyzer-time": [28575826.0, 26733080.0, 45946024.0, 55658457.0, 34892681.0, 75663773.0, 100024789.0, 129064740.0, 138120070.0, 167769804.0, 216313122.0, 251240199.0, 177809116.0, 193798121.0, 319234057.0, 346222497.0, 272316746.0, 394456116.0, 477582431.0, 503941762.0, 417442879.0, 535173892.0, 597433451.0]
}

def linTester(dateiname):
    """überprüft ob die Daten Linear ist.
    Mithilfe von Pearson"""
    print("--- LINTEST ---")

    df = pd.DataFrame(data)
    #df = pd.read_csv(dateiname)

    # Lineare Regression durchführen
    X = df[["Year-DIMACS"]]
    y = df[["dimacs-analyzer-time"]]
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Regressionskoeffizienten
    intercept = model.intercept_
    slope = model.coef_[0]
    
    # andere Werte
    # Perform linear regression
    slope2, intercept2, r_value, p_value, std_err = linregress(data['Year-DIMACS'], data['dimacs-analyzer-time'])

    print(f'Intercept (a): {intercept} {intercept2}') # Der Intercept gibt den Wert der abhängigen Variable bei einem unabhängigen Variablenwert von null an.
    print(f'Slope (b): {slope} {slope2}') # Die Slope gibt die Änderungsrate der abhängigen Variablen pro Einheit der unabhängigen Variablen an.
    print(f"R-Wert (r) {r_value}")
    print(f"p_value: {p_value}")
    print(f"std_err: {std_err}")



    # Ausgleichsgerade berechnen
    df['predicted'] = model.predict(X)

    # Korrelation berechnen zw. YEAR-Dimacs und Analyse Zeit
    correlation = df[['Year-DIMACS', 'dimacs-analyzer-time']].corr(method='pearson').iloc[0, 1]
    #print(df[['Year-DIMACS', 'dimacs-analyzer-time','predicted']].corr(method='pearson'))
    print(f"corr1: r={correlation}")







    # Ergebnisse darstellen
    plt.figure(figsize=(10, 5))
    plt.scatter(df['Year-DIMACS'], df['dimacs-analyzer-time'], color='blue', label='Actual data')
    plt.plot(df['Year-DIMACS'], df['predicted'], color='red', label=f'Fit line, Pearson r={correlation:.2f}')
    plt.xlabel('Year-DIMACS')
    plt.ylabel('dimacs-analyzer-time')
    plt.title('Lineare Regression und Korrelationsanalyse')
    plt.xticks(df["Year-DIMACS"].unique(),rotation=90)
    plt.legend()
    plt.show()


def expoTester(dateipath):
    """überprüft ob die Daten exponentielles Wachstum vorliegt.
    Die y-Daten werden mit log() gerechnet -> Steigung hat.
    Dann wird mit Hilfe von PEarson überprüft, ob das passt.
    """
    print("--- expo Test ---")
    df = pd.DataFrame(data)
    #df = pd.read_csv(dateipath)
    
    # Log-Transformation der abhängigen Variable y
    df['log_y'] = np.log(df['dimacs-analyzer-time'])

    # Lineares Regressionsmodell erstellen und anpassen
    X = df[["Year-DIMACS"]].values # Unabhängige Variable (muss 2D-Array sein)
    y = df[["log_y"]].values  # Transformierte abhängige Variable

    model = LinearRegression()
    model.fit(X, y)

    # Regressionskoeffizienten
    intercept = model.intercept_
    slope = model.coef_[0]

    print(f'Intercept (log(a)): {intercept}') # Der Intercept gibt den Wert der abhängigen Variable bei einem unabhängigen Variablenwert von null an.
    print(f'Slope (b): {slope}') # Die Slope gibt die Änderungsrate der abhängigen Variablen pro Einheit der unabhängigen Variablen an.

    # Vorhersage der transformierten y-Werte (log_y)
    df['predicted_log_y'] = model.predict(X)

    # Rücktransformation der vorhergesagten Werte
    df['predicted_y'] = np.exp(df['predicted_log_y'])

    # Ergebnisse anzeigen
    #print(df)

    # Korrelation berechnen zw. YEAR-Dimacs und Analyse Zeit
    correlation = df[['Year-DIMACS', 'predicted_y']].corr(method='pearson').iloc[0, 1]
    #print(df[['Year-DIMACS', 'dimacs-analyzer-time']].corr(method='pearson'))
    print(f"corr1: r={correlation}")

    # Plot der Daten und der Regressionslinie
    plt.scatter(df['Year-DIMACS'], df['dimacs-analyzer-time'], color='blue', label='Original Data')
    plt.plot(df['Year-DIMACS'], df['predicted_y'], color='red', label=f'Fit line, Pearson r={correlation:.2f}')
    plt.xlabel('Year-DIMACS')
    plt.ylabel('time')
    plt.legend()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Perform linar/exponential regression on DIMACS data.')
    parser.add_argument('csv_path', type=str, help='The path to the csv file containing the data.')

    args = parser.parse_args()
    linTester(args.csv_path)
    expoTester(args.csv_path)

if __name__ == "__main__":
    main()