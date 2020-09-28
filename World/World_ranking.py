#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np

#JHU
df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
focus = df.copy().drop(['Lat','Long'], axis=1).set_index(['Country/Region','Province/State'])
confirm = focus.groupby('Country/Region').sum().T

confirm.index = pd.to_datetime(confirm.index)

date = pd.to_datetime("today").strftime('_%m_%d')
#print('Latest update time is:',date)

confirm['time'] = pd.to_datetime(confirm.index)
confirm.index = confirm.time.dt.strftime('%m/%d')
confirm.drop('time', axis=1, inplace=True)


do_not_include = ['Antigua and Barbuda', 'Angola', 'Benin', 'Botswana', 
                  'Burundi', 'Cabo Verde', 'Chad', 'Comoros', 
                  'Congo (Brazzaville)', 'Congo (Kinshasa)', "Cote d'lvoire", 'Central African Republic',
                  'Diamond Princess', 'Dominica', 'Equatorial Guinea',
                  'Eritrea', 'Ecuador', 'Eswatini','Ethiopia', 'Gabon', 
                  'Gambia', 'Ghana', 'Grenada', 'Guinea', 'Guinea-Bissau',
                  'Guyana', 'Laos', 'Lesotho', 'Liberia', 'Libya', 'Madagascar',
                  'Malawi', 'Maldives', 'Mauritania', 'Mozambique',
                  'MS Zaandam', 'Namibia', 'Nicaragua', 'Papua New Guinea',
                  'Rwanda', 'Saint Lucia', 
                  'Saint Vincent and the Grenadines', 'Sao Tome and Principe',
                  'Seychelles', 'Sierra Leone', 'South Sudan', 'Suriname', 'Syria', 
                  'Tanzania', 'Togo', 'Uganda', 'West Bank and Gaza',
                  'Western Sahara', 'Yemen', 'Zambia', 'Zimbabwe']

cols = ['Country','COVID-free days','Total cases in the last 14 days','Last7','Previous7']
to_ca = []

for j, country in enumerate(confirm.iloc[-1].sort_values(ascending=False).index[:]):

    
    #choosing offsets
    if country == 'China':
        offset = 0
    elif country == 'Korea, South':
        offset = 10
    else:
        offset = 30    



    # leaving out countries which haven't been vetted, or have bad data
    if country in do_not_include:
        continue
        
           
    focus =  confirm.loc[:,[country]].copy()[offset:]
    focus['new'] = focus[country] - focus[country].shift(1)
    
    # Correcting some data
    if country == 'France':
        focus.at['06/02', 'new'] = 0
        focus.at['06/04', 'new'] = 767
        
    # New Zealand
    if country == 'New Zealand':
        import requests
        url = 'https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-current-situation/covid-19-current-cases/covid-19-current-cases-details'

        header = {
          "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
          "X-Requested-With": "XMLHttpRequest"
        }

        r = requests.get(url, headers=header)

        dfs = pd.read_html(r.text)
        hm = dfs[0]
        nz = hm[['Date notified of potential case','Overseas travel']]
        nz['new'] = 1
        nz = nz[nz['Overseas travel'] != 'Yes']
        tod = pd.to_datetime('today')
        idx = pd.date_range('02-26-2020', tod)
        focus = nz.groupby(['Date notified of potential case']).sum()
        focus.index = pd.to_datetime(focus.index, dayfirst=True)
        focus = focus.reindex(idx, fill_value=0)

    # Thailand cases are all in managed isolation since 05/26
    if country == 'Thailand':
        import re
        import requests
        import time
        import datetime
        url_s = 'https://data.go.th/dataset/covid-19-daily'
        t = requests.get(url_s).text
        filenames = re.findall('https:(.+?)\.xlsx', t)
        url = 'https:' + filenames[0] + '.xlsx'
        df_t = pd.read_excel(url)
        #dayt = datetime.date(1899, 12, 30)
        #c = 0
        #for i in df_t[df_t.columns[6]]:
        #    df_t[df_t.columns[6]][c] = dayt + datetime.timedelta(days=i)
        #    c=c+1
        df_t = df_t.set_index([df_t.columns[6]])
        df_t.index.name = None
        df_t = df_t[df_t[df_t.columns[3]]=='Thailand']
        df_t['new'] = 0
        df_t.loc[pd.isna(df_t[df_t.columns[8]]),'new'] = 1
        tod = pd.to_datetime('today')
        idx = pd.date_range('01-22-2020', tod)
        df_t = df_t.groupby(df_t.index).sum()
        df_t.index = pd.to_datetime(df_t.index, dayfirst=True)
        focus = df_t.reindex(idx, fill_value=0)
   
    #correcting country names
    if country == 'Taiwan*':
        country = 'Taiwan'
    if country == 'Korea, South':
        country = 'South Korea'
    if country == 'United Arab Emirates':
        country = 'U.A.E.'
    if country == 'Bosnia and Herzegovina':
        country = 'Bosnia'

  
    i = len(focus['new']) -1
    c = 0
    while i > 0:
        if focus['new'][i] <= 0:
            c = c + 1
        else:
            i = 0
        i = i - 1
    total=int(focus['new'][len(focus)-14:].sum()) #compute total cases in last 14 days
    last7 = int(focus['new'][len(focus)-7:].sum()) #last week
    prev7 = int(focus['new'][len(focus)-14:len(focus)-7].sum()) #prev week
    if total < 0:
        total = 0
    if last7 < 0:
        last7 = 0
    if last7 > total:
        total = last7
    if prev7 < 0:
        prev7 = 0
    if (last7 == 0) & (total == 0):
        prev7 = 0
    
    to_ca.append((country,
                  c,
                  total,
                  last7,
                  prev7))
    
