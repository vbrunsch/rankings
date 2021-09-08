#!/usr/bin/env python
# coding: utf-8
import os

import requests
import pandas as pd
from datetime import timedelta

url = 'https://www.uckermark.de/index.phtml?La=1&mNavID=1897.1&object=tx,2203.741.1&kat=&kuo=2&sub=0'
html = requests.get(url).content
df_list = pd.read_html(html)

names = df_list[1][0][2:15].to_frame()
names = names.rename(columns={0: 'Namen'})

new = df_list[1][1][2:15].to_frame()
new = new.rename(columns={1: 'Neue Fälle'}).fillna(0)
new['Namen'] = names
new['Neue Fälle'] = new['Neue Fälle'].astype(int)
new.set_index('Namen', inplace = True)
new.index.name = None
#print(new)

old_uck = pd.read_csv(f'Germany/Brandenburg/Uckermark/data/Uckermark old csv just new cases.csv').set_index('Unnamed: 0')
old_uck.index.name = None
#print(old_uck)

old_uck = old_uck.join(new)
#print(old_uck)

tod = pd.Timestamp.today()- timedelta(hours=6)
tod = tod.date()
tod2 = tod.strftime('%m/%d/%Y')
tod = tod.strftime('%-m/%-d/%Y')

print(tod)
print(tod2)
if tod == old_uck.columns[-2]:
    old_uck = old_uck.drop(old_uck.columns[-2], axis = 1)
#print(old_uck)

old_uck = old_uck.rename(columns={'Neue Fälle': tod})
#print(old_uck)

import re
h = html.decode("ISO-8859-1")
matches = re.findall('Stand: (.*),', h)
try:
    day = re.findall('(..)\. ', matches[0])[0]
    mon = re.findall('\. (.*)&nbsp; ', matches[0])[0]
    yea = re.findall('\. .* (....)', matches[0])[0]
except:
    day = re.findall('(..)\.', matches[0])[0]
    mon = re.findall('\.(..)', matches[0])[0]
    yea = re.findall('\..* (....)', matches[0])[0]




if mon == 'Januar':
    mon = '01'
elif mon == 'Februar':
    mon = '02'
elif mon == 'M&auml;rz':
    mon = '03'
elif mon == 'April':
    mon = '04'
elif mon == 'Mai':
    mon = '05'
elif mon == 'Juni':
    mon = '06'
elif mon == 'Juli':
    mon = '07'
elif mon == 'August':
    mon = '08'
elif mon == 'September':
    mon = '09'
elif mon == ' September':
    mon = '09'
elif mon == 'Oktober':
    mon = '10'
elif mon == 'November':
    mon = '11'
elif mon == 'Dezember':
    mon = '12'

sta = mon+day+yea
import datetime
dtsta = datetime.datetime.strptime(sta, '%m%d%Y').date()
dtold = datetime.datetime.strptime(old_uck.columns[-1], '%m/%d/%Y').date()
if dtsta != dtold:
    old_uck[old_uck.columns[-1]]= 0

old_uck.to_csv(f'Germany/Brandenburg/Uckermark/data/Uckermark old csv just new cases.csv')

l7 = list(old_uck)[-7:]
l14 = list(old_uck)[-14:]

sum7 = pd.DataFrame()
sum7['sum_7']= old_uck[l7].sum(axis=1)

sum14 = pd.DataFrame()
sum14['sum_14']= old_uck[l14].sum(axis=1)

#print(sum7)
#print(sum14)

import numpy as np
mdf = sum7.copy()
mdf['Neuzugänge letzten 7 Tage_x'] = sum7['sum_7'].astype(int)
mdf['Gemeinde'] = mdf.index
mdf = mdf.drop('sum_7', axis = 1)
mdf['Neuzugänge letzten 14 Tage'] = sum14.astype(int)
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

