# %%
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from mortgage import Loan
import re

# %% 
### DATA COLLECTION ###
## GROUP 1 - HOME PRICE

# Median House Price by State
url = "https://www.bankrate.com/real-estate/median-home-price/#median-price-by-state"
response = requests.get(url)
print(response.status_code)

# %%
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find_all("table")

# %%
df_house= pd.read_html(str(table))
# convert list to dataframe
df_house= pd.DataFrame(df_house[0])
df_house.head()
# %%
#df_med_house= df_med_house.sort_values(by="Price", ascending = False)
#df_med_house['rank'] = df_med_house['Median House Price'].rank(ascending = False)
#df_med_house

### GROUP 2 - INCOME 

# Average Salary by State
url = "https://www.newtraderu.com/2023/11/01/average-income-by-state/"
response = requests.get(url)
print(response.status_code)

# %%
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find_all("table")

# %%
lst = pd.read_html(str(table))
df_avg_sal = lst[0]
df_avg_sal.head()

## CLEAN-UP
# %%
df_new = df_house.merge(df_avg_sal, how = 'left', on = "State")
# Massuchasetts in Original Dataset but Dropped from Table on Accident
df_new.at[21, "Annual Average Wage"] = '$76,600'
df_new.at[21, "Average Hourly Wage"] = '$36.83'

# Correct Read Html Error 
#df_new.at[21, "Average Hourly Wage"] = '$36.83'
df_new["Average Hourly Wage"] = df_new["Average Hourly Wage"].replace('<\/\w+', '', regex = True)

# No DC data
df_new = df_new.dropna()

# %%
cols = ['Price', 'Annual Average Wage', 'Average Hourly Wage']
df_new[cols]= df_new[cols].replace('\$', '', regex = True)
df_new[cols]= df_new[cols].replace(',', '', regex = True).astype(float)
df_new = df_new.rename(columns={"Price" : "Median House Price"})

# %%
# Scrape Data Analyst Average Salary by State
url = "https://www.zippia.com/data-analyst-jobs/salary/"
response = requests.get(url)
print(response.status_code)

# %%
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find_all("table")

# %%
lst = pd.read_html(str(table))
df_analyst_sal = lst[0]
df_analyst_sal.head()

# %%
# Clean up
cols = ['Avg. Salary', 'Hourly Rate']
df_analyst_sal[cols]= df_analyst_sal[cols].replace('\$', '', regex = True)
df_analyst_sal[cols]= df_analyst_sal[cols].replace(',', '', regex = True).astype(float)
df_analyst_sal = df_analyst_sal.drop(["Rank"], axis=1)
df_analyst_sal = df_analyst_sal.rename(columns={"Avg. Salary" : "Data Analyst Average Salary"})
df_analyst_sal = df_analyst_sal.rename(columns={"Hourly Rate" : "Data Analyst Hourly Rate"})

# %%
updated_date = soup.find('div', {'class': "last-updated-date"}).text
updated_date = updated_date.strip('Updated ')
updated_date = datetime.strptime(updated_date, "%B %d, %Y")
updated_date = updated_date.strftime("%m/%d/%y")
date = updated_date.astype(str)


# %%
col_name = "Data Analyst Job Count as of ".format(updated_date.strftime("%m/%d/%y"))
df_analyst_sal = df_analyst_sal.rename(columns={"Job Count" : col_name})
df_analyst_sal

# %%
df_new = df_new.merge(df_analyst_sal, how = 'left', on = "State")
df_new.head()
# %%


# %%
### GROUP 3 - TAX RATES

# Tax Burden by State
#!!! IP ADDRESS BLOCKED - Use Backup CSV file !!!
#url = "https://wallethub.com/edu/states-with-highest-lowest-tax-burden/20494"
#response = requests.get(url)
#print(response.status_code)

# %%
#soup = BeautifulSoup(response.text, 'html.parser')
#table = soup.find_all("table")

# %%
#df_tax = pd.read_html(str(table))
# convert list to dataframe
#df_tax = pd.DataFrame(df_tax[0])
#df_tax.head()

# %%
#df_tax = df_tax.drop(['Overall Rank*'], axis=1)
#df_new = df_new.merge(df_tax, how = 'left', on = "State")

# %%
# Clean up new DF
#cols = ['Property Tax Burden (%)', 'Individual Income Tax Burden (%)', 'Total Sales & Excise Tax Burden (%)']
#df_new[cols] = df_new[cols].replace('%\s\D\d+\D', '', regex = True).astype(float)
#df_new['Total Tax Burden (%)'] = df_new['Total Tax Burden (%)'].replace('%', '', regex = True).astype(float)
#df_new['Median House Price'] = df_new['Median House Price'].replace('\D', '', regex = True).astype(float)
#df_new.head()

# %%
# BACK UP CSV File for Tax Rate
url = 'https://raw.githubusercontent.com/jbethan/finalproj_state_affordability/main/2023_tax_burden_backup.csv'
df_tax = pd.read_csv(url)
df_tax.head()

# %%
df_new = df_new.merge(df_tax, how = 'left', on = "State")
df_new = df_new.rename(columns={"Individual Income Tax Burden" : "Income Tax Burden"})
df_new = df_new.rename(columns={"Total Sales & Excise Tax Burden" : "Sales Tax Burden"})
df_new.head()

# %%
## GROUP 4 - RENT (Selenium code in average_rent_by_state.py)

