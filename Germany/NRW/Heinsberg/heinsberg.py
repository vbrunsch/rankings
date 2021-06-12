import sys
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time 
import requests
import re

url_s = 'https://www.gangelt.de/news/226-erster-corona-fall-in-nrw'
t = requests.get(url_s).text
soup = BeautifulSoup(t, "lxml")
container = soup.find("section",attrs={'class': 'article-content clearfix'})

sta = re.findall('Stand (..\...\.....)', t)
erk = re.findall('Erkelenz \((.*?)/.*?\)', t)
gan = re.findall('Gangelt \((.*?)/.*?\)', t)
gei = re.findall('Geilenkirchen \((.*?)/.*?\)', t)
hei = re.findall('Heinsberg \((.*?)/.*?\)', t)
hue = re.findall('Hückelhoven \((.*?)/.*?\)', t)
sel = re.findall('Selfkant \((.*?)/.*?\)', t)
ueb = re.findall('Übach-Palenberg \((.*?)/.*?\)', t)
wal = re.findall('Waldfeucht \((.*?)/.*?\)', t)
was = re.findall('Wassenberg \((.*?)/.*?\)', t)
weg = re.findall('Wegberg \((.*?)/.*?\)', t)

gem = ['Erkelenz','Gangelt','Geilenkirchen','Heinsberg','Hückelhoven','Selfkant','Übach-Palenberg','Waldfeucht','Wassenberg','Wegberg']
df = pd.DataFrame(data = [erk,gan,gei,hei,hue,sel,ueb,wal,was,weg], index = gem)
df = df.astype(int)
sta = sta[:-56]
df.columns = sta
print(df)
df.to_csv(f'Germany/NRW/Heinsberg/data/LK_Heinsberg_gesamt.csv')

from datetime import timedelta
neu = pd.DataFrame(index = gem)
for i in range(0,21):
  neu[df.columns[i]] = df[df.columns[i]]-df[df.columns[i+1]]
print(neu)
neu.to_csv(f'Germany/NRW/Heinsberg/data/LK_Heinsberg_neu.csv')

zus = pd.DataFrame(index = gem)
to = pd.Timestamp.today()# - timedelta(days = 2)
tod = to.strftime('%d.%m.%Y')
if tod != neu.columns[0]:
  sys.exit(f'No new data, last data from {neu.columns[0]}')

try:
  dat7 = to - timedelta(days = 7)
  dat7s = dat7.strftime('%d.%m.%Y')
  indat7 = list(neu.columns).index(dat7s)
except:
  try:
    dat7 = to - timedelta(days = 8)
    dat7s = dat7.strftime('%d.%m.%Y')
    indat7 = list(neu.columns).index(dat7s)
  except:
    try:
      dat7 = to - timedelta(days = 6)
      dat7s = dat7.strftime('%d.%m.%Y')
      indat7 = list(neu.columns).index(dat7s)
    except:
      try:
        dat7 = to - timedelta(days = 9)
        dat7s = dat7.strftime('%d.%m.%Y')
        indat7 = list(neu.columns).index(dat7s)
      except:
        dat7 = to - timedelta(days = 5)
        dat7s = dat7.strftime('%d.%m.%Y')
        indat7 = list(neu.columns).index(dat7s)

zus['last7'] = 0
for i in range(0,indat7+1):
  zus['last7'] = zus['last7'] + neu[neu.columns[i]]
  

try:
  dat14 = to - timedelta(days = 14)
  dat14s = dat14.strftime('%d.%m.%Y')
  indat14 = list(neu.columns).index(dat14s)
except:
  try:
    dat14 = to - timedelta(days = 15)
    dat14s = dat14.strftime('%d.%m.%Y')
    indat14 = list(neu.columns).index(dat14s)
  except:
    try:
      dat14 = to - timedelta(days = 13)
      dat14s = dat14.strftime('%d.%m.%Y')
      indat14 = list(neu.columns).index(dat14s)
    except:
      try:
        dat14 = to - timedelta(days = 16)
        dat14s = dat14.strftime('%d.%m.%Y')
        indat14 = list(neu.columns).index(dat14s)
      except:
        dat14 = to - timedelta(days = 12)
        dat14s = dat14.strftime('%d.%m.%Y')
        indat14 = list(neu.columns).index(dat14s)

zus['last14'] = 0
for i in range(0,indat14+1):
  zus['last14'] = zus['last14'] + neu[neu.columns[i]]

import numpy as np
zus['neg_l7']=np.where(zus['last7']< 0, zus['last7'], 0)
zus['last7']= zus['last7']-zus['neg_l7']
zus['last14']=np.where(zus['last14']< 0, zus['last14']-zus['neg_l7'], zus['last14']+zus['neg_l7'])
zus['last14']=np.where(zus['last14']< zus['last7'], zus['last7'], zus['last14'])
zus = zus[['last7','last14']]

zus['mix'] = np.where(zus['last7'] == 0, 0.6, zus['last7'])
zus['mix'] = np.where(zus['last14'] == 0, 0.2, zus['mix'])
zus['Gemeinde'] = zus.index
print(zus)
print(dat7s)
print(dat14s)
zus.to_csv(f'Germany/NRW/Heinsberg/data/Heinsberg_for_dw14_7.csv')

# For Rankings
mdf = zus.copy()
mdf = mdf.drop_duplicates()
mdf['Neuzugänge letzten 7 Tage_x'] = mdf['last7']
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
    with open(f'Heinsberg.html', 'w', encoding="utf-8") as out:
        body = s.render().replace('&#x2197;','<span style="color: red"> &#x2197;</span>') # red arrow up
        body = body.replace('&#x2198','<span style="color: green"> &#x2198;</span>') # green arrow down
        content = top + toti + body + bottom
        out.write(content)
except Exception as e:
    print(f'Error:\n{e}')