# Save pickle and last updated time for visualizations
region_path = "germany/brandenburg/uckermark"
config_path = "visualizations"
pickle_file = f"{config_path}/pickles/{region_path}.pkl"
last_updated_file = f"{config_path}/last-updated/{region_path}.log"
os.makedirs(os.path.dirname(pickle_file), exist_ok=True)
os.makedirs(os.path.dirname(last_updated_file), exist_ok=True)
tab.to_pickle(pickle_file)
with open(last_updated_file, 'w') as file:
    file.write(datetime.datetime.utcnow().strftime('%m/%d/%Y %H:%M:%S UTC'))

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
    with open(f'Uckermark.html', 'w', encoding="utf-8") as out:
        body = s.render().replace('&#x2197;','<span style="color: red"> &#x2197;</span>') # red arrow up
        body = body.replace('&#x2198','<span style="color: green"> &#x2198;</span>') # green arrow down
        content = top + toti + body + bottom
        out.write(content)
except Exception as e:
    print(f'Error:\n{e}')


    
## For Datawrapper
ags = pd.read_csv(f'Germany/Brandenburg/Uckermark/data/AGS2.csv')

get_ags = pd.Series(ags['AGS'].values,index=ags['Gemeinde']).to_dict()

sum7['Gemeinde'] = sum7.index
sum7['Gemeinde'] = sum7['Gemeinde'].str.replace(r'Stadt ', '')
sum7['Gemeinde'] = sum7['Gemeinde'].str.replace(r'Gemeinde ', '')
sum7['Gemeinde'] = sum7['Gemeinde'].str.replace(r'Amt ', '')
sum7['Gemeinde'] = sum7['Gemeinde'].str.replace('Schwedt \(Oder\)', 'Schwedt/Oder')

sum7 = sum7.append(sum7.loc[sum7['Gemeinde'] == 'Brüssow'], ignore_index = True)
sum7.at[len(sum7)-1,'Gemeinde']= 'Carmzow-Wallmow'
sum7 = sum7.append(sum7.loc[sum7['Gemeinde'] == 'Brüssow'], ignore_index = True)
sum7.at[len(sum7)-1,'Gemeinde']= 'Göritz'
sum7 = sum7.append(sum7.loc[sum7['Gemeinde'] == 'Brüssow'], ignore_index = True)
sum7.at[len(sum7)-1,'Gemeinde']= 'Schenkenberg'
sum7 = sum7.append(sum7.loc[sum7['Gemeinde'] == 'Brüssow'], ignore_index = True)
sum7.at[len(sum7)-1,'Gemeinde']= 'Schönfeld'

sum7 = sum7.append(sum7.loc[sum7['Gemeinde'] == 'Gerswalde'], ignore_index = True)
sum7.at[len(sum7)-1,'Gemeinde']= 'Flieth-Stegelitz'
sum7 = sum7.append(sum7.loc[sum7['Gemeinde'] == 'Gerswalde'], ignore_index = True)
sum7.at[len(sum7)-1,'Gemeinde']= 'Milmersdorf'
sum7 = sum7.append(sum7.loc[sum7['Gemeinde'] == 'Gerswalde'], ignore_index = True)
sum7.at[len(sum7)-1,'Gemeinde']= 'Mittenwalde'
sum7 = sum7.append(sum7.loc[sum7['Gemeinde'] == 'Gerswalde'], ignore_index = True)
sum7.at[len(sum7)-1,'Gemeinde']= 'Temmen-Ringenwalde'

sum7 = sum7.append(sum7.loc[sum7['Gemeinde'] == 'Oder-Welse'], ignore_index = True)
sum7.at[len(sum7)-1,'Gemeinde']= 'Berkholz-Meyenburg'
sum7 = sum7.append(sum7.loc[sum7['Gemeinde'] == 'Oder-Welse'], ignore_index = True)
sum7.at[len(sum7)-1,'Gemeinde']= 'Mark Landin'
sum7 = sum7.append(sum7.loc[sum7['Gemeinde'] == 'Oder-Welse'], ignore_index = True)
sum7.at[len(sum7)-1,'Gemeinde']= 'Passow'
sum7 = sum7.append(sum7.loc[sum7['Gemeinde'] == 'Oder-Welse'], ignore_index = True)
sum7.at[len(sum7)-1,'Gemeinde']= 'Pinnow'

