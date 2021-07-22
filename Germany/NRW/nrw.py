import pandas as pd
import numpy as np

zus = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Aachen/data/Aachen_for_dw14_7.csv', index_col= 0)
df_Bor = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Borken/data/Borken_for_dw14_7.csv', index_col= 0)
df_Coe = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Coesfeld/data/Coesfeld_for_dw14_7.csv', index_col= 0)
df_Due = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Dueren/data/Dueren_for_dw14_7.csv', index_col= 0)
df_Erk = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/ERK/data/ERK_for_dw14_7.csv', index_col= 0)
df_Gue = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Guetersloh/data/Guetersloh_for_dw14_7.csv', index_col= 0)
#df_Hei = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Heinsberg/data/Heinsberg_for_dw14_7.csv', index_col= 0)
df_Hoe = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Hoexter/data/H%C3%B6xter_for_dw14_7.csv',index_col= 0)
df_Kle = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Kleve/data/Kleve_for_dw14_7.csv', index_col= 0)
df_Lip = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Lippe/data/Lippe_for_dw14_7.csv', index_col= 0)
df_MK = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/MK/data/M%C3%A4rkischer_Kreis_for_dw14_7.csv', index_col= 0)
df_Met = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Mettmann/data/Mettmann_for_dw14_7.csv', index_col= 0)
df_Min = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Minden-Luebbecke/data/Minden-Luebbecke_for_dw14_7.csv', index_col= 0)
df_Olp = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Olpe/data/Olpe_for_dw14_7.csv', index_col= 0)
df_Pad = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Paderborn/data/Paderborn_for_dw14_7.csv', index_col= 0)
df_REK = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/REK/data/Rhein-Erft-Kreis_for_dw14_7.csv', index_col= 0)
df_RSK = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/RSK/data/Rhein-Sieg-Kreis_for_dw14_7.csv', index_col= 0)

df_SKs = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/SKs/data/SKs_for_dw14_7.csv', index_col= 0)
df_SKs = df_SKs.loc[['Bielefeld','Münster','Hamm','Mülheim a.d.Ruhr','Dortmund','Hagen','Bochum','Herne','Gelsenkirchen','Essen','Bottrop','Oberhausen','Duisburg','Krefeld','Düsseldorf','Mönchengladbach','Wuppertal','Solingen','Remscheid','Bonn','Leverkusen','Köln']]

df_Ste = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Steinfurt/data/Steinfurt_for_dw14_7.csv', index_col= 0)
df_War = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Warendorf/data/Warendorf_for_dw14_7.csv', index_col= 0)
df_Wes = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Wesel/data/Wesel_for_dw14_7.csv', index_col= 0)
df_RKN = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/RKN/data/Rhein-Kreis-Neuss_for_dw14_7.csv', index_col= 0)

df_Rec = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Recklinghausen/data/Recklinghausen_for_dw14_7.csv', index_col= 0)
df_Rec.index.name = None
df_Rec.columns = ['last7','last14','mix','Gemeinde']

df_RBK = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/RBK/data/Rheinisch-Bergischer-Kreis_for_dw14_7.csv', index_col= 0)
df_Vie = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Viersen/data/Viersen_for_dw14_7.csv', index_col= 0)
df_SW = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/SW/data/Siegen-Wittgenstein_for_dw14_7.csv', index_col= 0)
df_Soe = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Soest/data/Soest_for_dw14_7.csv', index_col= 0)
df_Unn = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Unna/data/Unna_for_dw14_7.csv', index_col= 0)
df_Hoc = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Hochsauerlandkreis/data/Hochsauerlandkreis_for_dw14_7.csv', index_col= 0)

zus = zus.append(df_Bor)
zus = zus.append(df_Coe)
zus = zus.append(df_Due)
zus = zus.append(df_Erk)
zus = zus.append(df_Gue)
#zus = zus.append(df_Hei)
zus = zus.append(df_Hoe)
zus = zus.append(df_Kle)
zus = zus.append(df_Lip)
zus = zus.append(df_MK)
zus = zus.append(df_Met)
zus = zus.append(df_Min)
zus = zus.append(df_Olp)
zus = zus.append(df_Pad)
zus = zus.append(df_REK)
zus = zus.append(df_RSK)
zus = zus.append(df_SKs)
zus = zus.append(df_Ste)
zus = zus.append(df_War)
zus = zus.append(df_Wes)
zus = zus.append(df_RKN)
zus = zus.append(df_Rec)
zus = zus.append(df_RBK)
zus = zus.append(df_Vie)
zus = zus.append(df_SW)
zus = zus.append(df_Soe)
zus = zus.append(df_Unn)
zus = zus.append(df_Hoc)

zus = zus.replace('Mülheim a.d.Ruhr','Mülheim an der Ruhr')
zus = zus.set_index('Gemeinde')
zus.index.name = None
zus['Gemeinde'] = zus.index
zus = zus.drop('GESAMT')
zus = zus.drop('Gesamt')
zus = zus.drop('Kreis gesamt')
zus = zus.drop('Kreis Borken')
zus = zus.drop('abweichender Meldeort')
zus = zus.drop('Kreis Coesfeld')
zus = zus.drop('Kreis Mettmann')
zus = zus.drop('Städteregion')
print(zus)
zus.to_csv(f'Germany/NRW/SKs/data/NRW_Gem_for_dw14_7.csv') 


# For Rankings
mdf = zus.copy()
mdf = mdf.drop_duplicates()
mdf['Neuzugänge letzten 7 Tage_x'] = mdf['last7'].astype(int)
mdf['Neuzugänge letzten 14 Tage'] = mdf['last14'].astype(int)
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
    with open(f'NRW.html', 'w', encoding="utf-8") as out:
        body = s.render().replace('&#x2197;','<span style="color: red"> &#x2197;</span>') # red arrow up
        body = body.replace('&#x2198','<span style="color: green"> &#x2198;</span>') # green arrow down
        content = top + toti + body + bottom
        out.write(content)
except Exception as e:
    print(f'Error:\n{e}')
