import numpy as np
import datetime
from datetime import timedelta
import pandas as pd

import re
import os
import time
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#93.0.4577.15
#91.0.4472.19
chromedriver_url = "https://chromedriver.storage.googleapis.com/93.0.4577.15/chromedriver_linux64.zip"
resp = urlopen(chromedriver_url)
with ZipFile(BytesIO(resp.read()), 'r') as zipObj:
    zipObj.extractall()
mode = os.stat('./chromedriver').st_mode
os.chmod('./chromedriver', mode | 0o111)

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("prefs", {"download.default_directory": os.getcwd()})
driver = webdriver.Chrome(options=options, executable_path=r'./chromedriver')

url = "https://data.gov.il/dataset/covid-19"
driver.get(url)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "content")))
id_url = driver.execute_script("""
let allLinks = document.querySelectorAll("a");
let targetLink;
for (let i = 0; i < allLinks.length; i++) {
    currTitle = allLinks[i].getAttribute("title");
    if (currTitle === "טבלת ישובים") {
        return allLinks[i].href;
    }
}
""")
print(id_url)
id = re.findall('https://data.gov.il/dataset/covid-19/resource/(.*)',id_url)
print(id)
csv_url = 'https://data.gov.il/datastore/dump/' + id[0] +'?bom=True'
print(csv_url)
try:
  os.rename(f'./{id[0]}.csv',f'./{id[0]}_old.csv')
except:
  print('oldname_prob')
