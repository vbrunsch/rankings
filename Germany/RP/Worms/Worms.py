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

for x in range(0,13):
    x = x + we*2
    m = 0
    tod = pd.Timestamp.today() -timedelta(days=x)
    tod = tod.strftime('%d.%m.%Y')
    while m == 0 and x < 14:
        for url in ['https://www.kreis-alzey-worms.eu/verwaltung/aktuelles/','https://www.kreis-alzey-worms.eu/verwaltung/aktuelles/?pageId586a9b2b=2#list_586a9b2b','https://www.kreis-alzey-worms.eu/verwaltung/aktuelles/?pageId586a9b2b=3#list_586a9b2b','https://www.kreis-alzey-worms.eu/verwaltung/aktuelles/?pageId586a9b2b=4#list_586a9b2b','https://www.kreis-alzey-worms.eu/verwaltung/aktuelles/?pageId586a9b2b=5#list_586a9b2b','https://www.kreis-alzey-worms.eu/verwaltung/aktuelles/?pageId586a9b2b=6#list_586a9b2b']:
            html = urllib.request.urlopen(url)
            htmlParse = BeautifulSoup(html, 'html.parser')
            for para in htmlParse.find_all("li"): 
                t = para.get_text()
                #print(t)
                matches = re.findall(tod, t)
                if matches:
                    if re.findall('Corona: Heute',t) or re.findall('Corona: Seit',t):
                        m = m + 1
                        print(matches[0])
                        lin = re.findall('href="(.*)">Corona', str(para))
                        link = 'https://www.kreis-alzey-worms.eu/'+ lin[0]
                        df = pd.read_html(link)
                        df = df[0]
                        df = df.replace('-', 0)
                        df[df.columns[1]] = df[df.columns[1]].astype(int)
                        df[df.columns[2]] = df[df.columns[2]].astype(int)
                        df[df.columns[3]] = df[df.columns[3]].astype(int)
                        df[df.columns[4]] = df[df.columns[4]].astype(int)
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
                            rei = pd.DataFrame(index = df.index)
                            kon = pd.DataFrame(index = df.index)
                            zus = pd.DataFrame(index = df.index)

                        neu[tod] = cop[['Neue FÃ¤lle']]
                        unb[tod] = cop[['unbekannter Infektionsherd']]
                        rei[tod] = cop[['ReiserÃ¼ckkehrer']]
                        kon[tod] = cop[['Kontakt zu positiv getesteter Person']]
                        
                        if re.findall('Corona: Seit',t):
                            we = we + 1
                            tod = pd.Timestamp.today() -timedelta(days=x+1)
                            tod = tod.strftime('%d.%m.%Y')
                            neu[tod] = 0
                            unb[tod] = 0
                            rei[tod] = 0
                            kon[tod] = 0
                            tod = pd.Timestamp.today() -timedelta(days=x+2)
                            tod = tod.strftime('%d.%m.%Y')
                            neu[tod] = 0
                            unb[tod] = 0
                            rei[tod] = 0
                            kon[tod] = 0
import numpy as np


zus['last7'] = neu[neu.columns[0]]+neu[neu.columns[1]]+neu[neu.columns[2]]+neu[neu.columns[3]]+neu[neu.columns[4]]+neu[neu.columns[5]]+neu[neu.columns[6]]
zus['last14'] = zus['last7'] + neu[neu.columns[7]]+neu[neu.columns[8]]+neu[neu.columns[9]]+neu[neu.columns[10]]+neu[neu.columns[11]]+neu[neu.columns[12]]+neu[neu.columns[13]]
zus['mix'] = np.where(zus['last7'] == 0, 0.6, zus['last7'])
zus['mix'] = np.where(zus['last14'] == 0, 0.2, zus['mix'])

zus['last7_risk'] = unb[unb.columns[0]]+unb[unb.columns[1]]+unb[unb.columns[2]]+unb[unb.columns[3]]+unb[unb.columns[4]]+unb[unb.columns[5]]+unb[unb.columns[6]]
zus['last14_risk'] = zus['last7'] + unb[unb.columns[7]]+unb[unb.columns[8]]+unb[unb.columns[9]]+unb[unb.columns[10]]+unb[unb.columns[11]]+unb[unb.columns[12]]+unb[unb.columns[13]]
zus['mix_risk'] = np.where(zus['last7_risk'] == 0, 0.6, zus['last7_risk'])
zus['mix_risk'] = np.where(zus['last14_risk'] == 0, 0.2, zus['mix_risk'])

zus.to_csv(f'Germany/RP/Worms/data/Worms_for_dw14_7.csv')
print(zus)
