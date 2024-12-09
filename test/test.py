import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Beispieldaten erstellen
np.random.seed(0)
df = pd.DataFrame({
    'Year-DIMACS': np.linspace(0, 10, 100),
    'dimacs-analyzer-time': np.exp(2 + 0.5 * np.linspace(0, 10, 100)) + np.random.normal(size=100)
})

# Log-Transformation der abhängigen Variable y
df['log_dimacs-analyzer-time'] = np.log(df['dimacs-analyzer-time'])

# Lineares Regressionsmodell erstellen und anpassen
expoX = df[["Year-DIMACS"]].values  # Unabhängige Variable (muss 2D-Array sein)
expoy = df[["log_dimacs-analyzer-time"]].values  # Transformierte abhängige Variable

model = LinearRegression()
model.fit(expoX, expoy)

expoIntercept = model.intercept_[0]
expoSlope = model.coef_[0][0]
print("e2:",model.coef_)

# Vorhersage der transformierten y-Werte (log_y)
df['predicted_log_dimacs-analyzer-time'] = model.predict(expoX)

# Exponentielle Funktion erstellen
def exponential_function(x):
    return np.exp(expoIntercept) * np.exp(expoSlope * x)

# Vorhersage der originalen y-Werte (exp_y)
df['predicted_dimacs-analyzer-time'] = exponential_function(df['Year-DIMACS'])

# Plot der Daten und der angepassten Funktion
plt.scatter(df['Year-DIMACS'], df['dimacs-analyzer-time'], label='Daten', color='blue')
plt.plot(df['Year-DIMACS'], df['predicted_dimacs-analyzer-time'], label='Angepasste exponentielle Funktion', color='red')
plt.xlabel('Year-DIMACS')
plt.ylabel('dimacs-analyzer-time')
plt.legend()
#plt.show()

# Exponentielle Funktion anzeigen
print(f"Exponentielle Funktion: y = {np.exp(expoIntercept)} * e({expoSlope} * x)")
