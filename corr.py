import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Load the data
data = pd.read_csv('sorted_by_SAT/02-zchaff-kconfigreader-median.csv')

# Calculate Pearson's correlation coefficient
correlation = data['dimacs-analyzer-time'].corr(data['Year-DIMACS'])
print("Pearson's correlation coefficient:", correlation)

# Perform linear regression
slope, intercept, r_value, p_value, std_err = linregress(data['Year-DIMACS'], data['dimacs-analyzer-time'])
print("Steigung",slope)
print("Achsenabschnitt mit y Achse",intercept)
print("Stärke und Richtung einer linearen Beziehung",r_value)
print("Standardfehler der Steigung",std_err)

# Create the scatter plot
plt.scatter(data['Year-DIMACS'], data['dimacs-analyzer-time'], color='blue', label='Data Points')

# Add the regression line
plt.plot(data['Year-DIMACS'], intercept + slope * data['Year-DIMACS'], 'r', label='Fitted line')

print("1: ",(intercept + slope * data['Year-DIMACS']).corr(data['Year-DIMACS']))
print("2: ",(5 * data['dimacs-analyzer-time'] **2).corr(data['Year-DIMACS']))


# Label the axes and add a legend
plt.xlabel('JAhr des FM')
plt.ylabel('Nanosekunden')
plt.title('Regression Line and Pearson Correlation')
plt.legend()

# Show the plot
plt.show()
