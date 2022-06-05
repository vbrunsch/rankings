import chardet
import pandas as pd
import requests
from zipfile import ZipFile
from io import BytesIO
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time 
import re
from datetime import datetime
from datetime import timedelta

que = f'https://covid19.ssi.dk/overvagningsdata/download-fil-med-overvaagningdata'

t3 = requests.get(que).text
htmlParse = BeautifulSoup(t3, 'html.parser')

to = pd.Timestamp.today()# - timedelta(days = 1)
tod = to.strftime('%m_%d_%Y')
ye = to - timedelta(days = 1)
yes = ye.strftime('%m_%d_%Y')
gem = re.findall('a href="(https://files.ssi.dk/covid19/overvagning/dashboard/overvaagningsdata-dashboard-covid19.*)" target=',t3)

r = requests.get(gem[0])
z = ZipFile(BytesIO(r.content))    
file = z.extract('Kommunalt_DB/07_bekraeftede_tilfaelde_pr_dag_pr_kommune.csv')
#with open(file) as f:
#    print(f.read())

with open(file,'rb') as f:
    result = chardet.detect(f.read())  # or readline if the file is large


df= pd.read_csv(file, encoding=result['encoding'],sep=';',engine='python')
print(df)
