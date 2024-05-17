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

def Tester(dateiname):
    """überprüft ob die Daten Linear & exponentiell verteilt sind ist.
    Mithilfe von Pearson"""
    print("--- BEIDES ---")

    df = pd.DataFrame(data)
    #df = pd.read_csv(dateiname)

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
    linSlope2, linIntercept2, lin_r_value, lin_p_value, lin_std_err = linregress(data['Year-DIMACS'], data['dimacs-analyzer-time'])



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
    print(f"corr1: r={expo_correlation}")

    expoSlope2, expoIntercept2, expo_r_value, expo_p_value, expo_std_err = linregress(df['Year-DIMACS'], df['predicted_dimacs-analyzer-time_expo'])

    series = {
        'Dataname': dateiname,
        'lin_intercept': linIntercept[0],
        'lin_slope': linSlope[0],
        'lin_p_wert': lin_p_value,
        'lin_std_err': lin_std_err,
        'lin_pearson_corr': LinCorrelation,
        
        'expoIntercept2': expoIntercept[0],
        'expoSlope': expoSlope[0],
        'expo_r_value': expo_r_value,
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
    plt.plot(df['Year-DIMACS'], df['predicted_dimacs-analyzer-time_expo'], color='green', label=f'Fit line (log-lionear Regression), Pearson r={expo_correlation:.2f}')
    plt.xlabel('Year-DIMACS')
    plt.ylabel('dimacs-analyzer-time')
    plt.title('Lineare Regression und Korrelationsanalyse')
    plt.xticks(df["Year-DIMACS"].unique(),rotation=90)
    plt.legend()
    plt.savefig('test.png')  # Plot speichern
    plt.show()
    plt.close()
    

    print(series)
    return series


def main():
    parser = argparse.ArgumentParser(description='Perform linar/exponential regression on DIMACS data.')
    parser.add_argument('csv_path', type=str, help='The path to the csv file containing the data.')

    args = parser.parse_args()
    #linTester(args.csv_path)
    #expoTester(args.csv_path)
    Tester(args.csv_path)

if __name__ == "__main__":
    main()