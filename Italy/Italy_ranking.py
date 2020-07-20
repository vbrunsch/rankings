#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
#

df = pd.read_csv('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv')
focus = df.copy().drop(['stato','codice_regione','codice_provincia','sigla_provincia','lat','long','note'], axis=1).set_index(['data'])
#totale_casi denominazione_provincia denominazione_regione

confirm_r = focus.groupby('denominazione_regione').sum().T
confirm_p = focus.groupby('denominazione_provincia').sum().T

cols=['Province','COVID-Free Days','New Cases in Last 14 Days']
import datetime as dt
collect = []
for country in confirm_p.columns:
    if country != 'In fase di definizione/aggiornamento':
        bula = focus[focus['denominazione_provincia']==country]
        bula2 = bula.copy().drop(['denominazione_provincia','denominazione_regione'], axis=1).diff()
        ave = bula2['totale_casi']
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
tab = tab[['Rank', 'Province', 'COVID-Free Days', 'New Cases in Last 14 Days']]       
s = tab.style.apply(highlighter, axis = 1).set_table_styles(styles).hide_index()
try:        
    with open(f'Italy.html', 'w', encoding="utf-8") as out:
        content = top + s.render() + bottom
        out.write(content)
except Exception as e:
    print(f'Error:\n{e}')
