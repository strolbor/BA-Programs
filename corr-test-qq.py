import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import argparse
from scipy.stats import linregress, probplot
import os
import glob

saveQQ = False

def TesterSAT(dateiname: str):
    """Überprüft, ob die Daten linear und exponentiell verteilt sind, mithilfe von Pearson für SAT-Solver"""
    df = pd.read_csv(dateiname)

    # Lineare Regression durchführen
    linX = df[["Year-DIMACS"]]
    liny = df[["dimacs-analyzer-time"]]
    
    model = LinearRegression()
    model.fit(linX, liny)
    
    linIntercept = model.intercept_[0]
    linSlope = model.coef_[0][0]
    
    linSlope2, linIntercept2, lin_r_value, lin_p_value, lin_std_err = linregress(df['Year-DIMACS'], df['dimacs-analyzer-time'])

    df['predicted'] = model.predict(linX)
    LinCorrelation = df[['Year-DIMACS', 'dimacs-analyzer-time']].corr(method='pearson').iloc[0, 1]

    # Log-Transformation der abhängigen Variable y
    df['log_dimacs-analyzer-time'] = np.log(df['dimacs-analyzer-time'])

    expoX = df[["Year-DIMACS"]].values
    expoy = df[["log_dimacs-analyzer-time"]].values

    model = LinearRegression()
    model.fit(expoX, expoy)

    expoIntercept = model.intercept_[0]
    expoSlope = model.coef_[0][0]

    df['predicted_log_dimacs-analyzer-time'] = model.predict(expoX)
    df['predicted_dimacs-analyzer-time_expo'] = np.exp(df['predicted_log_dimacs-analyzer-time'])

    expo_correlation = df[['Year-DIMACS', 'predicted_dimacs-analyzer-time_expo']].corr(method='pearson').iloc[0, 1]
    expoSlope2, expoIntercept2, expo_r_value, expo_p_value, expo_std_err = linregress(df['Year-DIMACS'], df['predicted_dimacs-analyzer-time_expo'])

    series = {
        'Dataname': dateiname.split("/")[1],
        'lin_formula': f"{linSlope} * x + {linIntercept}",
        'lin_p_wert': lin_p_value,
        'lin_std_err': lin_std_err,
        'lin_pearson_corr': LinCorrelation,
        
        'expo_formula': f"{np.exp(expoIntercept)} * e^({expoSlope} * x)",
        'expo_p_value': expo_p_value,
        'expo_std_err': expo_std_err,
        'expo_pearson_corr': expo_correlation
    }

    df.sort_values(by='Year-DIMACS', inplace=True)

    # Normales Diagramm
    plt.figure(figsize=(12, 6))
    plt.plot(df['Year-DIMACS'], df['dimacs-analyzer-time'], color='blue', label='Actual data', marker='o', linestyle='-')
    plt.plot(df['Year-DIMACS'], df['predicted'], color='red', label=f'Fit line (Linear Regression), Pearson r={LinCorrelation:.2f}')
    plt.plot(df['Year-DIMACS'], df['predicted_dimacs-analyzer-time_expo'], color='green', label=f'Fit line (log-linear Regression), Pearson r={expo_correlation:.2f}')
    plt.xlabel('Feature Modell Jahr')
    plt.ylabel('Nanosekunden')
    plt.title(f'Lineare Regression und Korrelationsanalyse ({dateiname.split("/")[1].replace(".csv","")})')
    plt.xticks(df["Year-DIMACS"].unique(), rotation=90)
    plt.grid(True, which="both", ls="--")
    plt.legend()
    plt.savefig(dateiname.replace("-median.csv", "-regression-test.png") if dateiname.endswith('-median.csv') else dateiname.replace(".csv", "-regression-test.png"))
    plt.close()

    if saveQQ:
        # QQ-Plot für lineare Regression
        plt.figure(figsize=(12, 6))
        probplot(df['dimacs-analyzer-time'], dist="norm", plot=plt)
        plt.title(f'QQ-Plot (Linear Regression) ({dateiname.split("/")[1].replace(".csv","")})')
        plt.savefig(dateiname.replace("-median.csv", "-qqplot-linear.png") if dateiname.endswith('-median.csv') else dateiname.replace(".csv", "-qqplot-linear.png"))
        plt.close()

        # QQ-Plot für log-lineare Regression
        plt.figure(figsize=(12, 6))
        probplot(df['log_dimacs-analyzer-time'], dist="norm", plot=plt)
        plt.title(f'QQ-Plot (Log-Linear Regression) ({dateiname.split("/")[1].replace(".csv","")})')
        plt.savefig(dateiname.replace("-median.csv", "-qqplot-loglinear.png") if dateiname.endswith('-median.csv') else dateiname.replace(".csv", "-qqplot-loglinear.png"))
        plt.close()

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
            if file.endswith('median.csv') and not file.endswith("Regrssion-result.csv"):
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





