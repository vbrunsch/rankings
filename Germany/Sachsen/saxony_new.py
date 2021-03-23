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
jsp = pd.read_json('https://www.coronavirus.sachsen.de/corona-statistics/rest/infectionOverview.jsp')
dres = jsp[jsp.columns[0]].to_frame()
leip = jsp[jsp.columns[1]].to_frame()
chem = jsp[jsp.columns[2]].to_frame()

dre = int(round(dres.at['incidence',dres.columns[0]] * 5.5678))
lei = int(round(leip.at['incidence',leip.columns[0]] * 5.93145))
che = int(round(chem.at['incidence',chem.columns[0]] * 2.46334))

df = df_list[-11]
df['Landkreis'] = 'Bautzen'
df1 = df_list[-10]
df1['Landkreis'] = 'Erzgebirgskreis'
df2 = df_list[-9]
df2['Landkreis'] = 'Görlitz'
df3 = df_list[-8]
df3['Landkreis'] = 'Leipzig'
df4 = df_list[-7]
df4['Landkreis'] = 'Meißen'
df5 = df_list[-6]
df5['Landkreis'] = 'Mittelsachsen'
df6 = df_list[-5]
df6['Landkreis'] = 'Nordsachsen'
df7 = df_list[-4]
df7['Landkreis'] = 'Sächsische Schweiz-Osterzgebirge'
df8 = df_list[-3]
df8['Landkreis'] = 'Vogtlandkreis'
df9 = df_list[-2]
df9['Landkreis'] = 'Zwickau'

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
df.loc[len(df.index)] = [0,'Dresden', dre,556780,0,'Landeshauptstadt Dresden']
df.loc[len(df.index)] = [0,'Leipzig', lei,593145,0,'Stadt Leipzig'] 
df.loc[len(df.index)] = [0,'Chemnitz', che,246334,0,'Stadt Chemnitz'] 

df = df.set_index('Gemeinde')
#df = df.iloc[:,1]
#df = df['Neuzugänge letzten 7 Tage']
print(df)

df.to_csv(f'Germany/Sachsen/data/Sachsen_Staedte_for_dw_neu.csv')

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


mdf = df.merge(old, on='Gemeinde')
mdf['Neuzugänge letzten 7 Tage_x'] = mdf['Neuzugänge letzten 7 Tage_x'].astype(int)
mdf['Neuzugänge letzten 7 Tage_y'] = mdf['Neuzugänge letzten 7 Tage_y'].astype(int)
mdf['Neuzugänge letzten 14 Tage'] = mdf['Neuzugänge letzten 7 Tage_x'] + mdf['Neuzugänge letzten 7 Tage_y']

# Map for Görlitz only
goe_only = mdf[mdf['Landkreis']=='Görlitz']
goe_only['Neuzugänge letzten 7 Tage'] = goe_only['Neuzugänge letzten 7 Tage_x']
goe_only['Neuzugänge letzten 7 Tage_x'] = np.where(goe_only['Neuzugänge letzten 7 Tage_x'] == 0, 0.6, goe_only['Neuzugänge letzten 7 Tage_x'])
goe_only['Neuzugänge letzten 7 Tage_x'] = np.where(goe_only['Neuzugänge letzten 14 Tage'] == 0, 0.2, goe_only['Neuzugänge letzten 7 Tage_x'])
goe_only['Neuzugänge letzten 7 Tage_x'] = goe_only['Neuzugänge letzten 7 Tage_x']*10
goe_only.to_csv(f'Germany/Sachsen/data/Sachsen_Görlitz_for_dw_14_Tage_neu.csv')

# Map for Mittelsachsen only
mit_only = mdf[mdf['Landkreis']=='Mittelsachsen']
mit_only['Neuzugänge letzten 7 Tage'] = mit_only['Neuzugänge letzten 7 Tage_x']
mit_only['Neuzugänge letzten 7 Tage_x'] = np.where(mit_only['Neuzugänge letzten 7 Tage_x'] == 0, 0.6, mit_only['Neuzugänge letzten 7 Tage_x'])
mit_only['Neuzugänge letzten 7 Tage_x'] = np.where(mit_only['Neuzugänge letzten 14 Tage'] == 0, 0.2, mit_only['Neuzugänge letzten 7 Tage_x'])
mit_only['Neuzugänge letzten 7 Tage_x'] = mit_only['Neuzugänge letzten 7 Tage_x']*10
mit_only.to_csv(f'Germany/Sachsen/data/Sachsen_Mittelsachsen_for_dw_14_Tage_neu.csv')



