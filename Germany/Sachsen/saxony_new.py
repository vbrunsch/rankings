#!/usr/bin/env python
# coding: utf-8
import os

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

df = pd.read_html('https://www.coronavirus.sachsen.de/corona-statistics/rest/communitySituation.jsp?boundaryId=14625&_=1618533867674', encoding = 'utf-8')[0]#.set_index('Unnamed: 0')#df_list[-11]
df['Landkreis'] = 'Bautzen'
df1 = pd.read_html('https://www.coronavirus.sachsen.de/corona-statistics/rest/communitySituation.jsp?boundaryId=14521&_=1618533867675', encoding = 'utf-8')[0]#.set_index('Unnamed: 0')#df_list[-10]
df1['Landkreis'] = 'Erzgebirgskreis'
df2 = pd.read_html('https://www.coronavirus.sachsen.de/corona-statistics/rest/communitySituation.jsp?boundaryId=14626&_=1618533867676', encoding = 'utf-8')[0]#.set_index('Unnamed: 0')#df_list[-9]
df2['Landkreis'] = 'Görlitz'
df3 = pd.read_html('https://www.coronavirus.sachsen.de/corona-statistics/rest/communitySituation.jsp?boundaryId=14729&_=1618533867677', encoding = 'utf-8')[0]#.set_index('Unnamed: 0')#df_list[-8]
df3['Landkreis'] = 'Leipzig'
df4 = pd.read_html('https://www.coronavirus.sachsen.de/corona-statistics/rest/communitySituation.jsp?boundaryId=14627&_=1618533867678', encoding = 'utf-8')[0]#.set_index('Unnamed: 0')#df_list[-7]
df4['Landkreis'] = 'Meißen'
df5 = pd.read_html('https://www.coronavirus.sachsen.de/corona-statistics/rest/communitySituation.jsp?boundaryId=14522&_=1618533867679', encoding = 'utf-8')[0]#.set_index('Unnamed: 0')#df_list[-6]
df5['Landkreis'] = 'Mittelsachsen'
df6 = pd.read_html('https://www.coronavirus.sachsen.de/corona-statistics/rest/communitySituation.jsp?boundaryId=14730&_=1618533867680', encoding = 'utf-8')[0]#.set_index('Unnamed: 0')#df_list[-5]
df6['Landkreis'] = 'Nordsachsen'
df7 = pd.read_html('https://www.coronavirus.sachsen.de/corona-statistics/rest/communitySituation.jsp?boundaryId=14628&_=1618533867681', encoding = 'utf-8')[0]#.set_index('Unnamed: 0')#df_list[-4]
df7['Landkreis'] = 'Sächsische Schweiz-Osterzgebirge'
df8 = pd.read_html('https://www.coronavirus.sachsen.de/corona-statistics/rest/communitySituation.jsp?boundaryId=14523&_=1618533867682', encoding = 'utf-8')[0]#.set_index('Unnamed: 0')#df_list[-3]
df8['Landkreis'] = 'Vogtlandkreis'
df9 = pd.read_html('https://www.coronavirus.sachsen.de/corona-statistics/rest/communitySituation.jsp?boundaryId=14524&_=1618533867683', encoding = 'utf-8')[0]#.set_index('Unnamed: 0')#df_list[-2]
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

df['Gemeinde'] = df['Gemeinde'].str.replace(r'Bernsdorf, Stadt \(Landkreis Bautzen\)', 'Bernsdorf - Bautzen')
df['Gemeinde'] = df['Gemeinde'].str.replace(r'Bernsdorf \(Landkreis Zwickau\)', 'Bernsdorf - Zwickau')
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
d = datum - timedelta(days=8)

old = pd.read_csv(f'Germany/Sachsen/data/Sachsen_Staedte_for_rankings_{d.date()}.csv')

old['Gemeinde'] = old['Gemeinde'].str.replace(r'Bernsdorf, Stadt \(Landkreis Bautzen\)', 'Bernsdorf - Bautzen')
old['Gemeinde'] = old['Gemeinde'].str.replace(r'Bernsdorf \(Landkreis Zwickau\)', 'Bernsdorf - Zwickau')
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

