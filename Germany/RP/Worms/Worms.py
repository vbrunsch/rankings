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


import re

from datetime import timedelta

neu = pd.DataFrame()
unb = pd.DataFrame()
rei = pd.DataFrame()
kon = pd.DataFrame()
zus = pd.DataFrame()
we = 0

for x in range(0,14): # CHANGE HERE
    x = x + we*2
    m = 0
    tod = pd.Timestamp.today() -timedelta(days=x)
    tod = tod.strftime('%d.%m.%Y')
    while m == 0 and x < 14: # CHANGE HERE
        for url in ['https://www.kreis-alzey-worms.eu/verwaltung/aktuelles/','https://www.kreis-alzey-worms.eu/verwaltung/aktuelles/?pageId586a9b2b=2#list_586a9b2b','https://www.kreis-alzey-worms.eu/verwaltung/aktuelles/?pageId586a9b2b=3#list_586a9b2b','https://www.kreis-alzey-worms.eu/verwaltung/aktuelles/?pageId586a9b2b=4#list_586a9b2b','https://www.kreis-alzey-worms.eu/verwaltung/aktuelles/?pageId586a9b2b=5#list_586a9b2b','https://www.kreis-alzey-worms.eu/verwaltung/aktuelles/?pageId586a9b2b=6#list_586a9b2b']:
            if tod == '27.04.2021':
              m = m + 1
              neu[tod] = 0
              unb[tod] = 0
              #rei[tod] = 0
              kon[tod] = 0

            print(url)
            html = urllib.request.urlopen(url)
            htmlParse = BeautifulSoup(html, 'html.parser')
            for para in htmlParse.find_all("li"): 
                t = para.get_text()
                #print(t)
                matches = re.findall(tod, t)
                if matches:
                    if re.findall('Corona\-?: Heute',t) or re.findall('Corona\-?: heute',t) or re.findall('Corona: Seit',t):
                        m = m + 1
                        print(matches[0])
                        try:
                          lin = re.findall('href="(.*)">Corona', str(para))
                          link = 'https://www.kreis-alzey-worms.eu/'+ lin[0]
                        except:
                          lin = re.findall('href="(.*)"> Corona', str(para))
                          link = 'https://www.kreis-alzey-worms.eu/'+ lin[0]
                        df = pd.read_html(link, encoding = 'utf-8')
                        try:
                          if tod in ['16.09.2021']:
                            df = df[4]
                            #df = df.drop([df.columns[1],df.columns[2]], axis=1)
                            df = df.drop([0, 2])
                            #df = df[:-1]
                          elif tod in ['02.08.2021']:
                            df = df[3]
                            new_row = {'Unnamed: 0':'Stadt Worms', 'Neue Fälle':7, 'Unbekannter Infektionsherd':7, 'Einreisende / Reiserückkehrer':0, 'Kontakt zu positiv getesteter Person':0}
                            df = df.append(new_row, ignore_index = True)
                            df = df.reindex([7,0,1,2,3,4,5,6])
                          elif tod in ['14.09.2021']:
                            df = pd.read_csv('Germany/RP/Worms/data/worms_null.csv')
                          else:
                            df = df[3]
                            df = df.drop([0, 2])
                          print('neu')
                          print(df)
                        except:
                          try:
                            df = df[0]
                            df = df.drop(['Reiserückkehrer'], axis=1)
                            print('alt')
                            print(df)
                          except:
                            df = pd.read_csv('Germany/RP/Worms/data/worms_null.csv')
                            #df = df.set_index(df.columns[1])
                            print('null')
                            print(df)

                        df = df.replace('-', 0)
                        index_names = df[ df['Unnamed: 0'] == 'Ohne festen Wohnsitz im Landkreis' ].index
                        df.drop(index_names, inplace = True)
                        df[df.columns[1]] = df[df.columns[1]].astype(int)
                        df[df.columns[2]] = df[df.columns[2]].astype(int)
                        df[df.columns[3]] = df[df.columns[3]].astype(int)
                        #df[df.columns[4]] = df[df.columns[4]].astype(int)
                        df['AGS'] = ['07319000','07331003','07331001','07331002','07331023','07331017','07331004','07331006']

                        #Vg Alzey-Land
                        df = df.append(df.loc[df['AGS'] == '07331001'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331005'
                        df = df.append(df.loc[df['AGS'] == '07331001'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331007'
                        df = df.append(df.loc[df['AGS'] == '07331001'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331008'
                        df = df.append(df.loc[df['AGS'] == '07331001'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331010'
                        df = df.append(df.loc[df['AGS'] == '07331001'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331012'
                        df = df.append(df.loc[df['AGS'] == '07331001'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331014'
                        df = df.append(df.loc[df['AGS'] == '07331001'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331020'
                        df = df.append(df.loc[df['AGS'] == '07331001'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331021'
                        df = df.append(df.loc[df['AGS'] == '07331001'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331022'
                        df = df.append(df.loc[df['AGS'] == '07331001'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331024'
                        df = df.append(df.loc[df['AGS'] == '07331001'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331025'
                        df = df.append(df.loc[df['AGS'] == '07331001'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331026'
                        df = df.append(df.loc[df['AGS'] == '07331001'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331027'
                        df = df.append(df.loc[df['AGS'] == '07331001'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331031'
                        df = df.append(df.loc[df['AGS'] == '07331001'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331032'
                        df = df.append(df.loc[df['AGS'] == '07331001'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331042'
                        df = df.append(df.loc[df['AGS'] == '07331001'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331043'
                        df = df.append(df.loc[df['AGS'] == '07331001'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331044'
                        df = df.append(df.loc[df['AGS'] == '07331001'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331050'
                        df = df.append(df.loc[df['AGS'] == '07331001'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331051'
                        df = df.append(df.loc[df['AGS'] == '07331001'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331052'
                        df = df.append(df.loc[df['AGS'] == '07331001'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331053'
                        df = df.append(df.loc[df['AGS'] == '07331001'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331067'

                        #Vg Eich
                        df = df.append(df.loc[df['AGS'] == '07331002'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331018'
                        df = df.append(df.loc[df['AGS'] == '07331002'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331034'
                        df = df.append(df.loc[df['AGS'] == '07331002'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331038'
                        df = df.append(df.loc[df['AGS'] == '07331002'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331045'

                        #Vg Monsheim
                        df = df.append(df.loc[df['AGS'] == '07331023'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331041'
                        df = df.append(df.loc[df['AGS'] == '07331023'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331046'
                        df = df.append(df.loc[df['AGS'] == '07331023'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331048'
                        df = df.append(df.loc[df['AGS'] == '07331023'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331047'
                        df = df.append(df.loc[df['AGS'] == '07331023'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331054'
                        df = df.append(df.loc[df['AGS'] == '07331023'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331066'

                        #Vg Woellstein
                        df = df.append(df.loc[df['AGS'] == '07331017'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331030'
                        df = df.append(df.loc[df['AGS'] == '07331017'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331035'
                        df = df.append(df.loc[df['AGS'] == '07331017'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331060'
                        df = df.append(df.loc[df['AGS'] == '07331017'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331062'
                        df = df.append(df.loc[df['AGS'] == '07331017'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331070'
                        df = df.append(df.loc[df['AGS'] == '07331017'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331072'
                        df = df.append(df.loc[df['AGS'] == '07331017'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331075'

                        #Vg Woerrstadt
                        df = df.append(df.loc[df['AGS'] == '07331004'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331019'
                        df = df.append(df.loc[df['AGS'] == '07331004'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331029'
                        df = df.append(df.loc[df['AGS'] == '07331004'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331033'
                        df = df.append(df.loc[df['AGS'] == '07331004'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331056'
                        df = df.append(df.loc[df['AGS'] == '07331004'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331058'
                        df = df.append(df.loc[df['AGS'] == '07331004'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331059'
                        df = df.append(df.loc[df['AGS'] == '07331004'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331061'
                        df = df.append(df.loc[df['AGS'] == '07331004'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331063'
                        df = df.append(df.loc[df['AGS'] == '07331004'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331064'
                        df = df.append(df.loc[df['AGS'] == '07331004'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331065'
                        df = df.append(df.loc[df['AGS'] == '07331004'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331068'
                        df = df.append(df.loc[df['AGS'] == '07331004'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331073'

                        #Vg Wonnegau
                        df = df.append(df.loc[df['AGS'] == '07331006'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331009'
                        df = df.append(df.loc[df['AGS'] == '07331006'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331015'
                        df = df.append(df.loc[df['AGS'] == '07331006'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331028'
                        df = df.append(df.loc[df['AGS'] == '07331006'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331036'
                        df = df.append(df.loc[df['AGS'] == '07331006'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331037'
                        df = df.append(df.loc[df['AGS'] == '07331006'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331039'
                        df = df.append(df.loc[df['AGS'] == '07331006'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331011'
                        df = df.append(df.loc[df['AGS'] == '07331006'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331049'
                        df = df.append(df.loc[df['AGS'] == '07331006'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331055'
                        df = df.append(df.loc[df['AGS'] == '07331006'], ignore_index = True)
                        df.at[len(df)-1,'AGS']= '07331071'


                        df = df.set_index('AGS')
                        cop = df.copy()

                        if neu.empty:    
                            neu = pd.DataFrame(index = df.index)
                            unb = pd.DataFrame(index = df.index)
                            #rei = pd.DataFrame(index = df.index)
                            kon = pd.DataFrame(index = df.index)
                            zus = pd.DataFrame(index = df.index)

                        try:
                            neu[tod] = cop[['Neue Fälle']]
                        except:
                            try:
                              neu[tod] = cop[['neue Fälle']]
                            except:
                              a = ''
                              for i in cop.columns:
                                a = a + ',' + i
                              b = re.findall(',(Neue F.*?),',a)
                              neu[tod] = cop[[b[0]]]

                        try:
                          unb[tod] = cop[['unbekannter Infektionsherd']]
                        except:
                          unb[tod] = 0
                          
                        #rei[tod] = cop[['Reiserückkehrer']]
                        try:
                          kon[tod] = cop[['Kontakt zu positiv getesteter Person']]
                        except:
                          kon[tod] = 0
                        
                        if re.findall('Corona: Seit',t):
                            we = we + 1
                            tod = pd.Timestamp.today() -timedelta(days=x+1)
                            tod = tod.strftime('%d.%m.%Y')
                            neu[tod] = 0
                            unb[tod] = 0
                            #rei[tod] = 0
                            kon[tod] = 0
                            tod = pd.Timestamp.today() -timedelta(days=x+2)
                            tod = tod.strftime('%d.%m.%Y')
                            neu[tod] = 0
                            unb[tod] = 0
                            #rei[tod] = 0
                            kon[tod] = 0
                        
                        
import numpy as np

neu.to_csv(f'Germany/RP/Worms/data/Worms_current.csv')

zus['last7'] = neu[neu.columns[0]]+neu[neu.columns[1]]+neu[neu.columns[2]]+neu[neu.columns[3]]+neu[neu.columns[4]]+neu[neu.columns[5]]+neu[neu.columns[6]]
zus['last14'] = zus['last7'] + neu[neu.columns[7]]+neu[neu.columns[8]]+neu[neu.columns[9]]+neu[neu.columns[10]]+neu[neu.columns[11]]+neu[neu.columns[12]]+neu[neu.columns[13]]
zus['mix'] = np.where(zus['last7'] == 0, 0.6, zus['last7'])
zus['mix'] = np.where(zus['last14'] == 0, 0.2, zus['mix'])

zus['last7_risk'] = unb[unb.columns[0]]+unb[unb.columns[1]]+unb[unb.columns[2]]+unb[unb.columns[3]]+unb[unb.columns[4]]+unb[unb.columns[5]]+unb[unb.columns[6]]
zus['last14_risk'] = zus['last7_risk'] + unb[unb.columns[7]]+unb[unb.columns[8]]+unb[unb.columns[9]]+unb[unb.columns[10]]+unb[unb.columns[11]]+unb[unb.columns[12]]+unb[unb.columns[13]]
zus['mix_risk'] = np.where(zus['last7_risk'] == 0, 0.6, zus['last7_risk'])
zus['mix_risk'] = np.where(zus['last14_risk'] == 0, 0.2, zus['mix_risk'])

zus['Gemeinde'] = cop[['Unnamed: 0']]
zus.to_csv(f'Germany/RP/Worms/data/Worms_for_dw14_7.csv')
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
    with open(f'Worms.html', 'w', encoding="utf-8") as out:
        body = s.render().replace('&#x2197;','<span style="color: red"> &#x2197;</span>') # red arrow up
        body = body.replace('&#x2198','<span style="color: green"> &#x2198;</span>') # green arrow down
        content = top + toti + body + bottom
        out.write(content)
except Exception as e:
    print(f'Error:\n{e}')
