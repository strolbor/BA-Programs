import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd

# Daten erstellen
data = {
    "Year-DIMACS": [2002, 2003, 2005, 2006, 2004, 2007, 2008, 2009, 2010, 2011, 2014, 2015, 2012, 2013, 2017, 2018, 2016, 2019, 2021, 2022, 2020, 2023, 2024],
    "dimacs-analyzer-time": [28575826.0, 26733080.0, 45946024.0, 55658457.0, 34892681.0, 75663773.0, 100024789.0, 129064740.0, 138120070.0, 167769804.0, 216313122.0, 251240199.0, 177809116.0, 193798121.0, 319234057.0, 346222497.0, 272316746.0, 394456116.0, 477582431.0, 503941762.0, 417442879.0, 535173892.0, 597433451.0]
}

df = pd.DataFrame(data)

# Logarithmieren der dimacs-analyzer-time für exponentielle Anpassung
#df['log_dimacs-analyzer-time'] = np.log(df['dimacs-analyzer-time'])

# Exponentielle Regression durchführen (lineare Regression auf den log-transformierten Daten)
X = df[["Year-DIMACS"]]
y_log = df['dimacs-analyzer-time']
model_exp = LinearRegression()
model_exp.fit(X, y_log)

# Vorhersagen in den originalen Maßstab zurücktransformieren
df['predicted_exp'] = np.exp(model_exp.predict(X))

# Korrelation der ursprünglichen und vorhergesagten Werte berechnen
correlation_exp = np.corrcoef(df['dimacs-analyzer-time'], df['predicted_exp'])[0, 1]

# Ergebnisse darstellen
plt.figure(figsize=(10, 5))
plt.scatter(df['Year-DIMACS'], df['dimacs-analyzer-time'], color='blue', label='Actual data')
plt.plot(df['Year-DIMACS'], df['predicted_exp'], color='green', label=f'Exponential Fit, Pearson r={correlation_exp:.2f}')
plt.xlabel('Year-DIMACS')
plt.ylabel('dimacs-analyzer-time')
plt.title('Exponentielle Regression und Korrelationsanalyse')
plt.xticks(df["Year-DIMACS"].unique(),rotation=90)
plt.legend()
plt.show()

correlation_exp
