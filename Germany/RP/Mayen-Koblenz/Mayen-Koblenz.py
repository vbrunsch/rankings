
#pip install -q tabula-py
import os

from datetime import timedelta
import tabula
import pandas as pd
neu = pd.DataFrame()

for x in range(1,15):
    to = pd.Timestamp.today() -timedelta(days=x)
    if to.month == 1:
        mon = 'Januar%20' + str(to.year)
        mont = 'Januar'
    elif to.month == 2:
        mon = 'Februar%20' + str(to.year)
        mont = 'Februar'
    elif to.month == 3:
        mon = 'M%C3%A4rz%20' + str(to.year)
        mont = 'M%C3%A4rz'
    elif to.month == 4:
        mon = 'April%20' + str(to.year)
        mont = 'April'
    elif to.month == 5:
        mon = 'Mai%20' + str(to.year)
        mont = 'Mai'
    elif to.month == 6:
        mon = 'Juni%20' + str(to.year)
        mont = 'Juni'
    elif to.month == 7:
        mon = 'Juli%20' + str(to.year)
        mont = 'Juli'
    elif to.month == 8:
        mon = 'August%20' + str(to.year)
        mont = 'August'
    elif to.month == 9:
        mon = 'September%20' + str(to.year)
        mont = 'September'
    elif to.month == 10:
        mon = 'Oktober%20' + str(to.year)
        mont = 'Oktober'
    elif to.month == 11:
        mon = 'November%20' + str(to.year)
        mont = 'November'
    elif to.month == 12:
        mon = 'Dezember%20' + str(to.year)
        mont = 'Dezember'

    tod = to.strftime('%d.%m.%Y')
    pdf_path = "https://www.kvmyk.de/kv_myk/Corona/Corona-Statistiken/" + mon + "/Fallzahlen%20" + tod + ".pdf"
    pdf_path_t = "https://www.kvmyk.de/kv_myk/Corona/Corona-Statistiken/" + mont + "/Fallzahlen " + tod + ".pdf"
    
    try:
      dfs = tabula.read_pdf(pdf_path, stream=True)
      print(pdf_path)
    except:
      try:
        dfs = tabula.read_pdf(pdf_path_t, stream=True)
        print(pdf_path_t)
      except:
        print(tod)

    if tod == '07.04.2021':
        df = pd.DataFrame(data = [8,8,21,7,7,0,4,3,5,1,10,74], columns=[tod], index = ['Andernach', 'Bendorf', 'Koblenz','Mayen','VG Maifeld','VG Mendig','VG Pellenz','VG Rhein-Mosel','VG Vallendar','VG Vordereifel','VG Weißenthurm','Summe'])
    elif tod in ['01.05.2021','02.05.2021','24.05.2021','19.06.2021','20.06.2021','23.06.2021'] or to.weekday()>4:
        df = pd.DataFrame(data = [0,0,0,0,0,0,0,0,0,0,0,0], columns=[tod], index = ['Andernach', 'Bendorf', 'Koblenz','Mayen','VG Maifeld','VG Mendig','VG Pellenz','VG Rhein-Mosel','VG Vallendar','VG Vordereifel','VG Weißenthurm','Summe'])
    elif tod == '07.09.2021':
        df = pd.DataFrame(data = [13,7,23,1,1,0,3,0,3,1,8,60], columns=[tod], index = ['Andernach', 'Bendorf', 'Koblenz','Mayen','VG Maifeld','VG Mendig','VG Pellenz','VG Rhein-Mosel','VG Vallendar','VG Vordereifel','VG Weißenthurm','Summe'])
    elif tod in ['03.05.2021','04.05.2021','06.05.2021','07.05.2021']:
        df = dfs[0]
        print(df)
        df = df.replace({'Stadt Andernach':'Andernach'}, regex=True)
        df = df.replace({'Stadt Bendorf':'Bendorf'}, regex=True)
        df = df.replace({'Stadt Koblenz':'Koblenz'}, regex=True)
        df = df.replace({'Stadt Mayen':'Mayen'}, regex=True)
        df = df.set_index('Stadt/VG')
        df[tod] = df['Unnamed: 0']
        df = df[[tod]]        
    else:
        df = dfs[0]
        df = df.replace({'Stadt Andernach':'Andernach'}, regex=True)
        df = df.replace({'Stadt Bendorf':'Bendorf'}, regex=True)
        df = df.replace({'Stadt Koblenz':'Koblenz'}, regex=True)
        df = df.replace({'Stadt Mayen':'Mayen'}, regex=True)
        try:
          df = df.set_index('Stadt / VG')
        except:
          df = df.set_index('Stadt/VG')
        df[tod] = df['+-']
        df = df[[tod]]
        

    
    if neu.empty:
        neu = df.copy()
    else:
        neu = neu.join(df)
    print(tod) 
