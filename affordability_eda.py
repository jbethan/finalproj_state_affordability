# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# %%
data = pd.read_csv('2023_state_dataset.csv', index_col=None)
data = data.drop(data.columns[0], axis=1)
data.head()

# %%
data["Monthly Difference"] = data['Monthly Tax Adjusted Income']- data['Monthly Housing Payments']
data.head()

# %%
data.plot(x='State', y=['Monthly Housing Payments','Monthly Tax Adjusted Income'], kind = 'line', color = ['Blue', 'green'])
plt.xlabel ('State')
plt.ylabel ('Cost')
plt.title ('Monthly Adjusted Income v. Housing Payments')
plt.show ()
# %%
# Save figure
plt.savefig("income_housing.png", dpi = 300)
# %%