# Map for Bautzen only
bau_only = mdf[mdf['Landkreis']=='Bautzen']
bau_only['Neuzugänge letzten 7 Tage'] = bau_only['Neuzugänge letzten 7 Tage_x']
bau_only['Neuzugänge letzten 7 Tage_x'] = np.where(bau_only['Neuzugänge letzten 7 Tage_x'] == 0, 0.6, bau_only['Neuzugänge letzten 7 Tage_x'])
bau_only['Neuzugänge letzten 7 Tage_x'] = np.where(bau_only['Neuzugänge letzten 14 Tage'] == 0, 0.2, bau_only['Neuzugänge letzten 7 Tage_x'])
bau_only['Neuzugänge letzten 7 Tage_x'] = bau_only['Neuzugänge letzten 7 Tage_x']*10
bau_only.to_csv(f'Germany/Sachsen/data/Sachsen_Bautzen_for_dw_14_Tage_neu.csv')

# Map for Erzgebirgskreis only
erz_only = mdf[mdf['Landkreis']=='Erzgebirgskreis']
erz_only['Neuzugänge letzten 7 Tage'] = erz_only['Neuzugänge letzten 7 Tage_x']
erz_only['Neuzugänge letzten 7 Tage_x'] = np.where(erz_only['Neuzugänge letzten 7 Tage_x'] == 0, 0.6, erz_only['Neuzugänge letzten 7 Tage_x'])
erz_only['Neuzugänge letzten 7 Tage_x'] = np.where(erz_only['Neuzugänge letzten 14 Tage'] == 0, 0.2, erz_only['Neuzugänge letzten 7 Tage_x'])
erz_only['Neuzugänge letzten 7 Tage_x'] = erz_only['Neuzugänge letzten 7 Tage_x']*10
erz_only.to_csv(f'Germany/Sachsen/data/Sachsen_Erzgebirgskreis_for_dw_14_Tage_neu.csv')

# Map for Leipzig only
lei_only = mdf[mdf['Landkreis']=='Leipzig']
lei_only['Neuzugänge letzten 7 Tage'] = lei_only['Neuzugänge letzten 7 Tage_x']
lei_only['Neuzugänge letzten 7 Tage_x'] = np.where(lei_only['Neuzugänge letzten 7 Tage_x'] == 0, 0.6, lei_only['Neuzugänge letzten 7 Tage_x'])
lei_only['Neuzugänge letzten 7 Tage_x'] = np.where(lei_only['Neuzugänge letzten 14 Tage'] == 0, 0.2, lei_only['Neuzugänge letzten 7 Tage_x'])
lei_only['Neuzugänge letzten 7 Tage_x'] = lei_only['Neuzugänge letzten 7 Tage_x']*10
lei_only.to_csv(f'Germany/Sachsen/data/Sachsen_Leipzig_for_dw_14_Tage_neu.csv')

# Map for Meißen only
mei_only = mdf[mdf['Landkreis']=='Meißen']
mei_only['Neuzugänge letzten 7 Tage'] = mei_only['Neuzugänge letzten 7 Tage_x']
mei_only['Neuzugänge letzten 7 Tage_x'] = np.where(mei_only['Neuzugänge letzten 7 Tage_x'] == 0, 0.6, mei_only['Neuzugänge letzten 7 Tage_x'])
mei_only['Neuzugänge letzten 7 Tage_x'] = np.where(mei_only['Neuzugänge letzten 14 Tage'] == 0, 0.2, mei_only['Neuzugänge letzten 7 Tage_x'])
mei_only['Neuzugänge letzten 7 Tage_x'] = mei_only['Neuzugänge letzten 7 Tage_x']*10
mei_only.to_csv(f'Germany/Sachsen/data/Sachsen_Meißen_for_dw_14_Tage_neu.csv')

