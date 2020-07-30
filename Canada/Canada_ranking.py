#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np


df = pd.read_csv('https://raw.githubusercontent.com/ishaberry/Covid19Canada/master/timeseries_hr/cases_timeseries_hr.csv')
focus = df.copy().set_index(['date_report'])
focus = focus[focus.province != 'Repatriated']
focus = focus[focus.health_region != 'Not Reported']

#totale_casi denominazione_provincia denominazione_regione
abbrev = {
        'AB': 'Alberta',
        'BC': 'BC',
        'MB': 'Manitoba',
        'NB': 'New Brunswick',
        'NL': 'NL',
        'NS': 'Nova Scotia',
        'NT': 'NWT',
        'ON': 'Ontario',
        'PE': 'PEI',
        'QC': 'Quebec',
        'SK': 'Saskatchewan',
        'YT': 'Yukon'
}
in_abbrev = {v: k for k, v in abbrev.items()}
focus['abb'] = focus['province'].map(in_abbrev)

focus.loc[focus['health_region'] == 'Zone 1 (Moncton area)', 'health_region'] = 'Moncton area'
focus.loc[focus['health_region'] == 'Zone 2 (Saint John area)', 'health_region'] = 'Saint John area'
focus.loc[focus['health_region'] == 'Zone 3 (Fredericton area)', 'health_region'] = 'Fredericton area'
focus.loc[focus['health_region'] == 'Zone 4 (Edmundston area)', 'health_region'] = 'Edmundston area'
focus.loc[focus['health_region'] == 'Zone 5 (Campbellton area)', 'health_region'] = 'Campbellton area'
focus.loc[focus['health_region'] == 'Zone 6 (Bathurst area)', 'health_region'] = 'Bathurst area'
focus.loc[focus['health_region'] == 'Zone 7 (Miramichi area)', 'health_region'] = 'Miramichi area'
focus.loc[focus['health_region'] == 'Zone 1 - Western', 'health_region'] = 'Western'
focus.loc[focus['health_region'] == 'Zone 2 - Northern', 'health_region'] = 'Northern'
focus.loc[focus['health_region'] == 'Zone 3 - Eastern', 'health_region'] = 'Eastern'
focus.loc[focus['health_region'] == 'Zone 4 - Central', 'health_region'] = 'Central'

focus['co_st'] = focus['health_region']+', '+focus['abb']
confirm_r = focus.groupby('co_st').sum().T

cols=['Health Region','COVID-Free Days','New Cases in Last 14 Days']
collect = []
for country in confirm_r.columns:
    bula = focus[focus['co_st']==country]
    ave = bula['cases']
    las = len(ave)-14
    last_forteen = ave[las:].sum()
    if last_forteen < 0:
        last_forteen = 0
    last_forteen = int(last_forteen)
    i = len(ave)-1
    c = 0
    while i > 0:
        if ave[i] <= 0:
            c = c + 1
        else:
            i = 0
        i = i - 1

    collect.append((country,
                   c,
                   last_forteen))

thr = pd.DataFrame(collect, columns=cols)
fin = thr.sort_values(['COVID-Free Days'], ascending=[False])
fin['week'] = fin['COVID-Free Days'].gt(13) 
tab = fin.sort_values(['week'], ascending=[False])
tab_t = tab[tab['week']==True]
tab_f = tab[tab['week']==False]
tab_f = tab_f.sort_values(['New Cases in Last 14 Days','COVID-Free Days'], ascending = [True,False])
tab_t = tab_t.sort_values(['COVID-Free Days','New Cases in Last 14 Days'], ascending = [False,True])
tab = tab_t.append(tab_f)
tab = tab.drop(['week'], axis=1)

def highlighter(s):
    val_1 = s['COVID-Free Days']
    val_2 = s['New Cases in Last 14 Days']
    r=''
    try:
        if val_1>=14:
            r = 'background-color: #018001;'
        elif 20>=val_2 :
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
tab = tab[['Rank', 'Health Region', 'COVID-Free Days', 'New Cases in Last 14 Days']]       
s = tab.style.apply(highlighter, axis = 1).set_table_styles(styles).hide_index()
try:        
    with open(f'Canada.html', 'w', encoding="utf-8") as out:
        content = top + s.render() + bottom
        out.write(content)
except Exception as e:
    print(f'Error:\n{e}')