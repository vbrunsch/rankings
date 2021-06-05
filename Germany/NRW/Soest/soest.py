import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time 
import requests
import re

que = 'https://gis.kreis-soest.de/server/rest/services/Krisenstab/Corona_Dashboard_Kreis_Soest_Oeffentlich/MapServer/0/query?f=json&where=GEMEINDE%3C%3E%27Kreis%20Soest%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=ort%20asc&resultOffset=0&resultRecordCount=14/'

t3 = requests.get(que).text
#htmlParse = BeautifulSoup(t3, 'html.parser')
#print(htmlParse)

from datetime import timedelta
to = pd.Timestamp.today() - timedelta(days = 1)
tod = to.strftime('%m_%d_%Y')
ye = pd.Timestamp.today() - timedelta(days = 2)
yes = ye.strftime('%m_%d_%Y')

gem = re.findall('ort":"(.*?)"',t3)
inf = re.findall('bestaetigte":(.*?),',t3)
infy = re.findall('bestaetigte_vortag":(.*?),',t3)
dat = re.findall('Q_timestamp":"(.*?)"',t3)

df = pd.DataFrame(data = inf, index = gem)
df.columns = [tod]
df[yes] = infy

print(dat)
print(df)
df.to_csv(f'Soest_{tod}.csv')