# Map for Nordsachsen only
nor_only = mdf[mdf['Landkreis']=='Nordsachsen']
nor_only['Neuzugänge letzten 7 Tage'] = nor_only['Neuzugänge letzten 7 Tage_x']
nor_only['Neuzugänge letzten 7 Tage_x'] = np.where(nor_only['Neuzugänge letzten 7 Tage_x'] == 0, 0.6, nor_only['Neuzugänge letzten 7 Tage_x'])
nor_only['Neuzugänge letzten 7 Tage_x'] = np.where(nor_only['Neuzugänge letzten 14 Tage'] == 0, 0.2, nor_only['Neuzugänge letzten 7 Tage_x'])
nor_only['Neuzugänge letzten 7 Tage_x'] = nor_only['Neuzugänge letzten 7 Tage_x']*10
nor_only.to_csv(f'Germany/Sachsen/data/Sachsen_Nordsachsen_for_dw_14_Tage_neu.csv')

# Map for Sächsische Schweiz-Osterzgebirge only
ost_only = mdf[mdf['Landkreis']=='Sächsische Schweiz-Osterzgebirge']
ost_only['Neuzugänge letzten 7 Tage'] = ost_only['Neuzugänge letzten 7 Tage_x']
ost_only['Neuzugänge letzten 7 Tage_x'] = np.where(ost_only['Neuzugänge letzten 7 Tage_x'] == 0, 0.6, ost_only['Neuzugänge letzten 7 Tage_x'])
ost_only['Neuzugänge letzten 7 Tage_x'] = np.where(ost_only['Neuzugänge letzten 14 Tage'] == 0, 0.2, ost_only['Neuzugänge letzten 7 Tage_x'])
ost_only['Neuzugänge letzten 7 Tage_x'] = ost_only['Neuzugänge letzten 7 Tage_x']*10
ost_only.to_csv(f'Germany/Sachsen/data/Sachsen_Osterzgebirge_for_dw_14_Tage_neu.csv')

# Map for Vogtlandkreis only
vog_only = mdf[mdf['Landkreis']=='Vogtlandkreis']
vog_only['Neuzugänge letzten 7 Tage'] = vog_only['Neuzugänge letzten 7 Tage_x']
vog_only['Neuzugänge letzten 7 Tage_x'] = np.where(vog_only['Neuzugänge letzten 7 Tage_x'] == 0, 0.6, vog_only['Neuzugänge letzten 7 Tage_x'])
vog_only['Neuzugänge letzten 7 Tage_x'] = np.where(vog_only['Neuzugänge letzten 14 Tage'] == 0, 0.2, vog_only['Neuzugänge letzten 7 Tage_x'])
vog_only['Neuzugänge letzten 7 Tage_x'] = vog_only['Neuzugänge letzten 7 Tage_x']*10
vog_only.to_csv(f'Germany/Sachsen/data/Sachsen_Vogtlandkreis_for_dw_14_Tage_neu.csv')

# Map for Zwickau only
zwi_only = mdf[mdf['Landkreis']=='Zwickau']
zwi_only['Neuzugänge letzten 7 Tage'] = zwi_only['Neuzugänge letzten 7 Tage_x']
zwi_only['Neuzugänge letzten 7 Tage_x'] = np.where(zwi_only['Neuzugänge letzten 7 Tage_x'] == 0, 0.6, zwi_only['Neuzugänge letzten 7 Tage_x'])
zwi_only['Neuzugänge letzten 7 Tage_x'] = np.where(zwi_only['Neuzugänge letzten 14 Tage'] == 0, 0.2, zwi_only['Neuzugänge letzten 7 Tage_x'])
zwi_only['Neuzugänge letzten 7 Tage_x'] = zwi_only['Neuzugänge letzten 7 Tage_x']*10
zwi_only.to_csv(f'Germany/Sachsen/data/Sachsen_Zwickau_for_dw_14_Tage_neu.csv')


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

