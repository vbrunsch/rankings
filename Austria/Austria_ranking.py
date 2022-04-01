#!/usr/bin/env python
# coding: utf-8

import numpy as np
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import datetime
from datetime import timedelta
import pandas as pd


bez = pd.DataFrame()
now = datetime.date.today()- datetime.timedelta(days=1)
yes = now - datetime.timedelta(days=1)
date_time = now.strftime("%Y%m%d")
date_time_y = yes.strftime("%Y%m%d")
print(date_time)
try:
    url = f"https://github.com/statistikat/coronaDAT/raw/master/archive/{date_time}/data/{date_time}_140202_orig_csv_ages.zip"
    resp = urlopen(url)
except:
    try:
        url = f"https://github.com/statistikat/coronaDAT/raw/master/archive/{date_time_y}/data/{date_time_y}_140202_orig_csv_ages.zip"
        resp = urlopen(url)
    except:
        try:
            url = f"https://github.com/statistikat/coronaDAT/raw/master/archive/{date_time_y}/data/{date_time_y}_140201_orig_csv_ages.zip"
            resp = urlopen(url)
        except:
            try:
                url = f"https://github.com/statistikat/coronaDAT/raw/master/archive/{date_time}/data/{date_time}_140201_orig_csv_ages.zip"
                resp = urlopen(url)
            except:
                pass

zipfile = ZipFile(BytesIO(resp.read()))
zipfile.namelist()

cols=['District','COVID-Free Days','New Cases in Last 14 Days', 'Last7', 'Previous7']
collect = []

df = pd.read_csv(zipfile.open('CovidFaelle_Timeline_GKZ.csv'),usecols=["Time;Bezirk;GKZ;AnzEinwohner;AnzahlFaelle;AnzahlFaelleSum;AnzahlFaelle7Tage;SiebenTageInzidenzFaelle;AnzahlTotTaeglich;AnzahlTotSum;AnzahlGeheiltTaeglich;AnzahlGeheiltSum"])
df2 = df[df.columns[0]].str.split(';', expand=True)
df2 = df2.set_index(0)
df2.index.name = None
for d in df2[1].unique():
    n = df2[df2[1]==d]
    ave = n[4].astype(int)
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
        if ave[i] <= 0:
            c = c + 1
        else:
            i = 0
        i = i - 1

    collect.append((d,
                   c,
                   last_forteen,
                   last7,
                   prev7))

    
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
tab.columns = ['District', 'COVID-Free Days', 'New Cases in Last 14 Days', 'Last 7 Days', 'Pct Change']

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
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script>
function colorize() {
var NW = String.fromCharCode(8599);
var SW = String.fromCharCode(8600);
$('td').each(function() {
    $(this).html($(this).html().
    replace(SW, '<span style="color: green">'+ SW +'</span>').
    replace(NW, '<span style="color: red">'+ NW +'</span>'))
    ;
});
};
</script>
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
<body onload=colorize()>
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

tab = tab[['Rank', 'District', 'COVID-Free Days', 'New Cases in Last 14 Days','Last 7 Days','Percent Change']]       
s = tab.style.apply(highlighter, axis = 1).set_table_styles(styles).hide_index()

import datetime
from datetime import date
x = date.today()
d = x.weekday()
day =["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
totime = datetime.datetime.now()
toti = '<center><caption>'+'Last Update: '+day[d]+ ', '+ totime.strftime('%Y-%m-%d, %H:%M:%S') + ' ' + totime.astimezone().tzname() + '</caption></center>'

try:        
    with open(f'Austria.html', 'w', encoding="utf-8") as out:
        content = top + toti + s.render() + bottom
        out.write(content)
except Exception as e:
    print(f'Error:\n{e}')