fin = pd.DataFrame(to_ca,columns = cols)
fin['week'] = fin['COVID-free days'].gt(13) 
tab = fin.sort_values(['week'], ascending=[False])
tab_t = tab[tab['week']==True]
tab_f = tab[tab['week']==False]
tab_f = tab_f.sort_values(['Total cases in the last 14 days','COVID-free days'], ascending = [True,False])
tab_t = tab_t.sort_values(['COVID-free days','Total cases in the last 14 days'], ascending = [False,True])
tab = tab_t.append(tab_f)
tab = tab.drop(['week'], axis=1)


#Percent Change

tab['PercentChange'] = 100*(tab['Last7'] - tab['Previous7'])/(tab['Last7']+tab['Previous7'])
tab['PercentChange'] = tab['PercentChange'].fillna(0.0)

tab = tab.drop(['Previous7'], axis = 1)
tab.columns = ['Country', 'COVID-Free Days', 'New Cases in Last 14 Days', 'Last 7 Days', 'Pct Change']

def highlighter(s):
    val_1 = s['COVID-Free Days']
    val_2 = s['New Cases in Last 14 Days']
    
    r=''
    try:
        if val_1>=14: #More than 14 Covid free days
            r = 'background-color: #018001; color: #ffffff;'
        elif 20>=val_2 : # less than 20 in last 2 weeks
            r = 'background-color: #02be02; color: #ffffff;'
        elif 200>=val_2 >=21: #Light green
            r = 'background-color: #ffff01;'
        elif 1000>=val_2 >= 201: #Yellow
            r = 'background-color: #ffa501;'
        elif 20000>=val_2 >= 1001: #Orange
            r = 'background-color: #ff3434;'
        elif val_2 > 20001: # Red
            r = 'background-color: #990033;'
    except Exception as e:
        r = 'background-color: white'
    return [r]*(len(s)-2) + ['']*2

def hover(hover_color="#ffff99"):
    return dict(selector="tbody tr:hover td, tbody tr:hover th",
                props=[("background-color", "rgba(66, 165, 245, 0.2) !important")])

top = """
<!DOCTYPE html>
<meta content="text/html;charset=utf-8" http-equiv="Content-Type">
<meta content="utf-8" http-equiv="encoding">
<html>
<head>
<style>
    h2 {
        text-align: center;
        font-family: Helvetica, Arial, sans-serif;
    }
    table { 
        margin-left: auto;
        margin-right: auto;
    }
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
    }
    th, td {
        padding: 5px;
        text-align: center;
        font-family: Helvetica, Arial, sans-serif;
        font-size: 90%;
    }
    table tbody tr:hover {
        background-color: #dddddd;
    }
    /*
    table tbody tr:hover td, table tbody tr:hover th {
  background-color: #dddddd !important;
    }
    /*
    .wide {
        width: 90%; 
    }
</style>
</head>
<body>
"""
bottom = """
</body>
</html>
"""

arrow = lambda x : ' &#x2197;' if x>0 else (' &#x2192' if x ==0  else ' &#x2198')
styles=[hover(),]
tab['Rank'] = tab.reset_index().index
tab['Rank'] = tab['Rank'].add(1)
tab['Trend'] = tab['Pct Change'].map(arrow)
tab['Percent Change'] = tab['Pct Change'].map('{:,.2f}%'.format) + tab['Trend']
tab = tab.drop(['Trend','Pct Change'], axis = 1)

tab = tab[['Rank', 'Country', 'COVID-Free Days', 'New Cases in Last 14 Days','Last 7 Days','Percent Change']]       
s = tab.style.apply(highlighter, axis = 1).set_table_styles(styles).hide_index()

try:        
    with open(f'World.html', 'w', encoding="utf-8") as out:
        body = s.render().replace('&#x2197;','<span style="color: red"> &#x2197;</span>') # red arrow up
        body = body.replace('&#x2198','<span style="color: green"> &#x2198;</span>') # green arrow down
        content = top + body + bottom
        out.write(content)
except Exception as e:
    print(f'Error:\n{e}')
