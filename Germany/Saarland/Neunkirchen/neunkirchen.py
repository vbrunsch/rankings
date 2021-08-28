#!/usr/bin/env python
# coding: utf-8
#%pip install bs4
#%pip install urllib

import bs4
import urllib
import urllib.request  
from bs4 import BeautifulSoup
#import requests
import pandas as pd

url = 'https://www.landkreis-neunkirchen.de/index.php?id=3554'
html = urllib.request.urlopen(url)

htmlParse = BeautifulSoup(html, 'html.parser')

df = pd.DataFrame(index = ['Neunkirchen','Illingen','Ottweiler','Eppelborn','Merchweiler','Schiffweiler','Spiesen-Elversberg'])
import re

from datetime import timedelta
for x in range(1,15):
    to = pd.Timestamp.today() -timedelta(days=x)
    tod = to.strftime('%d.%m.%Y')
    text = htmlParse.get_text()
    matches = re.findall(tod+'.*\),', text)
    try:
      if re.findall('Illingen \+?(\d+)',matches[0].replace(u'\xa0', u' ')):
          ne = re.findall('Neunkirchen \+?(\d+)',matches[0].replace(u'\xa0', u' '))[0]
          il = re.findall('Illingen \+?(\d+)',matches[0].replace(u'\xa0', u' '))[0]
          ot = re.findall('Ottweiler \+?(\d+)',matches[0].replace(u'\xa0', u' '))[0]
          ep = re.findall('Eppelborn \+?(\d+)',matches[0].replace(u'\xa0', u' '))[0]
          me = re.findall('Merchweiler \+?(\d+)',matches[0].replace(u'\xa0', u' '))[0]
          sc = re.findall('Schiffweiler \+?(\d+)',matches[0].replace(u'\xa0', u' '))[0]
          sp = re.findall('Spiesen-Elversberg \+?(\d+)',matches[0].replace(u'\xa0', u' '))[0]
          df[tod] = [int(ne),int(il),int(ot),int(ep),int(me),int(sc),int(sp)]
      else:
          df[tod] = [0,0,0,0,0,0,0]
    except:
      df[tod] = [0,0,0,0,0,0,0]
if '27.08.2021' in df.columns:
  df['27.08.2021'] = [7,0,1,0,0,0,5]
print(df)

import numpy as np

df['last14'] = df.sum(axis = 1)
df['last7'] = df[df.columns[0]]+df[df.columns[1]]+df[df.columns[2]]+df[df.columns[3]]+df[df.columns[4]]+df[df.columns[5]]+df[df.columns[6]]

df['neg_l7']=np.where(df['last7']< 0, df['last7'], 0)
df['last7']= df['last7']-df['neg_l7']
df['last14']=np.where(df['last14']< 0, df['last14']-df['neg_l7'], df['last14']+df['neg_l7'])
df['last14']=np.where(df['last14']< df['last7'], df['last7'], df['last14'])

#df = df[['last7','last14']]

df['mix'] = np.where(df['last7'] == 0, 0.6, df['last7'])
df['mix'] = np.where(df['last14'] == 0, 0.2, df['mix'])


df.to_csv(f'Germany/Saarland/Neunkirchen/data/Neunkirchen_for_dw14_7.csv')
print(df)

mdf = df.copy()
mdf['Neuzugänge letzten 7 Tage_x'] = mdf['last7']
mdf['Gemeinde'] = mdf.index
mdf['Neuzugänge letzten 14 Tage'] = mdf['last14']
mdf['Neuzugänge letzten 7 Tage_y'] = mdf['Neuzugänge letzten 14 Tage']-mdf['Neuzugänge letzten 7 Tage_x']  
mdf['Covid-freie Wochen'] = 0
mdf['Covid-freie Wochen'] = np.where(mdf['Neuzugänge letzten 7 Tage_x'] == 0, 1, mdf['Covid-freie Wochen'])
mdf['Covid-freie Wochen'] = np.where(mdf['Neuzugänge letzten 14 Tage'] == 0 , 2, mdf['Covid-freie Wochen'])
mdf = mdf[['Gemeinde','Covid-freie Wochen','Neuzugänge letzten 14 Tage','Neuzugänge letzten 7 Tage_x','Neuzugänge letzten 7 Tage_y']]
#print(mdf)

