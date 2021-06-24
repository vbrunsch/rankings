import bs4
import urllib
import urllib.request  
from bs4 import BeautifulSoup
import pandas as pd

import re
import requests

url = 'https://infogram.com/1prlze1gwz52zkfg2105gzn9yecm3z5vrgn'
html = urllib.request.urlopen(url)
htmlParse = BeautifulSoup(html, 'html.parser')
lin = re.findall('window.infographicData=(.*);', str(htmlParse))
import json
m_st = lin[0]
mu = json.loads(m_st)
mudf = pd.DataFrame(data=mu)
lay = mudf['elements'][20]

mudf2 = pd.DataFrame(list(lay.items()))
lay2 = mudf2[mudf2.columns[1]][3]
mudf3 = pd.DataFrame(list(lay2.items()))
lay3 = mudf3[mudf3.columns[1]][2]
mudf4 = pd.DataFrame(list(lay3.items()))
lay4 = mudf4[mudf4.columns[1]][99]
mudf5 = pd.DataFrame(list(lay4.items()))
lay5 = mudf5[mudf5.columns[1]][9]
mudf6 = pd.DataFrame(list(lay5.items()))
lay6 = mudf6[mudf6.columns[1]][0]
mudf7 = pd.DataFrame(list(lay6.items()))
df = pd.DataFrame(data = mudf7[mudf7.columns[1]][4])
df2 = pd.DataFrame(data = df[df.columns[4]][0])
print(df2)

df_neu = pd.DataFrame(data = None,columns=['Gemeinde','Gesamtfallzahlen','Neu'])
for i in range(2,12):
  df3 = pd.DataFrame(data = df[df.columns[i]][0])
  o = df3['value'][1]
  g = df3['value'][2]
  n = df3['value'][7]
  ne = pd.DataFrame(data = [[o,g,n]], columns = ['Gemeinde','Gesamtfallzahlen','Neu'])
  df_neu = df_neu.append(ne)
df_neu = df_neu.set_index('Gemeinde')
df_neu['Gesamtfallzahlen'] = df_neu['Gesamtfallzahlen'].str.replace('\.','')
df_neu['Neu'] = df_neu['Neu'].str.replace('\.','')
df_neu = df_neu.astype(int)
from datetime import timedelta
to = pd.Timestamp.today() - timedelta(days = 1)
tod = to.strftime('%m_%d_%Y')
df_neu.to_csv(f'Germany/NRW/Recklinghausen/data/Recklinghausen_{tod}.csv')
print(df_neu)

import numpy as np

da7 = to - timedelta(days = 7)
da7s = da7.strftime('%m_%d_%Y')
da14 = to - timedelta(days = 14)
da14s = da14.strftime('%m_%d_%Y')
old7 = pd.read_csv(f'Germany/NRW/Recklinghausen/data/Recklinghausen_{da7s}.csv', index_col = 0)
old14 = pd.read_csv(f'Germany/NRW/Recklinghausen/data/Recklinghausen_{da14s}.csv', index_col = 0)

zus = df_neu.copy()
zus['last7'] = zus[zus.columns[0]].astype(int) - old7[old7.columns[0]].astype(int)
zus['last14'] = zus[zus.columns[0]].astype(int) - old14[old14.columns[0]].astype(int)

zus['neg_l7']=np.where(zus['last7']< 0, zus['last7'], 0)
zus['last7']= zus['last7']-zus['neg_l7']
zus['last14']=np.where(zus['last14']< 0, zus['last14']-zus['neg_l7'], zus['last14']+zus['neg_l7'])
zus['last14']=np.where(zus['last14']< zus['last7'], zus['last7'], zus['last14'])

zus = zus[['last7','last14']]
zus['mix'] = np.where(zus['last7'] == 0, 0.6, zus['last7'])
zus['mix'] = np.where(zus['last14'] == 0, 0.2, zus['mix'])
zus['Gemeinde'] = zus.index

print(zus)
zus.to_csv(f'Germany/NRW/Recklinghausen/data/Recklinghausen_for_dw14_7.csv') 


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
tab.index.name = None
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
    with open(f'Recklinghausen.html', 'w', encoding="utf-8") as out:
        body = s.render().replace('&#x2197;','<span style="color: red"> &#x2197;</span>') # red arrow up
        body = body.replace('&#x2198','<span style="color: green"> &#x2198;</span>') # green arrow down
        content = top + toti + body + bottom
        out.write(content)
except Exception as e:
    print(f'Error:\n{e}')