def TesterFM(dateiname: str):
    """Überprüft, ob die Daten linear und exponentiell verteilt sind, mithilfe von Pearson für FM-Solver"""
    df = pd.read_csv(dateiname)

    # Lineare Regression durchführen
    linX = df[["Year-SOLVER"]]
    liny = df[["dimacs-analyzer-time"]]
    
    model = LinearRegression()
    model.fit(linX, liny)
    
    linIntercept = model.intercept_[0]
    linSlope = model.coef_[0][0]
    
    linSlope2, linIntercept2, lin_r_value, lin_p_value, lin_std_err = linregress(df['Year-SOLVER'], df['dimacs-analyzer-time'])

    df['predicted'] = model.predict(linX)
    LinCorrelation = df[['Year-SOLVER', 'dimacs-analyzer-time']].corr(method='pearson').iloc[0, 1]

    # Log-Transformation der abhängigen Variable y
    df['log_dimacs-analyzer-time'] = np.log(df['dimacs-analyzer-time'])

    expoX = df[["Year-SOLVER"]].values
    expoy = df[["log_dimacs-analyzer-time"]].values

    model = LinearRegression()
    model.fit(expoX, expoy)

    expoIntercept = model.intercept_[0]
    expoSlope = model.coef_[0][0]

    df['predicted_log_dimacs-analyzer-time'] = model.predict(expoX)
    df['predicted_dimacs-analyzer-time_expo'] = np.exp(df['predicted_log_dimacs-analyzer-time'])

    expo_correlation = df[['Year-SOLVER', 'predicted_dimacs-analyzer-time_expo']].corr(method='pearson').iloc[0, 1]
    expoSlope2, expoIntercept2, expo_r_value, expo_p_value, expo_std_err = linregress(df['Year-SOLVER'], df['predicted_dimacs-analyzer-time_expo'])

    series = {
        'Dataname': dateiname.split("/")[1],
        'lin_formula': f"{linSlope} * x + {linIntercept}",
        'lin_p_wert': lin_p_value,
        'lin_std_err': lin_std_err,
        'lin_pearson_corr': LinCorrelation,
        
        'expo_formula': f"{np.exp(expoIntercept)} * e^({expoSlope} * x)",
        'expo_p_value': expo_p_value,
        'expo_std_err': expo_std_err,
        'expo_pearson_corr': expo_correlation
    }

    df.sort_values(by='Year-SOLVER', inplace=True)

    # Regression Test Plot
    plt.figure(figsize=(12, 6))
    plt.plot(df['Year-SOLVER'], df['dimacs-analyzer-time'], color='blue', label='Actual data', marker='o', linestyle='-')
    plt.plot(df['Year-SOLVER'], df['predicted'], color='red', label=f'Fit line (Linear Regression), Pearson r={LinCorrelation:.2f}')
    plt.plot(df['Year-SOLVER'], df['predicted_dimacs-analyzer-time_expo'], color='green', label=f'Fit line (log-linear Regression), Pearson r={expo_correlation:.2f}')
    plt.xlabel('Sat Solver Jahr')
    plt.ylabel('Nanosekunden')
    plt.title(f'Lineare Regression und Korrelationsanalyse ({dateiname.split("/")[1].replace(".csv","")})')
    plt.xticks(df["Year-SOLVER"].unique(), rotation=90)
    plt.grid(True, which="both", ls="--")
    plt.legend()
    plt.savefig(dateiname.replace("-median.csv", "-regression-test.png") if dateiname.endswith('-median.csv') else dateiname.replace(".csv", "-regression-test.png"))
    plt.close()


    if saveQQ:
        # QQ-Plot für lineare Regression
        plt.figure(figsize=(12, 6))
        probplot(df['dimacs-analyzer-time'], dist="norm", plot=plt)
        plt.title(f'QQ-Plot (Linear Regression) ({dateiname.split("/")[1].replace(".csv","")})')
        plt.savefig(dateiname.replace("-median.csv", "-qqplot-linear.png") if dateiname.endswith('-median.csv') else dateiname.replace(".csv", "-qqplot-linear.png"))
        plt.close()

        # QQ-Plot für log-lineare Regression
        plt.figure(figsize=(12, 6))
        probplot(df['log_dimacs-analyzer-time'], dist="norm", plot=plt)
        plt.title(f'QQ-Plot (Log-Linear Regression) ({dateiname.split("/")[1].replace(".csv","")})')
        plt.savefig(dateiname.replace("-median.csv", "-qqplot-loglinear.png") if dateiname.endswith('-median.csv') else dateiname.replace(".csv", "-qqplot-loglinear.png"))
        plt.close()

    return series

