# %%
import pandas as pd
import requests
from bs4 import BeautifulSoup
from mortgage import Loan
import re

# %%
# Median Sale Price by State
url = "https://www.bankrate.com/real-estate/median-home-price/#median-price-by-state"
response = requests.get(url)
print(response.status_code)

# %%
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find_all("table")

# %%
df = pd.read_html(str(table))
# convert list to dataframe
df = pd.DataFrame(df[0])
df.head()
# %%
#df = df.sort_values(by="Price", ascending = False)
#df['rank'] = df['Price'].rank(ascending = False)
#df


# %% 
# Average Salary by State
url = "https://www.newtraderu.com/2023/11/01/average-income-by-state/"
response = requests.get(url)
print(response.status_code)

# %%
soup = BeautifulSoup(response.text, 'html.parser')
table2 = soup.find_all("table")

# %%
lst = pd.read_html(str(table2))
#df2 = pd.read_html(table2)
df2 = lst[0]
df2.head()


# %%
df_new = df.merge(df2, how = 'left', on = "State")
# Massuchasetts in Original Dataset but Dropped from Table on Accident
df_new.at[21, "Annual Average Wage"] = '$76,600'
df_new.at[21, "Average Hourly Wage"] = '$36.83'

# Correct Read Html Error 
#df_new.at[21, "Average Hourly Wage"] = '$36.83'
df_new["Average Hourly Wage"] = df_new["Average Hourly Wage"].replace('<\/\w+', '', regex = True)

# No DC data
df_new = df_new.dropna()

# %%
cols = ['Price',	'Annual Average Wage',	'Average Hourly Wage']
df_new[cols]= df_new[cols].replace('\$', '', regex = True)
df_new[cols]= df_new[cols].replace(',', '', regex = True).astype(float)

# %%
# Tax Burden by State
# IP ADDRESS BLOCKED - Use Backup CSV file
#url = "https://wallethub.com/edu/states-with-highest-lowest-tax-burden/20494"
#response = requests.get(url)
#print(response.status_code)

# %%
#soup = BeautifulSoup(response.text, 'html.parser')
#table3 = soup.find_all("table")

# %%
#df3 = pd.read_html(str(table3))
# convert list to dataframe
#df3 = pd.DataFrame(df3[0])
#df3.head()

# %%
#df3 = df3.drop(['Overall Rank*'], axis=1)
#df_new = df_new.merge(df3, how = 'left', on = "State")


# %%
# Clean up new DF
#cols = ['Property Tax Burden (%)', 'Individual Income Tax Burden (%)', 'Total Sales & Excise Tax Burden (%)']
#df_new[cols] = df_new[cols].replace('%\s\D\d+\D', '', regex = True).astype(float)
#df_new['Total Tax Burden (%)'] = df_new['Total Tax Burden (%)'].replace('%', '', regex = True).astype(float)
#df_new['Price'] = df_new['Price'].replace('\D', '', regex = True).astype(float)
#df_new.head()

# %%
# BACK UP CSV File
df3 = pd.read_csv("2023_tax_burden_backup.csv")
df3.head()

# %%
df_new = df_new.merge(df3, how = 'left', on = "State")
df_new.head()

# %%
# Calculate Mortgage Loan Amount
# Assume FHA
df_new['Mortgage Amount'] = df_new['Price'] * .965
df_new['Down Payment'] = df_new['Price'] * .035
df_new.head()

# %%
# Daily Mortgage Rate
url = "https://www.mortgagenewsdaily.com/mortgage-rates"
response = requests.get(url)
print(response.status_code)

# %%
soup = BeautifulSoup(response.text, 'html.parser')
table4 = soup.find_all("table")

# %%
lst4 = pd.read_html(str(table4))
# convert list to dataframe
#df4 = pd.DataFrame(df[0])
df4 = lst4[0]
df4

# %%
fha_rate = df4.iloc[4,1].replace('%', '')
(var, date) = df4.columns[0]
date = re.match('\d+\D\d+\D\d{2}', date).group()

