#%%
import requests
import json
import prettytable
import pandas as pd

# %%
#headers = {'Content-type': 'application/json'}
#data = json.dumps({"seriesid": ['CUUR0000SA0','SUUR0000SA0'],"startyear":"2020", "endyear":"2023"})
#p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)

# The url for BLS API v2
url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'

payload = {}
file = open('bls_apikey.txt', 'r').read()

headers= {
  "apikey": file
}
key = '?registrationkey={}'.format(headers)


#%%
# Series stored as a dictionary
series_dict = {
    'ENU0100050010' : 'Alabama'
    }

# Start year and end year
dates = ('2020', '2022')

# Specify json as content type to return
headers = {'Content-type': 'application/json'}

# Submit the list of series as data
data = json.dumps({
    "seriesid": list(series_dict.keys()),
    "startyear": dates[0],
    "endyear": dates[1]})
print(data)

# %%
# Post request for the data
p = requests.post(
    '{}{}'.format(url, key),
    headers=headers,
    data=data).json()['Results']['series']

# %%
# Date index from first series
#date_list = [f"{i['year']}-{i['period'][1:]}-01" for i in p[0]['data']]
date_list = [f"{i['year']}" for i in p[0]['data']]
# Empty dataframe to fill with values
df = pd.DataFrame()

# Build a pandas series from the API results, p
for s in p:
    df[series_dict[s['seriesID']]] = pd.Series(
        index = pd.to_datetime(date_list),
        data = [i['value'] for i in s['data']]
        ).astype(float).iloc[::-1]

# Show last 5 results
df.tail()

# %%
print(p)

# %%
# STOP
json_data = json.loads(p.text)
for series in json_data['Results']['series']:
    x=prettytable.PrettyTable(["series id","year","period","value","footnotes"])
    seriesId = series['seriesID']
    for item in series['data']:
        year = item['year']
        period = item['period']
        value = item['value']
        footnotes=""
        for footnote in item['footnotes']:
            if footnote:
                footnotes = footnotes + footnote['text'] + ','
        if 'M01' <= period <= 'M12':
            x.add_row([seriesId,year,period,value,footnotes[0:-1]])
    output = open(seriesId + '.txt','w')
    output.write (x.get_string())
    output.close()
# %%
