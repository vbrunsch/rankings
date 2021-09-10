
import pytesseract
import shutil
import os
import random
try:
 from PIL import Image
except:# ImportError:
 import Image

import bs4
import urllib
import urllib.request  
from bs4 import BeautifulSoup
import pandas as pd

import re
import requests

import re
import numpy as np
import pandas as pd
from datetime import timedelta

url = 'https://www.kreis-mettmann-corona.de/Aktuelle-Meldungen/'
html = urllib.request.urlopen(url)
htmlParse = BeautifulSoup(html, 'html.parser')
lin = re.findall('"(\/Aktuelle-Meldungen\/Corona-Virus-[0-9]*-*[0-9]*-Infizierte.*?)"', str(htmlParse))
print(lin[0])

if 1 == 0:
 
 url2 = 'https://www.kreis-mettmann-corona.de' + lin[0]
 url2 = url2.replace('amp;','')
 #url2 = 'https://www.kreis-mettmann-corona.de/Aktuelle-Meldungen/Corona-Virus-130-Infizierte-23-510-Genesene-Inzidenz-18-7.php?object=tx,3535.5.1&ModID=7&FID=3535.324.1&NavID=3535.12&La=1&kat=3535.3'
 html2 = urllib.request.urlopen(url2)
 htmlParse2 = BeautifulSoup(html2, 'html.parser')
 lin2 = re.findall('"(\/media.*?g\.PNG.*)"', str(htmlParse2))
 imp = re.findall('" href="\/media\/custom\/(.*?g\.PNG.*?)"', str(htmlParse2))
 print(lin2)
 im_p = '"' + 'https://www.kreis-mettmann-corona.de' + lin2[1] + '"'

 os.system(f"wget {im_p}")
 #$wget ${im_p}

 ext_i = pytesseract.image_to_string(Image.open(imp[0]))


 infa = re.findall('[^\/].*?\/.*?\/([0-9]*)[^\/0-9]',ext_i)
 infa = infa[2:]
 infint = list(map(int, infa))
 infnp = np.array(infint)
 inf = infnp[infnp>1000]
inf =  [2378,2949,1461,1843,2894,2204,2472,1228,4512,5391,27332]
gem = ['Erkrath','Hilden','Haan','Heiligenhaus','Langenfeld','Mettmann','Monheim','Wülfrath','Ratingen','Velbert','Kreis Mettmann']
#gem = ['Erkrath','Haan','Heiligenhaus','Hilden','Langenfeld','Mettmann','Monheim','Ratingen','Velbert','Wülfrath','Kreis Mettmann']
#gem = ['Erkrath','Hilden','Monheim','Wülfrath','Haan','Heiligenhaus','Langenfeld','Mettmann','Ratingen','Velbert','Kreis Mettmann']
#gem = ['Erkrath','Hilden','Monheim','Wülfrath','Haan','Langenfeld','Ratingen','Kreis Mettmann','Heiligenhaus','Mettmann','Velbert']
df = pd.DataFrame(data = inf, index = gem)
df.columns = ['Gesamtfallzahlen']
to = pd.Timestamp.today() - timedelta(days = 1)
tod = to.strftime('%m_%d_%Y')
print(df)
df.to_csv(f'Germany/NRW/Mettmann/data/Mettmann_{tod}.csv')

da7 = to - timedelta(days = 7)
da7s = da7.strftime('%m_%d_%Y')
da14 = to - timedelta(days = 14)
da14s = da14.strftime('%m_%d_%Y')
old7 = pd.read_csv(f'Germany/NRW/Mettmann/data/Mettmann_{da7s}.csv', index_col = 0)
old14 = pd.read_csv(f'Germany/NRW/Mettmann/data/Mettmann_{da14s}.csv', index_col = 0)

zus = df.copy()
zus['last7'] = zus['Gesamtfallzahlen'].astype(int) - old7[old7.columns[0]].astype(int)
zus['last14'] = zus['Gesamtfallzahlen'].astype(int) - old14[old14.columns[0]].astype(int)

import numpy as np
zus['neg_l7']=np.where(zus['last7']< 0, zus['last7'], 0)
zus['last7']= zus['last7']-zus['neg_l7']
zus['last14']=np.where(zus['last14']< 0, zus['last14']-zus['neg_l7'], zus['last14']+zus['neg_l7'])
zus['last14']=np.where(zus['last14']< zus['last7'], zus['last7'], zus['last14'])
zus = zus[['last7','last14']]

zus['mix'] = np.where(zus['last7'] == 0, 0.6, zus['last7'])
zus['mix'] = np.where(zus['last14'] == 0, 0.2, zus['mix'])
zus['Gemeinde'] = zus.index

zus = zus.replace('Langenfeld','Langenfeld (Rhld.)')
zus = zus.replace('Monheim','Monheim am Rhein')
zus = zus.set_index('Gemeinde')
zus.index.name = None
zus['Gemeinde'] = zus.index

print(zus)
zus.to_csv(f'Germany/NRW/Mettmann/data/Mettmann_for_dw14_7.csv')

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
    with open(f'Mettmann.html', 'w', encoding="utf-8") as out:
        body = s.render().replace('&#x2197;','<span style="color: red"> &#x2197;</span>') # red arrow up
        body = body.replace('&#x2198','<span style="color: green"> &#x2198;</span>') # green arrow down
        content = top + toti + body + bottom
        out.write(content)
except Exception as e:
    print(f'Error:\n{e}')