col_name = "FHA Rate as of {}".format(date)
df_new[col_name] = fha_rate
df_new["Mortgage Term"] = 30
df_new.head()

# %%
df5 = pd.read_csv('2023_home_insurance_rates_by_state.csv')

df_new["Annual Home Insurance"] = ''

# %%
for i in range(len(df_new)):
    state = df_new.loc[i, 'State']
    loan = df_new.loc[i, "Mortgage Amount"]

    if loan < 300000:
        rate = df5.loc[df5['State'] == state, 'Rate at $200k'].values.squeeze()
        df_new.loc[i,"Annual Home Insurance"] = loan * rate
    elif loan < 400000:
        rate = df5.loc[df5['State'] == state, 'Rate at $300k'].values.squeeze()
        df_new.loc[i,"Annual Home Insurance"] = loan * rate
    elif loan < 500000:
        rate = df5.loc[df5['State'] == state, 'Rate at $400k'].values.squeeze()
        df_new.loc[i,"Annual Home Insurance"] = loan * rate
    else:
        rate = df5.loc[df5['State'] == state, 'Rate at $500k'].values.squeeze()
        df_new.loc[i,"Annual Home Insurance"] = loan * rate

# %%
# Monthly House Payment
loan = Loan(principal = 200000, interest=.06, term=30)
loan.monthly_payment

# %%
df_new["Monthly Mortgage"] = ''

# %%
rate_col = "FHA Rate as of {}".format(date)
df_new.loc[0,"Mortgage Term"]
# %%
for i in range(len(df_new)):
    rate_col = "FHA Rate as of {}".format(date)
    principal = df_new.loc[i, "Mortgage Amount"]
    interest =float(df_new.loc[i, rate_col])
    term = df_new.loc[i,"Mortgage Term"]
    loan = Loan(principal = principal, interest = (interest/100), term = term)
    df_new.loc[i, "Monthly Mortgage"] = float(loan.monthly_payment)  

# %%
df_new['PMI (1.5%)'] = df_new['Monthly Mortgage'] * 0.015

# %%
df_new["Monthly Housing Payments"] = ''
for i in range(len(df_new)): 
    m_mortgage = float(df_new.loc[i, "Monthly Mortgage"])
    m_propertytx = (df_new.loc[i, "Price"] *0.45* df_new.loc[i, "Property Tax Burden"]) / 1200
    m_pmi = df_new.loc[i, 'PMI (1.5%)']
    m_insurance = df_new.loc[i, 'Annual Home Insurance']/12
    df_new.loc[i,"Monthly Housing Payments"] = m_mortgage + m_propertytx + m_pmi + m_insurance
    #print(df_new.loc[i, 'State'], m_propertytx, m_pmi, m_insurance)

# %%
df_new["Monthly Individual Income"] = df_new["Annual Average Wage"]/12

# %%
df_new["Monthly Tax Adjusted Income"] = ''
for i in range(len(df_new)):
    salary = df_new.loc[i, "Annual Average Wage"]
    if salary < 44725:
        m_income = df_new.loc[i, "Annual Average Wage"]/12
        m_statetx = df_new.loc[i, "Individual Income Tax Burden"]/100
        df_new.loc[i,"Monthly Tax Adjusted Income"] = m_income * (.88 - m_statetx)
    elif salary < 95375:
        m_income = df_new.loc[i, "Annual Average Wage"]/12
        m_statetx = df_new.loc[i, "Individual Income Tax Burden"]/100
        df_new.loc[i,"Monthly Tax Adjusted Income"] = m_income * (.78 - m_statetx)
    else:
        m_income = df_new.loc[i, "Annual Average Wage"]/12
        m_statetx = df_new.loc[i, "Individual Income Tax Burden"]/100
        df_new.loc[i,"Monthly Tax Adjusted Income"] = m_income * (.88 - m_statetx)

# %%
df_new = df_new.rename(columns={"Price" : "Median House Price"})
df_new.head()

# %%
# Create CSV file
# df_new.to_csv('2023_state_dataset.csv')