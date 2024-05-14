import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Daten erstellen
data = {
    "Year-DIMACS": [2002, 2003, 2005, 2006, 2004, 2007, 2008, 2009, 2010, 2011, 2014, 2015, 2012, 2013, 2017, 2018, 2016, 2019, 2021, 2022, 2020, 2023, 2024],
    "dimacs-analyzer-time": [28575826.0, 26733080.0, 45946024.0, 55658457.0, 34892681.0, 75663773.0, 100024789.0, 129064740.0, 138120070.0, 167769804.0, 216313122.0, 251240199.0, 177809116.0, 193798121.0, 319234057.0, 346222497.0, 272316746.0, 394456116.0, 477582431.0, 503941762.0, 417442879.0, 535173892.0, 597433451.0]
}

df = pd.DataFrame(data)

# Lineare Regression durchführen
X = df[["Year-DIMACS"]]
y = df["dimacs-analyzer-time"]
model = LinearRegression()
model.fit(X, y)

# Ausgleichsgerade berechnen
df['predicted'] = model.predict(X)

# Korrelation berechnen
correlation = df[['Year-DIMACS', 'dimacs-analyzer-time']].corr(method='pearson').iloc[0, 1]

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

correlation
