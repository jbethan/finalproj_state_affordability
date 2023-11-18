# %%
import pandas as pd
import seaborn as sns

# %%
data = pd.read_csv('2023_state_dataset.csv', index_col=None)
data = data.drop(data.columns[0], axis=1)
data.head()

# %%
