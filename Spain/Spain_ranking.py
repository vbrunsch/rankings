from scipy import optimize
import datetime
import pandas as pd
import seaborn as sns
import json
import numpy as np
import os
numb=10
from datetime import date
#date_of_analysis='03/07/21'                                                                                                                                                      
date_of_analysis=date.today().strftime("%m/%d/%y")
print(date_of_analysis)

# Main Data Source JRC
df = pd.read_csv('https://raw.githubusercontent.com/ec-jrc/COVID-19/master/data-by-region/jrc-covid-19-all-days-by-regions.csv')
# change nan in regions to country names
regionnan = pd.isnull(df["Region"])
df["Region"].iloc[regionnan] = df[regionnan]["CountryName"]

output_directory="output_spain"
spain=df[df["CountryName"]=="Spain"]


#all_countries={'Spain':spain}


df3=spain
df3.rename(columns = {'Date':'date', 'Region':'province'}, inplace = True)
e_dataframe1=pd.pivot_table(df3, values='CumulativePositive', index=['date'],columns=['province'],aggfunc=np.mean)
e_dataframe1 = e_dataframe1.fillna(0).astype(int)
e_dataframe1 = e_dataframe1.diff().fillna(0)

e_dataframe1['Date'] = pd.to_datetime(e_dataframe1.index)
e_dataframe1.index = pd.to_datetime(e_dataframe1.index)
e_dataframe1['dated'] = e_dataframe1.Date.diff().dt.days

e_dataframe1 = e_dataframe1.drop('Date', axis = 1)

dates = pd.date_range(e_dataframe1.index.min(), e_dataframe1.index.max())

e_dataframe1 = e_dataframe1.reindex(dates)



for i in e_dataframe1.columns:
  e_dataframe1['datem'] = e_dataframe1[i] % e_dataframe1['dated']
  e_dataframe1['dateq'] = e_dataframe1[i]//e_dataframe1['dated']
  e_dataframe1 = e_dataframe1.fillna(0)

  e_dataframe1[i] = e_dataframe1['dateq']+e_dataframe1['datem']
  e_dataframe1 = e_dataframe1.drop('datem',axis = 1)

  for index, row in e_dataframe1.iloc[::-1].iterrows():
    if row['dated'] > 1:
      dq = row['dateq']
    elif row['dated'] == 0:
      e_dataframe1[i].loc[index]=dq

  e_dataframe1 = e_dataframe1.drop('dateq',axis = 1)

e_dataframe1 = e_dataframe1.drop('dated',axis = 1)
print(e_dataframe1)

cols=['Comunidad Autónoma','COVID-Free Days','New Cases in Last 14 Days', 'Last7', 'Previous7']
collect = []
for p in e_dataframe1.columns:
    if p != 'NC':
        n = e_dataframe1[p]
        #p_long = ab.loc[ab['Abbrev']==p,'Province'].item()
        ave = n
        ave.drop(ave.tail(4).index,inplace=True)
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

        collect.append((p,
                        c,
                        int(last_forteen),
                        int(last7),
                        int(prev7)))

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
tab.columns = ['Comunidad Autónoma', 'COVID-Free Days', 'New Cases in Last 14 Days', 'Last 7 Days', 'Pct Change']

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

tab = tab[['Rank', 'Comunidad Autónoma', 'COVID-Free Days', 'New Cases in Last 14 Days','Last 7 Days','Percent Change']]       
s = tab.style.apply(highlighter, axis = 1).set_table_styles(styles).hide_index()

import datetime
from datetime import date
x = date.today()
d = x.weekday()
day =["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
totime = datetime.datetime.now()
toti = '<center><caption>'+'Last Update: '+day[d]+ ', '+ totime.strftime('%Y-%m-%d, %H:%M:%S') + ' ' + totime.astimezone().tzname() + '</caption></center>'

try:        
    with open(f'Spain.html', 'w', encoding="utf-8") as out:
        body = s.render().replace('&#x2197;','<span style="color: red"> &#x2197;</span>') # red arrow up
        body = body.replace('&#x2198','<span style="color: green"> &#x2198;</span>') # green arrow down
        content = top + toti + body + bottom
        out.write(content)
except Exception as e:
    print(f'Error:\n{e}')
