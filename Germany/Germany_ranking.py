import os
from datetime import datetime
import logging
import urllib.request, urllib.error, urllib.parse
import pandas as pd
import numpy as np
import geopandas as gpd
import json, requests
from json import loads

final_gdf = pd.DataFrame()
for i in ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16']:  
  baseURL = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_" + i + "_hubv/FeatureServer/0"
  fields = "*"
  # Get record extract limit
  urlstring = baseURL + "?f=json"
  j = urllib.request.urlopen(urlstring)
  js = json.load(j)
  maxrcn = int(js["maxRecordCount"])
  print(("Record extract limit: %s" % maxrcn))

  # Get object ids of features
  where = "1=1"#"Meldedatum>=CURRENT_TIMESTAMP-20"
  urlstring = baseURL + "/query?where={}&returnIdsOnly=true&f=json".format(where)
  j = urllib.request.urlopen(urlstring)
  js = json.load(j)
  idfield = js["objectIdFieldName"]
  idlist = js["objectIds"]
  idlist.sort()
  numrec = len(idlist)
  print(("Number of target records: %s" % numrec))

  # Gather features
  print("Gathering records…")
  fs = dict()
  fslist = []
  for i in range(0, numrec, maxrcn):
    torec = i + (maxrcn - 1)
    if torec > numrec:
      torec = numrec - 1
    fromid = idlist[i]
    toid = idlist[torec]
    where = "{} >= {} and {} <= {}".format(idfield, fromid, idfield, toid)
    print( " {}".format(where))
    urlstring = baseURL + "/query?where={}&returnGeometry=true&outFields={}&f=geojson".format(where,fields)
    resp = requests.get(urlstring, verify = False)
    data = resp.json() 
    gdf = gpd.GeoDataFrame.from_features(data['features'])
    #merge data
    fslist.append(gdf)
  inter_gdf = pd.concat(fslist)
  final_gdf = final_gdf.append(inter_gdf)


#df = gpd.read_file('https://opendata.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0.geojson')
df_pop = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/population%20Germany%20districts.csv')

focus = final_gdf.copy().drop(['ObjectId','Altersgruppe','Geschlecht','AnzahlTodesfall','Datenstand','NeuerFall','NeuerTodesfall','Refdatum','NeuGenesen','AnzahlGenesen','IstErkrankungsbeginn','Altersgruppe2','geometry'], axis=1)#.set_index(['Meldedatum'])
confirm = focus.groupby('Bundesland').sum().T
confirm_LK = focus.groupby('Landkreis').sum().T
#confirm_LK = confirm_LK.drop(['LK Göttingen (alt)'], axis = 1)

cols=['District/County Town','COVID-Free Days','New Cases in Last 14 Days','Last7','Previous7','Postcode','Population']
import datetime as dt
all_lks = pd.DataFrame()
collect = []
for country in confirm_LK.columns:
    bula = focus[focus['Landkreis']==country]
    #bula['Datum']= pd.to_datetime(bula['Meldedatum']).dt.date
    bula['Datum']= (bula['Meldedatum']/1000).astype(int).map(lambda x: pd.to_datetime(x, unit = 's'))
    bula = bula.sort_values(['Datum'], ascending=[True])
    bula['Total'] = bula.groupby(['Landkreis', 'Datum'])['AnzahlFall'].transform('sum')
    new_bula = bula.drop_duplicates(subset=['Landkreis', 'Datum'])


    bula2 = new_bula.copy().drop(['Bundesland','AnzahlFall'], axis=1)


    bula2.set_index('Datum', inplace=True)
    #bula2.index = pd.to_datetime(bula2.index).dt.date
    idx = pd.date_range('01/26/2020', dt.datetime.today().strftime("%m/%d/%Y"))
    bula2 = bula2.reindex(idx, fill_value=0)
    bula2.drop(bula2.tail(2).index,inplace=True)
    
    idzips = bula2['IdLandkreis'].unique()
    for i in idzips:
      if i not in [0,'0']:
        idzip = i
    all_lks[idzip]= bula2['Total']
    # print(bula2)

    ave = bula2['Total']
    las = len(ave)-14
    last_forteen = ave[las:].sum()
    if last_forteen < 0:
        last_forteen = 0
    last7 = ave[len(ave)-7:].sum() #last week
    prev7 = ave[len(ave)-14:len(ave)-7].sum() #prev week
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
        if ave[i] <= 0:
            c = c + 1
        else:
            i = 0
        i = i - 1

    # Get postcode
    postcode = bula2[bula2["IdLandkreis"] != 0]["IdLandkreis"].values[0]

    # Get population
    population_series = df_pop[df_pop.iloc[:, 0] == int(postcode)].iloc[:, 3]
    population = 100000
    if population_series.size > 0:
        population = population_series.values[0]
        population = int(population.replace(" ", ""))
    else:
        logging.error("Could not get population of %s! Defaulting population to 100,000", country)

    collect.append((country,
                    c,
                    last_forteen,
                    last7,
                    prev7,
                    postcode,
                    population
                    ))

