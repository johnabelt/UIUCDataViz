import requests
import json
import pandas as pd

s = requests.Session()
s.get('https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf')

headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-US,en;q=0.9",
    "adrum": "isAjax:true",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest",
  "referrer": "https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf",
  "referrerPolicy": "no-referrer-when-downgrade",
  "mode": "cors"
}

dfFinal = pd.DataFrame(columns = ['Ticker', 'Name', 'Sector', 'AssetClass', 'MarketValue', 'Weight', 'NotionalValue', 'Shares',	'CUSIP',	'ISIN',	'SEDOL',	'Price',	'Location' ,'Exchange','Currency','FXRate', 'Maturity','MarketCurrency'])

for year in range(1990,2021):
    r = s.get('https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf/1467271812596.ajax?tab=all&fileType=json&asOfDate='+str(year)+'0630&_=1595745548968', headers=headers)

    rFormat = json.loads(r.text[1:])
    dfR = pd.DataFrame(rFormat['aaData'], columns = ['Ticker', 'Name', 'Sector', 'AssetClass', 'MarketValue', 'Weight', 'NotionalValue', 'Shares',	'CUSIP',	'ISIN',	'SEDOL',	'Price',	'Location' ,'Exchange','Currency','FXRate', 'Maturity','MarketCurrency'])

    for cName in ['MarketValue', 'Weight', 'NotionalValue', 'Shares', 'Price', 'Maturity']:
        dfR[cName] = [item['raw'] for item in dfR[cName]]
    dfR['Year'] = year
    dfFinal = dfFinal.append(dfR)
    print(year)
dfFinal.to_csv('weights2.csv')


dfFinal = pd.DataFrame(columns = ['Ticker', 'Name', 'Sector', 'AssetClass', 'MarketValue', 'Weight', 'NotionalValue', 'Shares',	'CUSIP',	'ISIN',	'SEDOL',	'Price',	'Location' ,'Exchange','Currency','FXRate', 'Maturity','MarketCurrency', 'Year'])
from datetime import date
from dateutil.rrule import rrule, DAILY, MONTHLY

a = date(2000, 1, 1)
b = date(2006, 12, 31)

for dt in rrule(DAILY, dtstart=a, until=b):
    if len(dfFinal[dfFinal['Year'] == dt.strftime("%Y")]) > 0: continue
    r = s.get('https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf/1467271812596.ajax?tab=all&fileType=json&asOfDate='+dt.strftime("%Y%m%d")+'&_=1595745548968', headers=headers)

    rFormat = json.loads(r.text[1:])
    dfR = pd.DataFrame(rFormat['aaData'], columns = ['Ticker', 'Name', 'Sector', 'AssetClass', 'MarketValue', 'Weight', 'NotionalValue', 'Shares',	'CUSIP',	'ISIN',	'SEDOL',	'Price',	'Location' ,'Exchange','Currency','FXRate', 'Maturity','MarketCurrency'])

    for cName in ['MarketValue', 'Weight', 'NotionalValue', 'Shares', 'Price', 'Maturity']:
        dfR[cName] = [item['raw'] for item in dfR[cName]]
    dfR['Year'] = dt.strftime("%Y")
    dfFinal = dfFinal.append(dfR)
    print(dt)
dfFinal.to_csv('weights3.csv')
