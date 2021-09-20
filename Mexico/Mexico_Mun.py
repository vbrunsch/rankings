#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
print('a')
df_o = pd.read_csv('http://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/datos_abiertos_covid19.zip', encoding = "ISO-8859-1")
print('b')
df = df_o[df_o['RESULTADO_LAB']==1]
df = df[df['ENTIDAD_RES']<33]
df = df[['FECHA_INGRESO','ENTIDAD_RES','MUNICIPIO_RES']]

cat_states = pd.read_csv('Mexico/Mexico_Cat_States.csv')
cat_muns = pd.read_csv('Mexico/Mexico_Cat_Municipalities.csv')
cat_muns = cat_muns[cat_muns['CLAVE_MUNICIPIO']<996]

get_st_names = pd.Series(cat_states['ENTIDAD_FEDERATIVA'].values,index=cat_states['CLAVE_ENTIDAD']).to_dict()
get_st_ab_names = pd.Series(cat_states['ABREVIATURA'].values,index=cat_states['CLAVE_ENTIDAD']).to_dict()
get_mu_names = pd.Series(cat_muns['MUNICIPIO'].values,index=[cat_muns['CLAVE_ENTIDAD'],cat_muns['CLAVE_MUNICIPIO']]).to_dict()

cat_muns['Sta_Ab'] = cat_muns['CLAVE_ENTIDAD'].map(get_st_ab_names)
cat_muns['Mun_Sta'] = cat_muns['MUNICIPIO'] + ', (' + cat_muns['Sta_Ab'] + ')'
cat_mu_lis = cat_muns['Mun_Sta'].unique()

df['Sta'] = df['ENTIDAD_RES'].map(get_st_names)
df['Sta_Ab'] = df['ENTIDAD_RES'].map(get_st_ab_names)
df['Code_Mu'] = df[['ENTIDAD_RES', 'MUNICIPIO_RES']].apply(tuple, axis=1)
df['Mun'] = df['Code_Mu'].map(get_mu_names)
df['Mun_Sta'] = df['Mun'] + ', (' + df['Sta_Ab'] + ')'

mu = df.copy().drop(['ENTIDAD_RES','MUNICIPIO_RES','Sta', 'Sta_Ab', 'Code_Mu', 'Mun'], axis = 1)
mu_lis = mu['Mun_Sta'].unique()
mu_lis = [x for x in mu_lis if not pd.isnull(x)]

tod = pd.to_datetime('today')
idx = pd.date_range('02-27-2020', tod)

cols=['Municipalities','COVID-Free Days','New Cases in Last 14 Days', 'Last7', 'Previous7']
collect = []

for d in mu_lis:
    focus = mu[mu['Mun_Sta'] == d]
    focus = focus.drop(['Mun_Sta'], axis = 1)
    focus['New'] = 1
    focus = focus.groupby(['FECHA_INGRESO']).sum()
    focus.index = pd.to_datetime(focus.index, dayfirst=True)
    focus = focus.reindex(idx, fill_value=0)
    ave = focus[:-2]
    las = len(ave)-14
    last_forteen = int(ave[las:].sum().item())
    if last_forteen < 0:
        last_forteen = 0
    last7 = int(ave[len(ave)-7:].sum().item()) #last week
    prev7 = int(ave[len(ave)-14:len(ave)-7].sum().item()) #prev week
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
    while i > 0:
        if ave.values[i] <= 0:
            c = c + 1
        else:
            i = 0
        i = i - 1

    collect.append((d,
                   c,
                   last_forteen,
                   last7,
                   prev7))


    
zer = list(set(cat_mu_lis) - set(mu_lis))
for d in zer:
    collect.append((d,
                   len(idx),
                   0,
                   0,
                   0))
    

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
tab.columns = ['Municipalities', 'COVID-Free Days', 'New Cases in Last 14 Days', 'Last 7 Days', 'Pct Change']

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

tab = tab[['Rank', 'Municipalities', 'COVID-Free Days', 'New Cases in Last 14 Days','Last 7 Days','Percent Change']]       
s = tab.style.apply(highlighter, axis = 1).set_table_styles(styles).hide_index()

try:        
    with open(f'Mexico_Municipalities.html', 'w', encoding="utf-8") as out:
        body = s.render().replace('&#x2197;','<span style="color: red"> &#x2197;</span>') # red arrow up
        body = body.replace('&#x2198','<span style="color: green"> &#x2198;</span>') # green arrow down
        content = top + body + bottom
        out.write(content)
except Exception as e:
    print(f'Error:\n{e}')
    print(focus)