# Average Rent Price & Sq Ft by State
url = 'https://raw.githubusercontent.com/jbethan/finalproj_state_affordability/main/2023_average_rent_by_state.csv'
df_rent = pd.read_csv(url, index_col=None)
df_rent.head()

# %%
df_new = df_new.merge(df_rent, how = 'left', on = "State")
df_new.head()

# %%
# GROUP 5 - MORTGAGE

# Calculate Mortgage Loan Amount
# Assume FHA
df_new['Mortgage Loan Amount'] = df_new['Median House Price'] * .965
df_new['Down Payment'] = df_new['Median House Price'] * .035
df_new.head()

# %%
# Daily Mortgage Rate
url = "https://www.mortgagenewsdaily.com/mortgage-rates"
response = requests.get(url)
print(response.status_code)

# %%
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find_all("table")

# %%
lst = pd.read_html(str(table))
# convert list to dataframe
df_morg_rate = lst[0]
df_morg_rate

# %%
fha_rate = df_morg_rate.iloc[4,1].replace('%', '')
(var, date) = df_morg_rate.columns[0]
date = re.match('\d+\D\d+\D\d{2}', date).group()

col_name = "FHA Rate as of {}".format(date)
df_new[col_name] = fha_rate
df_new["Mortgage Term"] = 30
df_new.head()

# %%
# GROUP 6 - HOME INSURANCE (Scraped in home_insurance_by_state.py)
df_house_ins = pd.read_csv('2023_home_insurance_rates_by_state.csv')

df_new["Annual Home Insurance"] = ''

# Calculate Insurance Estimate according to Median House Price for each State
# %%
for i in range(len(df_new)):
    state = df_new.loc[i, 'State']
    loan = df_new.loc[i, "Mortgage Loan Amount"]

    if loan < 300000:
        rate = df_house_ins.loc[df_house_ins['State'] == state, 'Rate at $200k'].values.squeeze()
        df_new.loc[i,"Annual Home Insurance"] = loan * rate
    elif loan < 400000:
        rate = df_house_ins.loc[df_house_ins['State'] == state, 'Rate at $300k'].values.squeeze()
        df_new.loc[i,"Annual Home Insurance"] = loan * rate
    elif loan < 500000:
        rate = df_house_ins.loc[df_house_ins['State'] == state, 'Rate at $400k'].values.squeeze()
        df_new.loc[i,"Annual Home Insurance"] = loan * rate
    else:
        rate = df_house_ins.loc[df_house_ins['State'] == state, 'Rate at $500k'].values.squeeze()
        df_new.loc[i,"Annual Home Insurance"] = loan * rate

### DATA WRANGLING
# %%
# Calculate Monthly Mortgage Cost
loan = Loan(principal = 200000, interest=.06, term=30)
loan.monthly_payment

# %%
df_new["Monthly Mortgage Cost"] = ''

# %%
rate_col = "FHA Rate as of {}".format(date)
df_new.loc[0,"Mortgage Term"]
# %%
for i in range(len(df_new)):
    rate_col = "FHA Rate as of {}".format(date)
    principal = df_new.loc[i, "Mortgage Loan Amount"]
    interest =float(df_new.loc[i, rate_col])
    term = df_new.loc[i,"Mortgage Term"]
    loan = Loan(principal = principal, interest = (interest/100), term = term)
    df_new.loc[i, "Monthly Mortgage Cost"] = float(loan.monthly_payment)  

# %%
# Calculate Monthly PMI Cost
df_new['PMI (@1.5%)'] = df_new['Monthly Mortgage Cost'] * 0.015

# %%
# Calculate total Monthly House Payment
df_new["Monthly House Payment"] = ''
for i in range(len(df_new)): 
    m_mortgage = float(df_new.loc[i, "Monthly Mortgage Cost"])
    m_propertytx = (df_new.loc[i, "Median House Price"] *0.45* df_new.loc[i, "Property Tax Burden"]) / 1200
    m_pmi = df_new.loc[i, 'PMI (@1.5%)']
    m_insurance = df_new.loc[i, 'Annual Home Insurance']/12
    df_new.loc[i,"Monthly House Payment"] = m_mortgage + m_propertytx + m_pmi + m_insurance
    #print(df_new.loc[i, 'State'], m_propertytx, m_pmi, m_insurance)

# %%
# Calculate Monthly Gross Income
df_new["Monthly Gross Income"] = df_new["Annual Average Wage"]/12

# %%
# Calculate Income Adjusted for Taxes
df_new["Monthly Tax Adjusted Income"] = ''
for i in range(len(df_new)):
    salary = df_new.loc[i, "Annual Average Wage"]
    if salary < 44725:
        m_income = df_new.loc["Monthly Gross Income"]
        m_statetx = df_new.loc[i, "Income Tax Burden"]/100
        df_new.loc[i,"Monthly Tax Adjusted Income"] = m_income * (.88 - m_statetx)
    elif salary < 95375:
        m_income = df_new.loc["Monthly Gross Income"]
        m_statetx = df_new.loc[i, "Income Tax Burden"]/100
        df_new.loc[i,"Monthly Tax Adjusted Income"] = m_income * (.78 - m_statetx)
    else:
        m_income = df_new.loc["Monthly Gross Income"]
        m_statetx = df_new.loc[i, "Income Tax Burden"]/100
        df_new.loc[i,"Monthly Tax Adjusted Income"] = m_income * (.88 - m_statetx)

# %%
df_new.head()

# %%
# Create CSV file
# df_new.to_csv('2023_state_dataset.csv')