all_lks[11000] = all_lks[11001]+all_lks[11002]+all_lks[11003]+all_lks[11004]+all_lks[11005]+all_lks[11006]+all_lks[11007]+all_lks[11008]+all_lks[11009]+all_lks[11010]+all_lks[11011]+all_lks[11012]
all_lks.to_csv('German_regions_cases.csv')    
# Calculate Incidences
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

# Cases per 100k (with hacky fix to remove floating points)
tab['Cases per 100k (Last 7 Days)'] = ((tab['Last7'] / tab['Population']) * 100000).\
    apply('{:.2f}'.format).astype('float')
tab['Cases per 100k (Last 14 Days)'] = (((tab['Last7'] + tab['Previous7']) / tab['Population']) * 100000).\
    apply('{:.2f}'.format).astype('float')

tab = tab.drop(['Previous7'], axis=1)
tab.columns = ['District/County Town', 'COVID-Free Days', 'New Cases in Last 14 Days', 'Last 7 Days', 'Postcode',
               'Population', 'Pct Change', 'Cases per 100k (Last 7 Days)', 'Cases per 100k (Last 14 Days)']

# Save dataframe for the visualization, then reset table for the rankings page
districts_formatted = tab['District/County Town'].str.split(" ").\
    map(lambda split: f'{" ".join(split[1:])}, {split[0]}')
tab_formatted = tab
tab_formatted['District/County Town'] = districts_formatted

# Save pickle and last updated time for visualizations
pickle_file = "visualizations/pickles/germany.pkl"
last_updated_file = "visualizations/last-updated/germany.log"
os.makedirs(os.path.dirname(pickle_file), exist_ok=True)
os.makedirs(os.path.dirname(last_updated_file), exist_ok=True)
tab_formatted.to_pickle(pickle_file)
with open(last_updated_file, 'w') as file:
    file.write(datetime.utcnow().strftime("%m/%d/%Y %H:%M:%S UTC"))

tab = tab.drop(['Postcode', 'Population', 'Cases per 100k (Last 7 Days)', 'Cases per 100k (Last 14 Days)'], axis=1)

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
tab['Trend'] = tab['Pct Change'].map(arrow)
tab['Percent Change'] = tab['Pct Change'].map('{:,.2f}%'.format) + tab['Trend']
tab = tab.drop(['Trend','Pct Change'], axis = 1)

tab = tab[['Rank', 'District/County Town', 'COVID-Free Days', 'New Cases in Last 14 Days','Last 7 Days','Percent Change']]
s = tab.style.apply(highlighter, axis = 1).set_table_styles(styles).hide_index()

import datetime
from datetime import date
x = date.today()
d = x.weekday()
day =["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
totime = datetime.datetime.now()
toti = '<center><caption>'+'Last Update: '+day[d]+ ', '+ totime.strftime('%Y-%m-%d, %H:%M:%S') + ' ' + totime.astimezone().tzname() + '</caption></center>'

try:
    with open(f'Germany.html', 'w', encoding="utf-8") as out:
        body = s.render().replace('&#x2197;','<span style="color: red"> &#x2197;</span>') # red arrow up
        body = body.replace('&#x2198','<span style="color: green"> &#x2198;</span>') # green arrow down
        content = top + toti + body + bottom
        out.write(content)
except Exception as e:
    print(f'Error:\n{e}')


