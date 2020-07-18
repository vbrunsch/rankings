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

cols = ['Country','COVID-free days','Total cases in the last 14 days']
to_ca = []

for j, country in enumerate(confirm.iloc[-1].sort_values(ascending=False).index[:]):

    
    #choosing offsets
    if country == 'China':
        offset = 0
    elif country == 'Korea, South':
        offset = 10
    else:
        offset = 30    



    #leaving out countries which haven't been vetted, or have bad data
    if country in do_not_include:
        continue
        
           
    focus =  confirm.loc[:,[country]].copy()[offset:]
    focus['new'] = focus[country] - focus[country].shift(1)
    
    # Correcting some data
    if country == 'France':
        focus.at['06/02', 'new'] = 0
        focus.at['06/04', 'new'] = 767
        
    # New Zealand cases are all in managed isolation since 06/17
    if country == 'New Zealand':
        focus['new'].loc['06/17':] = 0
    
   
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
    total=int(focus['new'][len(focus)-14:].sum()) #compute total cases
    if total < 0:
        total = 0
    to_ca.append((country,
                  c,
                  total))
    
fin = pd.DataFrame(to_ca,columns = cols)
fin['week'] = fin['COVID-free days'].gt(13) 
tab = fin.sort_values(['week'], ascending=[False])
tab_t = tab[tab['week']==True]
tab_f = tab[tab['week']==False]
tab_f = tab_f.sort_values(['Total cases in the last 14 days','COVID-free days'], ascending = [True,False])
tab_t = tab_t.sort_values(['COVID-free days','Total cases in the last 14 days'], ascending = [False,True])
tab = tab_t.append(tab_f)
tab = tab.drop(['week'], axis=1)

def highlighter(s):
    val_1 = s['COVID-free days']
    val_2 = s['Total cases in the last 14 days']
    r=''
    try:
        if val_1>=14:
            r = 'background-color: #018001;'
        elif 20>=val_2>=0 :
            r = 'background-color: #02be02;'
        elif 200>=val_2 >=21:
            r = 'background-color: #ffff01;'
        elif 1000>=val_2 >= 201:
            r = 'background-color: #ffa501;'
        elif 20000>=val_2 >= 1001:
            r = 'background-color: #ff3434;'
        elif val_2 > 20001:
            r = 'background-color: #990033;'
    except Exception as e:
        r = 'background-color: white'
    return [r]*len(s)

def hover(hover_color="#ffff99"):
    return dict(selector="tbody tr:hover td, tbody tr:hover th",
                props=[("background-color", "rgba(66, 165, 245, 0.2) !important")])


top = """

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



styles=[hover(),]
tab['Rank'] = tab.reset_index().index
tab['Rank'] = tab['Rank'].add(1)
tab = tab[['Rank', 'Country', 'COVID-free days', 'Total cases in the last 14 days']]       
s = tab.style.apply(highlighter, axis = 1).set_table_styles(styles).hide_index()
try:        
    with open(f'World.html', 'w', encoding="utf-8") as out:
        content = top + s.render() + bottom
        out.write(content)
except Exception as e:
    print(f'Error:\n{e}')