driver.get(csv_url)
time.sleep(15)  # wait for download to complete
driver.close()
csv_path = f"./{id[0]}.csv"
#csv_path = csv_path + '.csv'
print(csv_path)
df_new = pd.read_csv(csv_path, index_col = 0)
df_old = pd.read_csv(r'israel_data.csv', index_col = 0)
#df_old = df_old.drop('Unnamed: 0', axis = 1)
if not df_new.equals(df_old):

    import requests
    from urllib.request import urlopen
    df1 = pd.read_csv(csv_path)
    town_lis1 = df1['City_Name'].unique()
    df1['Cumulative_verified_cases'] = np.where(df1['Cumulative_verified_cases']=='<15', 1, df1['Cumulative_verified_cases'])
    df1['Cumulative_verified_cases'] = df1['Cumulative_verified_cases'].astype(int)

    cols=['Area','COVID-Free Days','New Cases in Last 14 Days', 'Last7', 'Previous7']
    collect = []

    for d in town_lis1:
        if d != 'לא ידוע':

            fo1 = df1[df1['City_Name']==d]
            fo1 = fo1.set_index('Date')
            fo1 = fo1['Cumulative_verified_cases']
            ave = fo1.diff()
            ave = ave[1:]
            las = len(ave)-14
            last_forteen = int(ave[las:].sum().item())
            #last_forteen = sum(ave[las:])
            if last_forteen < 0:
                last_forteen = 0
            last7 = int(ave[len(ave)-7:].sum().item()) #last week
            prev7 = int(ave[len(ave)-14:len(ave)-7].sum().item()) #prev week
            #last7 = sum(ave[len(ave)-7:]) #last week
            #prev7 = sum(ave[len(ave)-14:len(ave)-7]) #prev week
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
            while i > -1:
                if ave.values[i] <= 0:
                    c = c + 1
                else:
                    i = 0
                i = i - 1

            collect.append((d,
                           int(c),
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
    tab.columns = ['Area', 'COVID-Free Days', 'New Cases in Last 14 Days', 'Last 7 Days', 'Pct Change']

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
            font-size: 80%;
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
    tab['Percent Change'] = tab['Pct Change'].map('{:,.2f}%'.format) +"<br>"+ tab['Trend']
    tab = tab.drop(['Trend','Pct Change'], axis = 1)

    tab = tab[['Rank', 'Area', 'COVID-Free Days', 'New Cases in Last 14 Days','Last 7 Days','Percent Change']]       
    s = tab.style.apply(highlighter, axis = 1).set_table_styles(styles).hide_index()

    toti = datetime.datetime.today().date() - timedelta(days = 1)
    if toti.weekday() <5:
        toti = "<center><caption>Wednesday, " + str(toti) + "</caption></center>"
    else:
        toti = "<center><caption>Sunday, " + str(toti) + "</caption></center>"

    try:        
        with open(f'Israel_new.html', 'w', encoding="utf-8") as out:
            body = s.render().replace('&#x2197;','<span style="color: red"> &#x2197;</span>') # red arrow up
            body = body.replace('&#x2198','<span style="color: green"> &#x2198;</span>') # green arrow down
            content = top + toti + body + bottom
            out.write(content)
    except Exception as e:
        print(f'Error:\n{e}')
        print(df1)


    ## old



    df1 = pd.read_csv(r'israel_data.csv')
    town_lis1 = df1['City_Name'].unique()
    df1['Cumulative_verified_cases'] = np.where(df1['Cumulative_verified_cases']=='<15', 1, df1['Cumulative_verified_cases'])
    df1['Cumulative_verified_cases'] = df1['Cumulative_verified_cases'].astype(int)

    cols=['Area','COVID-Free Days','New Cases in Last 14 Days', 'Last7', 'Previous7']
    collect = []

    for d in town_lis1:
        if d != 'לא ידוע':
            fo1 = df1[df1['City_Name']==d]
            fo1 = fo1.set_index('Date')
            fo1 = fo1['Cumulative_verified_cases']
            ave = fo1.diff()
            ave = ave[1:]
            las = len(ave)-14
            last_forteen = int(ave[las:].sum().item())
            #last_forteen = sum(ave[las:])
            if last_forteen < 0:
                last_forteen = 0
            last7 = int(ave[len(ave)-7:].sum().item()) #last week
            prev7 = int(ave[len(ave)-14:len(ave)-7].sum().item()) #prev week
            #last7 = sum(ave[len(ave)-7:]) #last week
            #prev7 = sum(ave[len(ave)-14:len(ave)-7]) #prev week
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
            while i > -1:
                if ave.values[i] <= 0:
                    c = c + 1
                else:
                    i = 0
                i = i - 1

            collect.append((d,
                           int(c),
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
    tab.columns = ['Area', 'COVID-Free Days', 'New Cases in Last 14 Days', 'Last 7 Days', 'Pct Change']

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
            font-size: 80%;
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
    tab['Percent Change'] = tab['Pct Change'].map('{:,.2f}%'.format) +"<br>"+ tab['Trend']
    tab = tab.drop(['Trend','Pct Change'], axis = 1)

    tab = tab[['Rank', 'Area', 'COVID-Free Days', 'New Cases in Last 14 Days','Last 7 Days','Percent Change']]       
    s = tab.style.apply(highlighter, axis = 1).set_table_styles(styles).hide_index()

    import datetime
    from datetime import timedelta
    toti = datetime.datetime.today().date() - timedelta(days = 1)
    if toti.weekday() <5:
        told = toti - timedelta(days = 3)
        told = "<center><caption>Sunday, " + str(told) + "</caption></center>"
    else:
        told = toti - timedelta(days = 4)
        told = "<center><caption>Wednesday, " + str(told) + "</caption></center>"

    try:        
        with open(f'Israel_old.html', 'w', encoding="utf-8") as out:
            body = s.render().replace('&#x2197;','<span style="color: red"> &#x2197;</span>') # red arrow up
            body = body.replace('&#x2198','<span style="color: green"> &#x2198;</span>') # green arrow down
            content = top + told + body + bottom
            out.write(content)
    except Exception as e:
        print(f'Error:\n{e}')
        print(df1)
    
    df_old.to_csv('israel_data_old.csv')
    df_new.to_csv('israel_data.csv')
