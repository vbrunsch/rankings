#!/usr/bin/env python
# coding: utf-8

import numpy as np
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import datetime
from datetime import timedelta
import pandas as pd


mun = pd.DataFrame()
now = datetime.date.today()
yesterday = now - timedelta(days=1)
start = now - timedelta(days=22)
date_list = pd.date_range(start=start,end=yesterday).tolist()
for d in date_list:  
    if d.weekday() in [1,2,3,4,5]:
        date_time = d.strftime("%Y%m%d")
        try:#if date_time != '20211102' and date_time != '20211112':
          url = f"https://epistat.sciensano.be/Data/{date_time}/COVID19BE_CASES_MUNI_CUM_{date_time}.csv"
          print(d)
          df = pd.read_csv(url)
          df = df.dropna(subset=['NIS5'])
          df['TX_ADM_DSTR_DESCR_NL'] = df['TX_ADM_DSTR_DESCR_NL'].str.replace('Arrondissement d\’', '')
          df['TX_ADM_DSTR_DESCR_NL'] = df['TX_ADM_DSTR_DESCR_NL'].str.replace('Arrondissement de', '')
          df['TX_ADM_DSTR_DESCR_NL'] = df['TX_ADM_DSTR_DESCR_NL'].str.replace('Arrondissement', '')
          df['TX_ADM_DSTR_DESCR_FR'] = df['TX_ADM_DSTR_DESCR_FR'].str.replace('Arrondissement d\’', '')
          df['TX_ADM_DSTR_DESCR_FR'] = df['TX_ADM_DSTR_DESCR_FR'].str.replace('Arrondissement de', '')
          df['TX_ADM_DSTR_DESCR_FR'] = df['TX_ADM_DSTR_DESCR_FR'].str.replace('Arrondissement', '')

          df['arr'] = df['TX_ADM_DSTR_DESCR_NL']
          df.loc[df['TX_ADM_DSTR_DESCR_NL'] != df['TX_ADM_DSTR_DESCR_FR'], 'arr'] = df['TX_ADM_DSTR_DESCR_NL'] + '/' + df['TX_ADM_DSTR_DESCR_FR']

          df.loc[df['CASES'] == '<5', 'CASES'] = 1
          df = df.drop(['TX_DESCR_NL','TX_DESCR_FR','NIS5'], axis = 1)
          df = df.rename(columns={'CASES': d})
          df[d] = df[d].astype(str).astype(int)
          df = df.groupby(['arr']).sum() 
          if mun.empty:
              mun = df.copy()
          else:
              mun = mun.join(df)
        except:
          try:
            mun[d] = mun[mun.columns[-1]]
          except:
            print(d)
mun = mun.T


cols=['District(NL/FR)','COVID-Free Days','New Cases in Last 14 Days', 'Last7', 'Previous7']
collect = []

for d in mun.columns:
    n = mun[d].astype(str).astype(int)
    ave = n.diff()
    las = len(ave)-14
    last_forteen = int(ave[las:].sum().item())
    if last_forteen < 0:
        last_forteen = 0
    last7 = int(ave[len(ave)-7:].sum().item()) #last week
    prev7 = int(ave[len(ave)-14:len(ave)-7].sum().item()) #prev week
    if last7 < 0:
        last7 = 0
    if last7 > last_forteen:
        last_forteen = last7
    if prev7 < 0:
        prev7 = 0
    if (last7 == 0) & (last_forteen == 0):
        prev7 = 0
    i = len(ave)-1
    c = 0
    while i > 0:
        if ave[i] <= 0:
            c = c + 1
        else:
            i = 0
        i = i - 1

    collect.append((d,
                   c,
                   last_forteen,
                   last7,
                   prev7))

    
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

#Percent Change

tab['PercentChange'] = 100*(tab['Last7'] - tab['Previous7'])/(tab['Last7']+tab['Previous7'])
tab['PercentChange'] = tab['PercentChange'].fillna(0.0)

tab = tab.drop(['Previous7'], axis = 1)
tab.columns = ['District(NL/FR)', 'COVID-Free Days', 'New Cases in Last 14 Days', 'Last 7 Days', 'Pct Change']

def highlighter(s):
    val_1 = s['COVID-Free Days']
    val_2 = s['New Cases in Last 14 Days']
    
    r=''
    try:
        if val_1>=14: #More than 14 Covid free days
            r = 'background-color: #24773B; color: #ffffff;'
        elif 20>=val_2 : # less than 20 in last 2 weeks
            r = 'background-color: #89c540;' 
        elif 200>=val_2 >=21: #Yellow
            r = 'background-color: #f9cc3d;'
        elif 1000>=val_2 >= 201: #Orange
            r = 'background-color: #f8961d;'
        elif 20000>=val_2 >= 1001: #Light Red
            r = 'background-color: #ef3d23;'
        elif 200000>=val_2 > 20001: # Red
            r = 'background-color: #B11F24;'
        elif 1000000>=val_2 > 200001: # Light Purple
            r = 'background-color: #652369;'
        elif val_2 > 1000000: # Purple
            r = 'background-color: #36124B; color: #ffffff;'
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
#tab.loc[tab['COVID-Free Days']==idx.size,['Rank']] = 1 
tab['Trend'] = tab['Pct Change'].map(arrow)
tab['Percent Change'] = tab['Pct Change'].map('{:,.2f}%'.format) + tab['Trend']
tab = tab.drop(['Trend','Pct Change'], axis = 1)

tab = tab[['Rank', 'District(NL/FR)', 'COVID-Free Days', 'New Cases in Last 14 Days','Last 7 Days','Percent Change']]       
s = tab.style.apply(highlighter, axis = 1).set_table_styles(styles).hide_index()

import datetime
from datetime import date
x = date.today()
d = x.weekday()
day =["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
totime = datetime.datetime.now()
toti = '<center><caption>'+'Last Update: '+day[d]+ ', '+ totime.strftime('%Y-%m-%d, %H:%M:%S') + ' ' + totime.astimezone().tzname() + '</caption></center>'

try:        
    with open(f'Belgium_Districts.html', 'w', encoding="utf-8") as out:
        body = s.render().replace('&#x2197;','<span style="color: red"> &#x2197;</span>') # red arrow up
        body = body.replace('&#x2198','<span style="color: green"> &#x2198;</span>') # green arrow down
        content = top + toti + body + bottom
        out.write(content)
except Exception as e:
    print(f'Error:\n{e}')
