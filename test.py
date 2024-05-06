import pandas as pd
import matplotlib.pyplot as plt

# Beispiel DataFrame erstellen
data = {'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Emily'],
        'Alter': [25, 30, 35, 40, 45],
        'Einkommen': [50000, 60000, 75000, 80000, 90000]}

df = pd.DataFrame(data)

# Plot erstellen
df.plot(x='Name', y='Alter', kind='bar')
plt.show()