print(neu)

neu = neu.replace({'\+/\-':''}, regex=True)
neu = neu.replace({'\+':''}, regex=True)
neu = neu.replace({'\-':''}, regex=True)
neu = neu.astype(int)
neu = neu[:-1]

neu.to_csv(f'Germany/RP/Mayen-Koblenz/data/Mayen_current.csv')

neu['Gemeinde'] = neu.index
neu['AGS'] = ['07137003','07137203','07111000','07137068','07137023','07137008','07137056','07137201','07137218','07137001','07137202']

#VG Maifeld
neu = neu.append(neu.loc[neu['AGS'] == '07137023'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137027'
neu = neu.append(neu.loc[neu['AGS'] == '07137023'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137029'
neu = neu.append(neu.loc[neu['AGS'] == '07137023'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137030'
neu = neu.append(neu.loc[neu['AGS'] == '07137023'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137041'
neu = neu.append(neu.loc[neu['AGS'] == '07137023'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137048'
neu = neu.append(neu.loc[neu['AGS'] == '07137023'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137053'
neu = neu.append(neu.loc[neu['AGS'] == '07137023'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137065'
neu = neu.append(neu.loc[neu['AGS'] == '07137023'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137070'
neu = neu.append(neu.loc[neu['AGS'] == '07137023'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137501'
neu = neu.append(neu.loc[neu['AGS'] == '07137023'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137080'
neu = neu.append(neu.loc[neu['AGS'] == '07137023'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137086'
neu = neu.append(neu.loc[neu['AGS'] == '07137023'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137087'
neu = neu.append(neu.loc[neu['AGS'] == '07137023'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137089'
neu = neu.append(neu.loc[neu['AGS'] == '07137023'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137095'
neu = neu.append(neu.loc[neu['AGS'] == '07137023'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137102'
neu = neu.append(neu.loc[neu['AGS'] == '07137023'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137112'
neu = neu.append(neu.loc[neu['AGS'] == '07137023'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137114'

#VG Mendig
neu = neu.append(neu.loc[neu['AGS'] == '07137008'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137069'      
neu = neu.append(neu.loc[neu['AGS'] == '07137008'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137093'      
neu = neu.append(neu.loc[neu['AGS'] == '07137008'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137101'      
neu = neu.append(neu.loc[neu['AGS'] == '07137008'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137106'

#VG Pellenz
neu = neu.append(neu.loc[neu['AGS'] == '07137056'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137057'        
neu = neu.append(neu.loc[neu['AGS'] == '07137056'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137081'        
neu = neu.append(neu.loc[neu['AGS'] == '07137056'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137088'        
neu = neu.append(neu.loc[neu['AGS'] == '07137056'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137096'     

#VG Rhein-Mosel
neu = neu.append(neu.loc[neu['AGS'] == '07137201'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137204'   
neu = neu.append(neu.loc[neu['AGS'] == '07137201'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137205'   
neu = neu.append(neu.loc[neu['AGS'] == '07137201'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137206'   
neu = neu.append(neu.loc[neu['AGS'] == '07137201'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137207'   
neu = neu.append(neu.loc[neu['AGS'] == '07137201'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137208'   
neu = neu.append(neu.loc[neu['AGS'] == '07137201'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137212'   
neu = neu.append(neu.loc[neu['AGS'] == '07137201'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137504'   
neu = neu.append(neu.loc[neu['AGS'] == '07137201'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137214'   
neu = neu.append(neu.loc[neu['AGS'] == '07137201'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137215'   
neu = neu.append(neu.loc[neu['AGS'] == '07137201'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137217'   
neu = neu.append(neu.loc[neu['AGS'] == '07137201'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137219'   
neu = neu.append(neu.loc[neu['AGS'] == '07137201'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137220'   
neu = neu.append(neu.loc[neu['AGS'] == '07137201'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137221'   
neu = neu.append(neu.loc[neu['AGS'] == '07137201'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137223'   
neu = neu.append(neu.loc[neu['AGS'] == '07137201'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137227'   
neu = neu.append(neu.loc[neu['AGS'] == '07137201'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137230'   
neu = neu.append(neu.loc[neu['AGS'] == '07137201'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137231' 

#VG Vallendar
neu = neu.append(neu.loc[neu['AGS'] == '07137218'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137224'  
neu = neu.append(neu.loc[neu['AGS'] == '07137218'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137226'  
neu = neu.append(neu.loc[neu['AGS'] == '07137218'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137229' 

#VG Vordereifel
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137004' 
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137006' 
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137007' 
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137011' 
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137014' 
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137019' 
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137025' 
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137034' 
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137035' 
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137036' 
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137043' 
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137049' 
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137055' 
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137060' 
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137061' 
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137063' 
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137066' 
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137074' 
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137077' 
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137079' 
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137092' 
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137097' 
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137099' 
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137105' 
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137110' 
neu = neu.append(neu.loc[neu['AGS'] == '07137001'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137113' 

#VG Weißenthurm
neu = neu.append(neu.loc[neu['AGS'] == '07137202'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137209'
neu = neu.append(neu.loc[neu['AGS'] == '07137202'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137211'
neu = neu.append(neu.loc[neu['AGS'] == '07137202'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137216'
neu = neu.append(neu.loc[neu['AGS'] == '07137202'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137222'
neu = neu.append(neu.loc[neu['AGS'] == '07137202'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137225'
neu = neu.append(neu.loc[neu['AGS'] == '07137202'], ignore_index = True)
neu.at[len(neu)-1,'AGS']= '07137228'

neu = neu.set_index('AGS')
print(neu)

import numpy as np
zus = pd.DataFrame()
zus['last7'] = neu[neu.columns[0]]+neu[neu.columns[1]]+neu[neu.columns[2]]+neu[neu.columns[3]]+neu[neu.columns[4]]+neu[neu.columns[5]]+neu[neu.columns[6]]
zus['last14'] = zus['last7'] + neu[neu.columns[7]]+neu[neu.columns[8]]+neu[neu.columns[9]]+neu[neu.columns[10]]+neu[neu.columns[11]]+neu[neu.columns[12]]+neu[neu.columns[13]]
zus['mix'] = np.where(zus['last7'] == 0, 0.6, zus['last7'])
zus['mix'] = np.where(zus['last14'] == 0, 0.2, zus['mix'])
zus['Gemeinde'] = neu['Gemeinde']
zus.to_csv(f'Germany/RP/Mayen-Koblenz/data/Mayen_for_dw14_7.csv')
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

import datetime
# Save pickle and last updated time for visualizations
region_path = "germany/rp/mayenkoblenz"
config_path = "visualizations"
pickle_file = f"{config_path}/pickles/{region_path}.pkl"
last_updated_file = f"{config_path}/last-updated/{region_path}.log"
os.makedirs(os.path.dirname(pickle_file), exist_ok=True)
os.makedirs(os.path.dirname(last_updated_file), exist_ok=True)
tab.to_pickle(pickle_file)
with open(last_updated_file, 'w') as file:
    file.write(datetime.datetime.utcnow().strftime('%m/%d/%Y %H:%M:%S UTC'))

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
    with open(f'Mayen-Koblenz.html', 'w', encoding="utf-8") as out:
        body = s.render().replace('&#x2197;','<span style="color: red"> &#x2197;</span>') # red arrow up
        body = body.replace('&#x2198','<span style="color: green"> &#x2198;</span>') # green arrow down
        content = top + toti + body + bottom
        out.write(content)
except Exception as e:
    print(f'Error:\n{e}')
