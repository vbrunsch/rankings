#!/usr/bin/env python
# coding: utf-8


import json

import numpy as np
import pandas as pd
import os

data0=pd.read_csv("https://raw.githubusercontent.com/obuchel/classification/master/donnees-tests-covid19-labo-quotidien-2020-05-29-19h00.csv",sep=';',engine='python')
print(data0.columns)
df2=data0.groupby(["dep","jour"])["nb_pos"].sum().reset_index()
c1=['2020-05-14','2020-05-15','2020-05-16','2020-05-17','2020-05-18','2020-05-19','2020-05-20','2020-05-21','2020-05-22','2020-05-23','2020-05-24','2020-05-25','2020-05-26','2020-05-27','2020-05-28','2020-05-29']
df3=df2[np.isin(df2['jour'], c1, invert=True)]

#df3['jour']=df3['jour'].dt.date.to_string().replace("\n1","").replace("\n2","")
df4=df3.rename(columns={'dep': 'Combined_Key', 'jour':'jour','nb_pos': 'P'})
#dep;jour;clage_covid;nb_test;nb_pos;nb_test_h;nb_pos_h;nb_test_f;nb_pos_f

data = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/406c6a23-e283-4300-9484-54e78c8ae675',sep=';',engine="python")
#print(data.columns)
data=data[data['cl_age90']==0]
data["Combined_Key"]=data["dep"]
df_=data.groupby(["Combined_Key","jour"])["P"].sum().reset_index()
df=pd.concat([df4, df_])
#print(df4.columns,df_.columns,df.columns)

fr_de_di = pd.read_csv(r'france_dict.csv')

dic_dep = dict(zip(fr_de_di.Code, fr_de_di.Nom))

df['Departement'] = df['Combined_Key'].map(dic_dep)

cols=['Departement','COVID-Free Days','New Cases in Last 14 Days', 'Last7', 'Previous7']
collect = []

for d in df['Departement'].unique():
    focus = df[df['Departement']==d]
    focus = focus.set_index('jour')
    ave = focus['P']
    ave.index.name = None
    ave.index = pd.to_datetime(ave.index)
    las = len(ave)-14
    last_forteen = int(ave[las:].sum().item())
    #last_forteen = sum(ave[las:])
    if last_forteen < 0:
        last_forteen = 0
    last7 = int(ave[len(ave)-7:].sum().item()) #last week
    prev7 = int(ave[len(ave)-14:len(ave)-7].sum().item()) #prev week
    #last7 = sum(ave[len(ave)-7:]) #last week
    #prev7 = sum(ave[len(ave)-14:len(ave)-7]) #prev week
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
    while i > -1:
        if ave.values[i] <= 0:
            c = c + 1
        else:
            i = 0
        i = i - 1

    collect.append((d,
                   int(c),
                   int(last_forteen),
                   int(last7),
                   int(prev7)))
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
tab.columns = ['Departement', 'COVID-Free Days', 'New Cases in Last 14 Days', 'Last 7 Days', 'Pct Change']

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
tab['Percent Change'] = tab['Pct Change'].map('{:,.2f}%'.format)+ tab['Trend']
tab = tab.drop(['Trend','Pct Change'], axis = 1)

tab = tab[['Rank', 'Departement', 'COVID-Free Days', 'New Cases in Last 14 Days','Last 7 Days','Percent Change']]       
s = tab.style.apply(highlighter, axis = 1).set_table_styles(styles).hide_index()

import datetime
from datetime import date
x = date.today()
d = x.weekday()
day =["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
totime = datetime.datetime.now()
toti = '<center><caption>'+'Last Update: '+day[d]+ ', '+ totime.strftime('%Y-%m-%d, %H:%M:%S') + ' ' + totime.astimezone().tzname() + '</caption></center>'

try:        
    with open(f'France.html', 'w', encoding="utf-8") as out:
        body = s.render().replace('&#x2197;','<span style="color: red"> &#x2197;</span>') # red arrow up
        body = body.replace('&#x2198','<span style="color: green"> &#x2198;</span>') # green arrow down
        content = top + toti + body + bottom
        out.write(content)
except Exception as e:
    print(f'Error:\n{e}')
    print(focus)