sum7 = sum7.append(sum7.loc[sum7['Gemeinde'] == 'Gartz (Oder)'], ignore_index = True)
sum7.at[len(sum7)-1,'Gemeinde']= 'Casekow'
sum7 = sum7.append(sum7.loc[sum7['Gemeinde'] == 'Gartz (Oder)'], ignore_index = True)
sum7.at[len(sum7)-1,'Gemeinde']= 'Hohenselchow-Groß Pinnow'
sum7 = sum7.append(sum7.loc[sum7['Gemeinde'] == 'Gartz (Oder)'], ignore_index = True)
sum7.at[len(sum7)-1,'Gemeinde']= 'Mescherin'
sum7 = sum7.append(sum7.loc[sum7['Gemeinde'] == 'Gartz (Oder)'], ignore_index = True)
sum7.at[len(sum7)-1,'Gemeinde']= 'Tantow'

sum7 = sum7.append(sum7.loc[sum7['Gemeinde'] == 'Gramzow'], ignore_index = True)
sum7.at[len(sum7)-1,'Gemeinde']= 'Grünow'
sum7 = sum7.append(sum7.loc[sum7['Gemeinde'] == 'Gramzow'], ignore_index = True)
sum7.at[len(sum7)-1,'Gemeinde']= 'Oberuckersee'
sum7 = sum7.append(sum7.loc[sum7['Gemeinde'] == 'Gramzow'], ignore_index = True)
sum7.at[len(sum7)-1,'Gemeinde']= 'Randowtal'
sum7 = sum7.append(sum7.loc[sum7['Gemeinde'] == 'Gramzow'], ignore_index = True)
sum7.at[len(sum7)-1,'Gemeinde']= 'Uckerfelde'
sum7 = sum7.append(sum7.loc[sum7['Gemeinde'] == 'Gramzow'], ignore_index = True)
sum7.at[len(sum7)-1,'Gemeinde']= 'Zichow'


sum7['AGS'] = sum7['Gemeinde'].map(get_ags)
sum7 = sum7[sum7['Gemeinde'] != 'Oder-Welse']
sum7['AGS'] = sum7['AGS'].astype('int')
sum7['AGS'] = sum7['AGS'].astype('str')
sum7 = sum7.set_index('AGS')
#sum7 = sum7.drop('Gemeinde', axis = 1)
#sum7.index.astype('int').astype('str')
sum7.to_csv(f'Germany/Brandenburg/Uckermark/data/Uckermark_Staedte_for_dw7.csv')

sum14['Gemeinde'] = sum14.index
sum14['Gemeinde'] = sum14['Gemeinde'].str.replace(r'Stadt ', '')
sum14['Gemeinde'] = sum14['Gemeinde'].str.replace(r'Gemeinde ', '')
sum14['Gemeinde'] = sum14['Gemeinde'].str.replace(r'Amt ', '')
sum14['Gemeinde'] = sum14['Gemeinde'].str.replace(r'Schwedt \(Oder\)', 'Schwedt/Oder')

sum14 = sum14.append(sum14.loc[sum14['Gemeinde'] == 'Brüssow'], ignore_index = True)
sum14.at[len(sum14)-1,'Gemeinde']= 'Carmzow-Wallmow'
sum14 = sum14.append(sum14.loc[sum14['Gemeinde'] == 'Brüssow'], ignore_index = True)
sum14.at[len(sum14)-1,'Gemeinde']= 'Göritz'
sum14 = sum14.append(sum14.loc[sum14['Gemeinde'] == 'Brüssow'], ignore_index = True)
sum14.at[len(sum14)-1,'Gemeinde']= 'Schenkenberg'
sum14 = sum14.append(sum14.loc[sum14['Gemeinde'] == 'Brüssow'], ignore_index = True)
sum14.at[len(sum14)-1,'Gemeinde']= 'Schönfeld'

sum14 = sum14.append(sum14.loc[sum14['Gemeinde'] == 'Gerswalde'], ignore_index = True)
sum14.at[len(sum14)-1,'Gemeinde']= 'Flieth-Stegelitz'
sum14 = sum14.append(sum14.loc[sum14['Gemeinde'] == 'Gerswalde'], ignore_index = True)
sum14.at[len(sum14)-1,'Gemeinde']= 'Milmersdorf'
sum14 = sum14.append(sum14.loc[sum14['Gemeinde'] == 'Gerswalde'], ignore_index = True)
sum14.at[len(sum14)-1,'Gemeinde']= 'Mittenwalde'
sum14 = sum14.append(sum14.loc[sum14['Gemeinde'] == 'Gerswalde'], ignore_index = True)
sum14.at[len(sum14)-1,'Gemeinde']= 'Temmen-Ringenwalde'

