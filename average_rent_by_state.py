#%%
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

url = 'https://www.rentcafe.com/average-rent-market-trends/us/?t=638379614756101989&role=renter'

# %%
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(url)


#%%
soup = BeautifulSoup(driver.page_source, 'html.parser')

#%%
soup_table = soup.find_all("table")[1]

#%%
table = pd.read_html(str(soup_table))
df = table[0]
df.head()

#%%
cols = ['Average Rent',	'Average Apartment Size']
df[cols]= df[cols].replace('sq. ft.', '', regex = True)
df[cols]= df[cols].replace('\$', '', regex = True)
df[cols]= df[cols].replace(',', '', regex = True).astype(float)
df.head()

#%%
# Read to CSV
df.to_csv('2023_average_rent_by_state.csv')
# %%
driver.closer()
