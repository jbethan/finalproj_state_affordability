import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# %%
# Home Insurance Averages by State
url = "https://www.insurance.com/home-and-renters-insurance/home-insurance-basics/average-homeowners-insurance-rates-by-state"
response = requests.get(url)
print(response.status_code)

# %%
soup = BeautifulSoup(response.text, 'html.parser')
table_ins = soup.find_all("table")

# %%
df_ins = pd.read_html(str(table_ins))
# convert list to dataframe
df_ins = pd.DataFrame(df_ins[0])
df_ins.head()

# %%
# Clean up
cols = ['Average annual rates for $200,000 in dwelling coverage', 'Average annual rates for $300,000 in dwelling coverage',	'Average annual rates for $400,000 in dwelling coverage', 'Average annual rates for $500,000 in dwelling coverage']
df_ins[cols]= df_ins[cols].replace('\$', '', regex = True)
df_ins[cols]= df_ins[cols].replace(',', '', regex = True).astype(float)
df_ins['State']= df_ins['State'].replace('\*', '', regex = True)
df_ins.head()

# %%
# Create Rate for Each Bracket
df_ins["Rate at $200k"] = df_ins["Average annual rates for $200,000 in dwelling coverage"] / 200000
df_ins["Rate at $300k"] = df_ins["Average annual rates for $300,000 in dwelling coverage"] / 300000
df_ins["Rate at $400k"] = df_ins["Average annual rates for $400,000 in dwelling coverage"] / 400000
df_ins["Rate at $500k"] = df_ins["Average annual rates for $500,000 in dwelling coverage"] / 500000
df_ins.head()

# %%
# Read to CSV
#df_ins.to_csv('2023_home_insurance_rates_by_state.csv')
# %%
df_ins

# %%