sum14 = sum14.append(sum14.loc[sum14['Gemeinde'] == 'Oder-Welse'], ignore_index = True)
sum14.at[len(sum14)-1,'Gemeinde']= 'Berkholz-Meyenburg'
sum14 = sum14.append(sum14.loc[sum14['Gemeinde'] == 'Oder-Welse'], ignore_index = True)
sum14.at[len(sum14)-1,'Gemeinde']= 'Mark Landin'
sum14 = sum14.append(sum14.loc[sum14['Gemeinde'] == 'Oder-Welse'], ignore_index = True)
sum14.at[len(sum14)-1,'Gemeinde']= 'Passow'
sum14 = sum14.append(sum14.loc[sum14['Gemeinde'] == 'Oder-Welse'], ignore_index = True)
sum14.at[len(sum14)-1,'Gemeinde']= 'Pinnow'

sum14 = sum14.append(sum14.loc[sum14['Gemeinde'] == 'Gartz (Oder)'], ignore_index = True)
sum14.at[len(sum14)-1,'Gemeinde']= 'Casekow'
sum14 = sum14.append(sum14.loc[sum14['Gemeinde'] == 'Gartz (Oder)'], ignore_index = True)
sum14.at[len(sum14)-1,'Gemeinde']= 'Hohenselchow-Groß Pinnow'
sum14 = sum14.append(sum14.loc[sum14['Gemeinde'] == 'Gartz (Oder)'], ignore_index = True)
sum14.at[len(sum14)-1,'Gemeinde']= 'Mescherin'
sum14 = sum14.append(sum14.loc[sum14['Gemeinde'] == 'Gartz (Oder)'], ignore_index = True)
sum14.at[len(sum14)-1,'Gemeinde']= 'Tantow'

sum14 = sum14.append(sum14.loc[sum14['Gemeinde'] == 'Gramzow'], ignore_index = True)
sum14.at[len(sum14)-1,'Gemeinde']= 'Grünow'
sum14 = sum14.append(sum14.loc[sum14['Gemeinde'] == 'Gramzow'], ignore_index = True)
sum14.at[len(sum14)-1,'Gemeinde']= 'Oberuckersee'
sum14 = sum14.append(sum14.loc[sum14['Gemeinde'] == 'Gramzow'], ignore_index = True)
sum14.at[len(sum14)-1,'Gemeinde']= 'Randowtal'
sum14 = sum14.append(sum14.loc[sum14['Gemeinde'] == 'Gramzow'], ignore_index = True)
sum14.at[len(sum14)-1,'Gemeinde']= 'Uckerfelde'
sum14 = sum14.append(sum14.loc[sum14['Gemeinde'] == 'Gramzow'], ignore_index = True)
sum14.at[len(sum14)-1,'Gemeinde']= 'Zichow'

sum14['AGS'] = sum14['Gemeinde'].map(get_ags)
sum14 = sum14[sum14['Gemeinde'] != 'Oder-Welse']
sum14['AGS'] = sum14['AGS'].astype('int')
sum14['AGS'] = sum14['AGS'].astype('str')
sum14 = sum14.set_index('AGS')
#sum14 = sum14.drop('Gemeinde', axis = 1)
#sum14.index.astype('int').astype('str')
sum14.to_csv(f'Germany/Brandenburg/Uckermark/data/Uckermark_Staedte_for_dw14.csv')

sum14 = sum14.join(sum7['sum_7'])
sum14['mix'] = np.where(sum14['sum_7'] == 0, 0.6, sum14['sum_7'])
sum14['mix'] = np.where(sum14['sum_14'] == 0, 0.2, sum14['mix'])


sum14.to_csv(f'Germany/Brandenburg/Uckermark/data/Uckermark_Staedte_for_dw14_7.csv')
