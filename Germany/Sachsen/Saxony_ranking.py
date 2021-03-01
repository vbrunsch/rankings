#!/usr/bin/env python
# coding: utf-8
import requests
import pandas as pd

url = 'https://www.coronavirus.sachsen.de/infektionsfaelle-in-sachsen-4151.html'
html = requests.get(url).content
df_list = pd.read_html(html)

import re
h = html.decode('utf-8')
matches = re.findall('LastUpdated: (...........)', h)
da = matches[0][:-1]
print(da)

# For Datawrapper Map

kfs = df_list[-12]
dre = int(round(kfs.loc[kfs['Unnamed: 0'] == 'Landeshauptstadt Dresden', kfs.columns[1]].item()/10 * 5.5678))
lei = int(round(kfs.loc[kfs['Unnamed: 0'] == 'Stadt Leipzig', kfs.columns[1]].item()/10 * 5.93145))
che = int(round(kfs.loc[kfs['Unnamed: 0'] == 'Stadt Chemnitz', kfs.columns[1]].item()/10 * 2.46334))

df = df_list[-11]
df1 = df_list[-10]
df2 = df_list[-9]
df3 = df_list[-8]
df4 = df_list[-7]
df5 = df_list[-6]
df6 = df_list[-5]
df7 = df_list[-4]
df8 = df_list[-3]
df9 = df_list[-2]

df = df.append(df1)
df = df.append(df2)
df = df.append(df3)
df = df.append(df4)
df = df.append(df5)
df = df.append(df6)
df = df.append(df7)
df = df.append(df8)
df = df.append(df9)

df['Gemeinde'] = df['Gemeinde'].str.replace(r', Stadt', '')
df['Gemeinde'] = df['Gemeinde'].str.replace(r', Kurort', '')
df['Gemeinde'] = df['Gemeinde'].str.replace(r', Hochschulstadt', '')
df['Gemeinde'] = df['Gemeinde'].str.replace(r', Universitätsstadt', '')
df['Gemeinde'] = df['Gemeinde'].str.replace(r'a. d.', 'a.d.')
df['Gemeinde'] = df['Gemeinde'].str.replace(r' \(.*', '')
df['Gemeinde'] = df['Gemeinde'].str.replace(r'Verwaltungsgemeinschaft Nünchritz/Glaubitz', 'Glaubitz')
df['Gemeinde'] = df['Gemeinde'].str.replace(r'Verwaltungsgemeinschaft Röderaue/Wülknitz', 'Wülknitz')
df['Gemeinde'] = df['Gemeinde'].str.replace(r'Verwaltungsgemeinschaft Schönfeld/Lampertswalde', 'Lampertswalde')
df = df.append(df.loc[df['Gemeinde'] == 'Glaubitz'], ignore_index = True)
df.at[len(df)-1,'Gemeinde']= 'Nünchritz'
df = df.append(df.loc[df['Gemeinde'] == 'Wülknitz'], ignore_index = True)
df.at[len(df)-1,'Gemeinde']= 'Röderaue'
df = df.append(df.loc[df['Gemeinde'] == 'Lampertswalde'], ignore_index = True)
df.at[len(df)-1,'Gemeinde']= 'Schönfeld'
df.loc[len(df.index)] = [0,'Dresden', dre,0,0]
df.loc[len(df.index)] = [0,'Leipzig', lei,0,0] 
df.loc[len(df.index)] = [0,'Chemnitz', che,0,0] 

df = df.set_index('Gemeinde')
df = df.iloc[:,1]
#df = df['Neuzugänge letzten 7 Tage']
print(df)

df.to_csv(f'Germany/Sachsen/data/Sachsen_Staedte_for_dw.csv')

# For 14-Day-Map
from datetime import datetime, timedelta
import numpy as np

datum = pd.to_datetime(da)
d = datum - timedelta(days=7)

old = pd.read_csv(f'Germany/Sachsen/data/Sachsen_Staedte_for_rankings_{d.date()}.csv')

old['Gemeinde'] = old['Gemeinde'].str.replace(r', Stadt', '')
old['Gemeinde'] = old['Gemeinde'].str.replace(r', Kurort', '')
old['Gemeinde'] = old['Gemeinde'].str.replace(r', Hochschulstadt', '')
old['Gemeinde'] = old['Gemeinde'].str.replace(r', Universitätsstadt', '')
old['Gemeinde'] = old['Gemeinde'].str.replace(r'a. d.', 'a.d.')
old['Gemeinde'] = old['Gemeinde'].str.replace(r' \(.*', '')
old['Gemeinde'] = old['Gemeinde'].str.replace(r'Verwaltungsgemeinschaft Nünchritz/Glaubitz', 'Glaubitz')
old['Gemeinde'] = old['Gemeinde'].str.replace(r'Verwaltungsgemeinschaft Röderaue/Wülknitz', 'Wülknitz')
old['Gemeinde'] = old['Gemeinde'].str.replace(r'Verwaltungsgemeinschaft Schönfeld/Lampertswalde', 'Lampertswalde')
old = old.append(old.loc[old['Gemeinde'] == 'Glaubitz'], ignore_index = True)
old.at[len(old)-1,'Gemeinde']= 'Nünchritz'
old = old.append(old.loc[old['Gemeinde'] == 'Wülknitz'], ignore_index = True)
old.at[len(old)-1,'Gemeinde']= 'Röderaue'
old = old.append(old.loc[old['Gemeinde'] == 'Lampertswalde'], ignore_index = True)
old.at[len(old)-1,'Gemeinde']= 'Schönfeld'