def fm_starter():
    # Liste, um die Pfade aller Dateien mit der Endung 'median.csv' zu speichern
    median_csv_files = []
    df = initDF()


    # Durchlaufe das Verzeichnis und alle Unterverzeichnisse
    for subdir, dirs, files in os.walk("sorted_by_FM"):
        for file in files:
            if file.endswith('median.csv') and not file.endswith("Regrssion-result.csv"):
                median_csv_files.append(os.path.join(subdir, file))

    # Ausgabe der gefundenen Dateien
    for file_path in median_csv_files:
        print(file_path)
        row = TesterFM(file_path)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    
    # Gucken, welcher r-wert Genauer ist.
    # bedeutet höhere WSK (neben den p-werten) das die Nullhypothese falsch ist

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
            if file.endswith('.csv') and not file.endswith("Regrssion-result.csv"):
                median_csv_files.append(os.path.join(subdir, file))
    
    # Durchlaufe das Verzeichnis und alle Unterverzeichnisse
    for subdir, dirs, files in os.walk("sorted_by_verlauf_mit_vorjahren"):
        for file in files:
            if file.endswith('.csv') and not file.endswith("Regrssion-result.csv"):
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



def delete_generated_files_recursive(start_directory: str = '.'):
    """
    Löscht alle vom Skript generierten Dateien im angegebenen Verzeichnis und dessen Unterverzeichnissen.
    
    Args:
    start_directory (str): Der Pfad zu dem Startverzeichnis, in dem die Dateien gelöscht werden sollen. Standard ist das aktuelle Verzeichnis.
    """
    # Definieren Sie die Endungen der generierten Dateien
    generated_file_endings = ['-regression-test.png', '-qqplot-linear.png', '-qqplot-loglinear.png','Regrssion-result.csv']
    
    # Gehen Sie rekursiv durch alle Unterverzeichnisse
    for root, dirs, files in os.walk(start_directory):
        for ending in generated_file_endings:
            pattern = f'*{ending}'
            for file_path in glob.glob(os.path.join(root, pattern)):
                try:
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
                except OSError as e:
                    print(f"Error deleting file {file_path}: {e}")

def main2():

    parser = argparse.ArgumentParser(description='Perform linar/exponential regression on -median.csv data from picker.py.')
    parser.add_argument('-op',"--options", type=int, nargs='+', choices=[1, 2,3 ,4], help="1 für geordnet nach Feature Modell, 2 für geordnet nach SAT-Solver, 3 für geordnet nach Jahr")
    #parser.add_argument('-s','--suffix', nargs='?', type=str, help='Den Filterprefix (endswith) ändern', default='median.csv') # Optionales Argument
    parser.add_argument('-d','--delete',nargs='?', type=bool)
    parser.add_argument('-qq','--qqplot',nargs='?', type=bool)

    args = parser.parse_args()
    print(args)

    if args.qqplot is not None:
        global saveQQ
        saveQQ = True

    if args.options is not None:
        for option in args.options:
            if option == 2:
                sat_starter()
            if option == 1:
                fm_starter()
            if option == 3:
                verlauf_starter()
            if option == 4:
                delete_generated_files_recursive()
    
    if args.delete is not None:
        if args.delete:
            delete_generated_files_recursive()

    


if __name__ == "__main__":
    main2()