mdf['Neuzugänge letzten 7 Tage_x'] = np.where(mdf['Neuzugänge letzten 7 Tage_x'] == 0, 0.6, mdf['Neuzugänge letzten 7 Tage_x'])
mdf['Neuzugänge letzten 7 Tage_x'] = np.where(mdf['Neuzugänge letzten 14 Tage'] == 0, 0.2, mdf['Neuzugänge letzten 7 Tage_x'])
mdf['Neuzugänge letzten 7 Tage_x'] = mdf['Neuzugänge letzten 7 Tage_x']*10
#print(mdf)
#mdf = mdf.drop(['Neuzugänge letzten 7 Tage_x', 'Neuzugänge letzten 7 Tage_y'], axis = 1)

mdf.to_csv(f'Germany/Sachsen/data/Sachsen_Staedte_for_dw_14_Tage_neu.csv')




# For Rankings
jsp = pd.read_json('https://www.coronavirus.sachsen.de/corona-statistics/rest/infectionOverview.jsp')
dres = jsp[jsp.columns[0]].to_frame()
leip = jsp[jsp.columns[1]].to_frame()
chem = jsp[jsp.columns[2]].to_frame()

dre = int(round(dres.at['incidence',dres.columns[0]] * 5.5678))
lei = int(round(leip.at['incidence',leip.columns[0]] * 5.93145))
che = int(round(chem.at['incidence',chem.columns[0]] * 2.46334))


df_list = pd.read_html(html)

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
mdf['Neuzugänge letzten 7 Tage_x'] = mdf['Neuzugänge letzten 7 Tage_x'].astype(int)
mdf['Neuzugänge letzten 7 Tage_y'] = mdf['Neuzugänge letzten 7 Tage_y'].astype(int)
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
tab_f = tab_f.sort_values(['Neuzugänge letzten 7 Tage_x','Neuzugänge letzten 14 Tage'], ascending = [True,True])
tab_t = tab_t.sort_values(['Covid-freie Wochen','Neuzugänge letzten 7 Tage_x'], ascending = [False,True])
tab = tab_t.append(tab_f)
tab = tab.drop(['week'], axis=1)

#Percent Change

tab['PercentChange'] = 100*(tab['Neuzugänge letzten 7 Tage_x'] - tab['Neuzugänge letzten 7 Tage_y'])/(tab['Neuzugänge letzten 7 Tage_x']+tab['Neuzugänge letzten 7 Tage_y'])
tab['PercentChange'] = tab['PercentChange'].fillna(0.0)

tab = tab.drop(['Neuzugänge letzten 7 Tage_y'], axis = 1)
#tab.columns = ['Gemeinde', 'Covid-freie Wochen', 'Neue Fälle letzte 14 Tage', 'Letzte 7 Tage', 'Pct Change']

tab.to_pickle("visualizations/pickles/saxony.pkl")

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
    with open(f'Sachsen_neu.html', 'w', encoding="utf-8") as out:
        body = s.render().replace('&#x2197;','<span style="color: red"> &#x2197;</span>') # red arrow up
        body = body.replace('&#x2198','<span style="color: green"> &#x2198;</span>') # green arrow down
        content = top + toti + body + bottom
        out.write(content)
except Exception as e:
    print(f'Error:\n{e}')

    
# Goerlitz Tabelle
goe_gems = df2['Gemeinde'].unique()
goe_tab = tab[tab['Stadt/Gemeinde'].isin(goe_gems)]
goe_s = goe_tab.style.apply(highlighter, axis = 1).set_table_styles(styles).hide_index()

try:        
    with open(f'Görlitz_neu.html', 'w', encoding="utf-8") as out:
        body = goe_s.render().replace('&#x2197;','<span style="color: red"> &#x2197;</span>') # red arrow up
        body = body.replace('&#x2198','<span style="color: green"> &#x2198;</span>') # green arrow down
        content = top + toti + body + bottom
        out.write(content)
except Exception as e:
    print(f'Error:\n{e}')
    
# Mittelsachsen Tabelle
mit_gems = df5['Gemeinde'].unique()
mit_tab = tab[tab['Stadt/Gemeinde'].isin(mit_gems)]
mit_s = mit_tab.style.apply(highlighter, axis = 1).set_table_styles(styles).hide_index()

try:        
    with open(f'Mittelsachsen_neu.html', 'w', encoding="utf-8") as out:
        body = mit_s.render().replace('&#x2197;','<span style="color: red"> &#x2197;</span>') # red arrow up
        body = body.replace('&#x2198','<span style="color: green"> &#x2198;</span>') # green arrow down
        content = top + toti + body + bottom
        out.write(content)
except Exception as e:
    print(f'Error:\n{e}')
