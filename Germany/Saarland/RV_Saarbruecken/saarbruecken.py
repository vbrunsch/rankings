from datetime import timedelta
import bs4
import urllib
import urllib.request  
from bs4 import BeautifulSoup
import pandas as pd
import re
import requests

to = pd.Timestamp.today()# - timedelta(days = 1)
todf = to.strftime('%Y-%m-%d')
tod = to.strftime('%m_%d_%Y')

url = 'https://www.regionalverband-saarbruecken.de/corona/'
html = urllib.request.urlopen(url)
htmlParse = BeautifulSoup(html, 'html.parser')
lin = re.findall('a href="(.*)" title="Tägliche Fallzahl-Statistik aus dem Regionalverband"', str(htmlParse))
try:
  link = lin[0].replace('amp;', '')
except:
  try:
    lin = re.findall('a href="(.*)" title="Fallzahl-Statistik', str(htmlParse))
    link = lin[0].replace('amp;', '')
  except:
    lin = re.findall('a href="(.*)" title="Wochenend', str(htmlParse))
    link = lin[0].replace('amp;', '')
tab = pd.read_html(link)
df = tab[0]
df.columns = df.iloc[0]
df = df[1:-1]
df = df.replace('Sulzbach','Sulzbach/Saar')
df = df.set_index('Stadt/Gemeinde')
print(df)
df.to_csv(f'Germany/Saarland/RV_Saarbruecken/data/RV_Saarbruecken_{tod}.csv')

tim = re.findall('<meta content="(.*)" itemprop="datePublished"', str(htmlParse))
if tim[0] != todf:
  print(f'Data from {tim[0]}')
  print(f'Today is {todf}') 
else:
  print(f'Data is from today: {todf}')
  
yes = to - timedelta(days = 1)
yes = yes.strftime('%m_%d_%Y')
dfy = pd.read_csv(f'Germany/Saarland/RV_Saarbruecken/data/RV_Saarbruecken_{yes}.csv', index_col='Stadt/Gemeinde')

neu = pd.read_csv('Germany/Saarland/RV_Saarbruecken/data/RV_Saarbruecken_neu.csv', index_col='Stadt/Gemeinde')

neu[tod] = df['Fälle gesamt'].astype(int).values-dfy['Fälle gesamt'].astype(int).values

neu.to_csv('Germany/Saarland/RV_Saarbruecken/data/RV_Saarbruecken_neu.csv')

# For Datawrapper
import numpy as np
zus = pd.DataFrame()
zus['last7'] = neu[neu.columns[-1]] + neu[neu.columns[-2]] + neu[neu.columns[-3]] + neu[neu.columns[-4]] + neu[neu.columns[-5]] + neu[neu.columns[-6]] + neu[neu.columns[-7]]
zus['last14'] = zus['last7'] + neu[neu.columns[-8]] + neu[neu.columns[-9]] + neu[neu.columns[-10]] + neu[neu.columns[-11]] + neu[neu.columns[-12]] + neu[neu.columns[-13]] + neu[neu.columns[-14]]

zus['neg_l7']=np.where(zus['last7']< 0, zus['last7'], 0)
zus['last7']= zus['last7']-zus['neg_l7']
zus['last14']=np.where(zus['last14']< 0, zus['last14']-zus['neg_l7'], zus['last14']+zus['neg_l7'])
zus['last14']=np.where(zus['last14']< zus['last7'], zus['last7'], zus['last14'])

zus = zus[['last7','last14']]

zus['mix'] = np.where(zus['last7'] == 0, 0.6, zus['last7'])
zus['mix'] = np.where(zus['last14'] == 0, 0.2, zus['mix'])
zus['Gemeinde'] = zus.index

zus.to_csv(f'Germany/Saarland/RV_Saarbruecken/data/RV_Saarbruecken_for_dw14_7.csv')
print(zus) 

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

import datetime
# Save pickle and last updated time for visualizations
#region_path = "germany/rp/mayenkoblenz"
#config_path = "visualizations"
#pickle_file = f"{config_path}/pickles/{region_path}.pkl"
#last_updated_file = f"{config_path}/last-updated/{region_path}.log"
#os.makedirs(os.path.dirname(pickle_file), exist_ok=True)
#os.makedirs(os.path.dirname(last_updated_file), exist_ok=True)
#tab.to_pickle(pickle_file)
#with open(last_updated_file, 'w') as file:
#    file.write(datetime.datetime.utcnow().strftime('%m/%d/%Y %H:%M:%S UTC'))

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
    with open(f'RV_Saarbruecken.html', 'w', encoding="utf-8") as out:
        body = s.render().replace('&#x2197;','<span style="color: red"> &#x2197;</span>') # red arrow up
        body = body.replace('&#x2198','<span style="color: green"> &#x2198;</span>') # green arrow down
        content = top + toti + body + bottom
        out.write(content)
except Exception as e:
    print(f'Error:\n{e}')