df = pd.read_html('https://www.coronavirus.sachsen.de/corona-statistics/rest/communitySituation.jsp?boundaryId=14625&_=1618533867674', encoding = 'utf-8')[0]#.set_index('Unnamed: 0')#df_list[-11]
bau_gems = df['Gemeinde'].unique()
df1 = pd.read_html('https://www.coronavirus.sachsen.de/corona-statistics/rest/communitySituation.jsp?boundaryId=14521&_=1618533867675', encoding = 'utf-8')[0]#.set_index('Unnamed: 0')#df_list[-10]
df2 = pd.read_html('https://www.coronavirus.sachsen.de/corona-statistics/rest/communitySituation.jsp?boundaryId=14626&_=1618533867676', encoding = 'utf-8')[0]#.set_index('Unnamed: 0')#df_list[-9]
df3 = pd.read_html('https://www.coronavirus.sachsen.de/corona-statistics/rest/communitySituation.jsp?boundaryId=14729&_=1618533867677', encoding = 'utf-8')[0]#.set_index('Unnamed: 0')#df_list[-8]
df4 = pd.read_html('https://www.coronavirus.sachsen.de/corona-statistics/rest/communitySituation.jsp?boundaryId=14627&_=1618533867678', encoding = 'utf-8')[0]#.set_index('Unnamed: 0')#df_list[-7]
df5 = pd.read_html('https://www.coronavirus.sachsen.de/corona-statistics/rest/communitySituation.jsp?boundaryId=14522&_=1618533867679', encoding = 'utf-8')[0]#.set_index('Unnamed: 0')#df_list[-6]
df6 = pd.read_html('https://www.coronavirus.sachsen.de/corona-statistics/rest/communitySituation.jsp?boundaryId=14730&_=1618533867680', encoding = 'utf-8')[0]#.set_index('Unnamed: 0')#df_list[-5]
df7 = pd.read_html('https://www.coronavirus.sachsen.de/corona-statistics/rest/communitySituation.jsp?boundaryId=14628&_=1618533867681', encoding = 'utf-8')[0]#.set_index('Unnamed: 0')#df_list[-4]
df8 = pd.read_html('https://www.coronavirus.sachsen.de/corona-statistics/rest/communitySituation.jsp?boundaryId=14523&_=1618533867682', encoding = 'utf-8')[0]#.set_index('Unnamed: 0')#df_list[-3]
df9 = pd.read_html('https://www.coronavirus.sachsen.de/corona-statistics/rest/communitySituation.jsp?boundaryId=14524&_=1618533867683', encoding = 'utf-8')[0]#.set_index('Unnamed: 0')#df_list[-2]
#df = df_list[-11]
#df1 = df_list[-10]
#df2 = df_list[-9]
#df3 = df_list[-8]
#df4 = df_list[-7]
#df5 = df_list[-6]
#df6 = df_list[-5]
#df7 = df_list[-4]
#df8 = df_list[-3]
#df9 = df_list[-2]

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

# Goerlitz Tabelle
goe_gems = df2['Gemeinde'].unique()
goe_tab = tab[tab['Gemeinde'].isin(goe_gems)]

# Mittelsachsen Tabelle
mit_gems = df5['Gemeinde'].unique()
mit_tab = tab[tab['Gemeinde'].isin(mit_gems)]

# Bautzen Tabelle

bau_tab = tab[tab['Gemeinde'].isin(bau_gems)]

# Erzgebirgskreis Tabelle
erz_gems = df1['Gemeinde'].unique()
erz_tab = tab[tab['Gemeinde'].isin(erz_gems)]

# Leipzig Tabelle
lei_gems = df3['Gemeinde'].unique()
lei_tab = tab[tab['Gemeinde'].isin(lei_gems)]

# Meißen Tabelle
mei_gems = df4['Gemeinde'].unique()
mei_tab = tab[tab['Gemeinde'].isin(mei_gems)]

# Nordsachsen Tabelle
nor_gems = df6['Gemeinde'].unique()
nor_tab = tab[tab['Gemeinde'].isin(nor_gems)]

# Sächsische Schweiz-Osterzgebirge Tabelle
ost_gems = df7['Gemeinde'].unique()
ost_tab = tab[tab['Gemeinde'].isin(ost_gems)]

# Vogtlandkreis Tabelle
vog_gems = df8['Gemeinde'].unique()
vog_tab = tab[tab['Gemeinde'].isin(vog_gems)]