cols=['Gemeinde','Covid-freie Wochen','Neuzugänge letzten 14 Tage','Neuzugänge letzten 7 Tage_x','Neuzugänge letzten 7 Tage_y']
thr = pd.DataFrame(mdf, columns=cols)
fin = thr.sort_values(['Covid-freie Wochen'], ascending=[False])
fin['week'] = fin['Covid-freie Wochen'].gt(13) 
tab = fin.sort_values(['week'], ascending=[False])
tab_t = tab[tab['week']==True]
tab_f = tab[tab['week']==False]
tab_f = tab_f.sort_values(['Neuzugänge letzten 7 Tage_x','Neuzugänge letzten 14 Tage'], ascending = [True,True])
tab_t = tab_t.sort_values(['Covid-freie Wochen','Neuzugänge letzten 7 Tage_x'], ascending = [False,True])
tab = tab_t.append(tab_f)
tab = tab.drop(['week'], axis=1)

#Percent Change

tab['PercentChange'] = 100*(tab['Neuzugänge letzten 7 Tage_x'] - tab['Neuzugänge letzten 7 Tage_y'])/(tab['Neuzugänge letzten 7 Tage_x']+tab['Neuzugänge letzten 7 Tage_y'])
tab['PercentChange'] = tab['PercentChange'].fillna(0.0)

tab = tab.drop(['Neuzugänge letzten 7 Tage_y'], axis = 1)
#tab.columns = ['Gemeinde', 'Covid-freie Wochen', 'Neue Fälle letzte 14 Tage', 'Letzte 7 Tage', 'Pct Change']

def highlighter(s):
    val_1 = s['Letzte 7 Tage']
    val_2 = s['Neue Fälle letzte 14 Tage']
    
    r=''
    try:
        if 0==val_2: #More than 2 Covid free weeks
            r = 'background-color: #24773B; color: #ffffff;'
        elif 0==val_1 : # less than 20 in last 2 weeks
            r = 'background-color: #89c540;' 
        elif 10>=val_1 >=1: #Yellow
            r = 'background-color: #f9cc3d;'
        elif 35>=val_1 >= 11: #Orange
            r = 'background-color: #f8961d;'
        elif 100>=val_1 >= 36: #Light Red
            r = 'background-color: #ef3d23;'
        elif 1000>=val_1 > 100: # Red
            r = 'background-color: #B11F24;'
        elif 10000>=val_1 > 1000: # Light Purple
            r = 'background-color: #652369;'
        elif val_1 > 10000: # Purple
            r = 'background-color: #36124B; color: #ffffff;'
    except Exception as e:
        r = 'background-color: white'
    if 0 == val_2:
        return [r]*(len(s)-2) + ['']*2
    else:
        return [r]*(len(s)-3) + [''] + [r] + ['']

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
tab['Platz'] = tab.reset_index().index
tab['Platz'] = tab['Platz'].add(1)
tab['Platz'] = np.where(tab['Neuzugänge letzten 14 Tage'] == 0 , 1, tab['Platz'])
tab['Trend'] = tab['PercentChange'].map(arrow)
tab['Percent Change'] = tab['PercentChange'].map('{:,.2f}%'.format) + tab['Trend']
tab = tab.drop(['Trend','PercentChange'], axis = 1)

tab.rename(columns = {'Neuzugänge letzten 14 Tage':'Neue Fälle letzte 14 Tage'}, inplace = True)
tab.rename(columns = {'Neuzugänge letzten 7 Tage_x':'Letzte 7 Tage'}, inplace = True)
tab.rename(columns = {'Percent Change':'Trend'}, inplace = True)
tab.rename(columns = {'Gemeinde':'Stadt/Gemeinde'}, inplace = True)


tab = tab[['Platz', 'Stadt/Gemeinde', 'Covid-freie Wochen', 'Neue Fälle letzte 14 Tage', 'Letzte 7 Tage','Trend']]
tab = tab.drop('Covid-freie Wochen', axis = 1)
s = tab.style.apply(highlighter, axis = 1).set_table_styles(styles).hide_index()

import time
toti = time.strftime('%m/%d/%Y %H:%M:%S')
toti = "<center><caption>Last Update: " + toti + " UTC</caption></center>"

try:        
    with open(f'Neunkirchen.html', 'w', encoding="utf-8") as out:
        body = s.render().replace('&#x2197;','<span style="color: red"> &#x2197;</span>') # red arrow up
        body = body.replace('&#x2198','<span style="color: green"> &#x2198;</span>') # green arrow down
        content = top + toti + body + bottom
        out.write(content)
except Exception as e:
    print(f'Error:\n{e}')