mdf = df.to_frame().merge(old, on='Gemeinde')
mdf['Neuzugänge letzten 14 Tage'] = mdf['Neuzugänge letzten 7 Tage_x'] + mdf['Neuzugänge letzten 7 Tage_y']
#print(mdf)
mdf = mdf.drop(['Neuzugänge letzten 7 Tage_x', 'Neuzugänge letzten 7 Tage_y'], axis = 1)

mdf.to_csv(f'Germany/Sachsen/data/Sachsen_Staedte_for_dw_14_Tage.csv')


# For Rankings

kfs = df_list[-12]
dre = int(round(kfs.loc[kfs['Unnamed: 0'] == 'Landeshauptstadt Dresden', kfs.columns[1]].item()/10 * 5.5678))
lei = int(round(kfs.loc[kfs['Unnamed: 0'] == 'Stadt Leipzig', kfs.columns[1]].item()/10 * 5.93145))
che = int(round(kfs.loc[kfs['Unnamed: 0'] == 'Stadt Chemnitz', kfs.columns[1]].item()/10 * 2.46334))

df = df_list[-11]
df1 = df_list[-10]
df2 = df_list[-9]
df3 = df_list[-8]
df4 = df_list[-7]
df5 = df_list[-6]
df6 = df_list[-5]
df7 = df_list[-4]
df8 = df_list[-3]
df9 = df_list[-2]

df = df.append(df1)
df = df.append(df2)
df = df.append(df3)
df = df.append(df4)
df = df.append(df5)
df = df.append(df6)
df = df.append(df7)
df = df.append(df8)
df = df.append(df9)


df.loc[len(df.index)] = [0,'Dresden', dre,0,0]
df.loc[len(df.index)] = [0,'Leipzig', lei,0,0] 
df.loc[len(df.index)] = [0,'Chemnitz', che,0,0] 

df = df.set_index('Gemeinde')
df = df.iloc[:,1]
#df = df['Neuzugänge letzten 7 Tage']
print(df)

df.to_csv(f'Germany/Sachsen/data/Sachsen_Staedte_for_rankings_{da}.csv')




old = pd.read_csv(f'Germany/Sachsen/data/Sachsen_Staedte_for_rankings_{d.date()}.csv')
print(old)


mdf = df.to_frame().merge(old, on='Gemeinde')
mdf['Neuzugänge letzten 14 Tage'] = mdf['Neuzugänge letzten 7 Tage_x'] + mdf['Neuzugänge letzten 7 Tage_y']
mdf['Covid-freie Wochen'] = 0
mdf['Covid-freie Wochen'] = np.where(mdf['Neuzugänge letzten 7 Tage_x'] == 0, 1, mdf['Covid-freie Wochen'])
mdf['Covid-freie Wochen'] = np.where(mdf['Neuzugänge letzten 14 Tage'] == 0 , 2, mdf['Covid-freie Wochen'])
mdf = mdf[['Gemeinde','Covid-freie Wochen','Neuzugänge letzten 14 Tage','Neuzugänge letzten 7 Tage_x','Neuzugänge letzten 7 Tage_y']]
print(mdf)

cols=['Gemeinde','Covid-freie Wochen','Neuzugänge letzten 14 Tage','Neuzugänge letzten 7 Tage_x','Neuzugänge letzten 7 Tage_y']
thr = pd.DataFrame(mdf, columns=cols)
fin = thr.sort_values(['Covid-freie Wochen'], ascending=[False])
fin['week'] = fin['Covid-freie Wochen'].gt(13) 
tab = fin.sort_values(['week'], ascending=[False])
tab_t = tab[tab['week']==True]
tab_f = tab[tab['week']==False]
tab_f = tab_f.sort_values(['Neuzugänge letzten 14 Tage','Covid-freie Wochen'], ascending = [True,False])
tab_t = tab_t.sort_values(['Covid-freie Wochen','Neuzugänge letzten 14 Tage'], ascending = [False,True])
tab = tab_t.append(tab_f)
tab = tab.drop(['week'], axis=1)

#Percent Change

tab['PercentChange'] = 100*(tab['Neuzugänge letzten 7 Tage_x'] - tab['Neuzugänge letzten 7 Tage_y'])/(tab['Neuzugänge letzten 7 Tage_x']+tab['Neuzugänge letzten 7 Tage_y'])
tab['PercentChange'] = tab['PercentChange'].fillna(0.0)

tab = tab.drop(['Neuzugänge letzten 7 Tage_y'], axis = 1)
#tab.columns = ['Gemeinde', 'Covid-freie Wochen', 'Neue Fälle letzte 14 Tage', 'Letzte 7 Tage', 'Pct Change']

def highlighter(s):
    #val_1 = s['Covid-freie Wochen']
    val_2 = s['Neue Fälle letzte 14 Tage']
    
    r=''
    try:
        if 0==val_2: #More than 2 Covid free weeks
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


tab = tab[['Platz', 'Stadt/Gemeinde', 'Covid-freie Wochen', 'Neue Fälle letzte 14 Tage','Letzte 7 Tage','Trend']]
tab = tab.drop('Covid-freie Wochen', axis = 1)
s = tab.style.apply(highlighter, axis = 1).set_table_styles(styles).hide_index()


try:        
    with open(f'Sachsen.html', 'w', encoding="utf-8") as out:
        body = s.render().replace('&#x2197;','<span style="color: red"> &#x2197;</span>') # red arrow up
        body = body.replace('&#x2198','<span style="color: green"> &#x2198;</span>') # green arrow down
        content = top + body + bottom
        out.write(content)
except Exception as e:
    print(f'Error:\n{e}')