# Zwickau Tabelle
zwi_gems = df9['Gemeinde'].unique()
zwi_tab = tab[tab['Gemeinde'].isin(zwi_gems)]


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

# Save visualization data and HTML tables
tables = [[tab.copy(), "Sachsen_neu.html", "germany/saxony"],
          [goe_tab.copy(), "Görlitz_neu.html", "germany/saxony/goerlitz"],
          [mit_tab.copy(), "Mittelsachsen_neu.html", "germany/saxony/mittelsachsen"],
          [bau_tab.copy(), "Bautzen_neu.html", "germany/saxony/bautzen"],
          [erz_tab.copy(), "Erzgebirgskreis_neu.html", "germany/saxony/erzgebirgskreis"],
          [lei_tab.copy(), "Leipzig_neu.html", "germany/saxony/leipzig"],
          [mei_tab.copy(), "Meißen_neu.html", "germany/saxony/meißen"],
          [nor_tab.copy(), "Nordsachsen_neu.html", "germany/saxony/nordsachsen"],
          [ost_tab.copy(), "Osterzgebirge_neu.html", "germany/saxony/osterzgebirge"],
          [vog_tab.copy(), "Vogtlandkreis_neu.html", "germany/saxony/vogtlandkreis"],
          [zwi_tab.copy(), "Zwickau_neu.html", "germany/saxony/zwickau"]]

for table in tables:
    toti = datetime.utcnow().strftime('%m/%d/%Y %H:%M:%S UTC')
    # Save pickle and last updated time for visualizations
    pickle_file = f"visualizations/pickles/{table[2]}.pkl"
    last_updated_file = f"visualizations/last-updated/{table[2]}.log"
    os.makedirs(os.path.dirname(pickle_file), exist_ok=True)
    os.makedirs(os.path.dirname(last_updated_file), exist_ok=True)
    table[0].to_pickle(pickle_file)
    with open(last_updated_file, 'w') as file:
        file.write(toti)

    toti = "<center><caption>Last Update: " + toti + "</caption></center>"
    arrow = lambda x : ' &#x2197;' if x>0 else (' &#x2192' if x ==0  else ' &#x2198')
    styles=[hover(),]
    table[0]['Platz'] = table[0].reset_index().index
    table[0]['Platz'] = table[0]['Platz'].add(1)
    table[0]['Platz'] = np.where(table[0]['Neuzugänge letzten 14 Tage'] == 0 , 1, table[0]['Platz'])
    table[0]['Trend'] = table[0]['PercentChange'].map(arrow)
    table[0]['Percent Change'] = table[0]['PercentChange'].map('{:,.2f}%'.format) + table[0]['Trend']
    table[0] = table[0].drop(['Trend','PercentChange'], axis = 1)

    table[0].rename(columns = {'Neuzugänge letzten 14 Tage':'Neue Fälle letzte 14 Tage'}, inplace = True)
    table[0].rename(columns = {'Neuzugänge letzten 7 Tage_x':'Letzte 7 Tage'}, inplace = True)
    table[0].rename(columns = {'Percent Change':'Trend'}, inplace = True)
    table[0].rename(columns = {'Gemeinde':'Stadt/Gemeinde'}, inplace = True)

    table[0] = table[0][['Platz', 'Stadt/Gemeinde', 'Covid-freie Wochen', 'Neue Fälle letzte 14 Tage', 'Letzte 7 Tage','Trend']]
    table[0] = table[0].drop('Covid-freie Wochen', axis = 1)
    s = table[0].style.apply(highlighter, axis = 1).set_table_styles(styles).hide_index()

    try:
        with open(table[1], 'w', encoding="utf-8") as out:
            body = s.render().replace('&#x2197;','<span style="color: red"> &#x2197;</span>') # red arrow up
            body = body.replace('&#x2198','<span style="color: green"> &#x2198;</span>') # green arrow down
            content = top + toti + body + bottom
            out.write(content)
    except Exception as e:
        print(f'Error:\n{e}')
