#!/usr/bin/env python
# coding: utf-8

import numpy as np
import json
import urllib.request
import pandas as pd

cols=['States and Territories','COVID-Free Days','New Cases in Last 14 Days', 'Last7', 'Previous7']
collect = []

with urllib.request.urlopen('https://atlas.jifo.co/api/connectors/ba66fc4e-9f3a-43f7-bd7c-190a6f89f183') as url:
    data = json.loads(url.read().decode())
result = pd.DataFrame(data)

ab = 0
for d in data['sheetNames']:
    df = result[result['sheetNames']==d]
    focus = pd.DataFrame(df['data'][ab],columns=df['data'][ab][0])
    ab = ab + 1
    focus = focus.iloc[1:].set_index('')
    focus.index.name = None
    #focus = focus.rename({focus.columns(0): 'Overseas', focus.columns(1): 'Known Local', focus.columns(2): 'Unknown Local (Community)', focus.columns(3): 'Interstate travel', focus.columns(4): 'Under investigation'}, axis=1)
    focus.columns = ['Overseas','Known Local','Unknown Local (Community)','Interstate travel','Under investigation']
    focus['Overseas'].replace('', np.nan, inplace=True)
    focus = focus.dropna()
    focus['Known Local'] = focus['Known Local'].astype(float)
    focus['Unknown Local (Community)'] = focus['Unknown Local (Community)'].astype(float)
    focus['Under investigation']=focus['Under investigation'].replace(r'\s+',np.nan,regex=True).replace('',np.nan)
    focus['Under investigation']=focus['Under investigation'].fillna(0)
    focus = focus.replace({',':''}, regex=True)
    focus['Under investigation'] = focus['Under investigation'].astype(float)
    #focus['local transmission'] = focus['Unknown Local (Community)']#+focus['Under investigation']+focus['Known Local']
    ave = focus[['Under investigation']]
    ave = ave.values
 
    las = len(ave)-14
    m = ave[las:]
    n = np.tile(0.0, len(m))
    if m[0]<=0:
        n[0]= 0
    else:
        n[0]=m[0]
    for i in range(1,len(m)):
        if n[i-1]+m[i]<0:
            n[i]=0
        else:
            n[i]=n[i-1]+m[i]
    last_forteen = n[i]
    if last_forteen < 0:
        last_forteen = 0
    
    las7 = len(ave)-7
    m7 = ave[las7:]
    n7 = np.tile(0.0, len(m7))
    if m7[0]<=0:
        n7[0]= 0
    else:
        n7[0]=m7[0]
    for i in range(1,len(m7)):
        if n7[i-1]+m7[i]<0:
            n7[i]=0
        else:
            n7[i]=n7[i-1]+m7[i]
    last7 = n7[i]
    prev7 = last_forteen - last7
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
    en = ave[i]
    while i > 0:
        if ave[i] <= 0:
            c = c + 1
            if en + ave[i-1]<=0:
                en = en + ave[i-1]
            else:
                i = 0
        else:
            i = 0
        i = i - 1    
    if d == 'NSW':
        dname = 'New South Wales'
    elif d =='VIC':
        dname = 'Victoria'
    elif d == 'QLD':
        dname = 'Queensland'
    elif d == 'SA':
        dname = 'South Australia'
    elif d == 'WA':
        dname = 'Western Australia'
    elif d == 'TAS':
        dname = 'Tasmania'
    elif d == 'NT':
        dname = 'Northern Territory'
    elif d == 'ACT':
        dname = 'Australian Capital Territory'

    c1=c
    last_forteen1 = last_forteen
    last71=last7
    prev71=prev7
    
    
    ave = focus[['Unknown Local (Community)']]
    ave = ave.values
    las = len(ave)-14
    m = ave[las:]
    n = np.tile(0.0, len(m))
    if m[0]<=0:
        n[0]= 0
    else:
        n[0]=m[0]
    for i in range(1,len(m)):
        if n[i-1]+m[i]<0:
            n[i]=0
        else:
            n[i]=n[i-1]+m[i]
    last_forteen = n[i]
    if last_forteen < 0:
        last_forteen = 0
    
    las7 = len(ave)-7
    m7 = ave[las7:]
    n7 = np.tile(0.0, len(m7))
    if m7[0]<=0:
        n7[0]= 0
    else:
        n7[0]=m7[0]
    for i in range(1,len(m7)):
        if n7[i-1]+m7[i]<0:
            n7[i]=0
        else:
            n7[i]=n7[i-1]+m7[i]
    last7 = n7[i]
    prev7 = last_forteen - last7
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
    en = ave[i]
    while i > 0:
        if ave[i] <= 0:
            c = c + 1
            if en + ave[i-1]<=0:
                en = en + ave[i-1]
            else:
                i = 0
        else:
            i = 0
        i = i - 1   
     
    c2=c
    last_forteen2 = last_forteen
    last72=last7
    prev72=prev7
    
    ave = focus[['Known Local']]
    ave = ave.values
    las = len(ave)-14
    m = ave[las:]
    n = np.tile(0.0, len(m))
    if m[0]<=0:
        n[0]= 0
    else:
        n[0]=m[0]
    for i in range(1,len(m)):
        if n[i-1]+m[i]<0:
            n[i]=0
        else:
            n[i]=n[i-1]+m[i]
    last_forteen = n[i]
    if last_forteen < 0:
        last_forteen = 0
    
    las7 = len(ave)-7
    m7 = ave[las7:]
    n7 = np.tile(0.0, len(m7))
    if m7[0]<=0:
        n7[0]= 0
    else:
        n7[0]=m7[0]
    for i in range(1,len(m7)):
        if n7[i-1]+m7[i]<0:
            n7[i]=0
        else:
            n7[i]=n7[i-1]+m7[i]
    last7 = n7[i]
    prev7 = last_forteen - last7
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
    en = ave[i]
    while i > 0:
        if ave[i] <= 0:
            c = c + 1
            if en + ave[i-1]<=0:
                en = en + ave[i-1]
            else:
                i = 0
        else:
            i = 0
        i = i - 1   
     
    c3=c
    last_forteen3 = last_forteen
    last73=last7
    prev73=prev7
    
    collect.append((dname,
                   int(min(c1,c2,c3)),
                   int(last_forteen1+last_forteen2+last_forteen3),
                   int(last71 + last72 + last73),
                   int(prev71 + prev72 + prev73)))
    
    
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
tab.columns = ['States and Territories', 'COVID-Free Days', 'New Cases in Last 14 Days', 'Last 7 Days', 'Pct Change']

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

tab = tab[['Rank', 'States and Territories', 'COVID-Free Days', 'New Cases in Last 14 Days','Last 7 Days','Percent Change']]       
s = tab.style.apply(highlighter, axis = 1).set_table_styles(styles).hide_index()

try:        
    with open(f'Australia.html', 'w', encoding="utf-8") as out:
        body = s.render().replace('&#x2197;','<span style="color: red"> &#x2197;</span>') # red arrow up
        body = body.replace('&#x2198','<span style="color: green"> &#x2198;</span>') # green arrow down
        content = top + body + bottom
        out.write(content)
except Exception as e:
    print(f'Error:\n{e}')

