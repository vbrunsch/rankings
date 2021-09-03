import pandas as pd
import numpy as np
from datetime import timedelta
to = pd.Timestamp.today() - timedelta(days = 1)
tod = to.strftime('%m_%d_%Y')
ye = to - timedelta(days = 1)
yes = ye.strftime('%m_%d_%Y')
ye2 = to - timedelta(days = 2)
yes2 = ye2.strftime('%m_%d_%Y')
ye3 = to - timedelta(days = 3)
yes3 = ye3.strftime('%m_%d_%Y')

df = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/BW/Alb-Donau/data/Alb-Donau_cur.csv',index_col= 0)
print('Today:')
print(tod)
print('Alb-Donau-Kreis')
print(df[df.columns[-4:]])
print('https://alb-donau-kreis.maps.arcgis.com/apps/dashboards/24f948a52d2a41d4b89cdbc3b8a949bb')
print()
print()

df = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/Bayern/Ansbach/data/Ansbach_current1.csv',index_col=0)
print('Today(if Sa, expect 0):')
print(tod)
print('Ansbach')
print(df[df.columns[0:4]])
print('https://www.landkreis-ansbach.de/Quicknavigation/Startseite/Aktuelle-Lage-zum-Coronavirus.php')
print()
print()

print('Today (if weekend expect last weekday):')
print(tod)
print('Freising')
st = 'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/Bayern/Freising/data/freising_'
try:
  df = pd.read_csv(f'{st}{tod}.csv',index_col=0)
  print(f'data from {tod}')
  print(df)
  df1 = pd.read_csv(f'{st}{yes}.csv',index_col=0)
  print(f'data from {yes}')
  print(df1)
  print(df[df.columns[2]]-df1[df1.columns[2]])
except:
  try:
    df = pd.read_csv(f'{st}{yes}.csv',index_col=0)
    print(f'data from {yes}')
    print(df)
    df1 = pd.read_csv(f'{st}{yes2}.csv',index_col=0)
    print(f'data from {yes2}')
    print(df1)
    print(df[df.columns[2]]-df1[df1.columns[2]])
  except:
    try:
      df = pd.read_csv(f'{st}{yes3}.csv',index_col=0)
      print(f'data from {yes3}')
      print(df)
    except:
      print(f'no new data for Freising at least since {yes3}')
print('https://landkreis-freising.de/aktuelle-informationen-zum-coronavirus-covid-19/zahlen-und-fakten.html')
print()
print()

print('Today (if weekend expect last weekday):')
print(tod)
print('LK Muenchen')
st = 'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/Bayern/LK_Muenchen/data/LK_M%C3%BCnchen_'
try:
  df = pd.read_csv(f'{st}{tod}.csv',index_col=0)
  print(f'data from {tod}')
  print(df)
  df = pd.read_csv(f'{st}{yes}.csv',index_col=0)
  print(f'data from {yes}')
  print(df)
except:
  try:
    df = pd.read_csv(f'{st}{yes}.csv',index_col=0)
    print(f'data from {yes}')
    print(df)
    df = pd.read_csv(f'{st}{yes2}.csv',index_col=0)
    print(f'data from {yes2}')
    print(df)
  except:
    try:
      df = pd.read_csv(f'{st}{yes3}.csv',index_col=0)
      print(f'data from {yes3}')
      print(df)
    except:
      print(f'no new data for LK Muenchen at least since {yes3}')
print('https://www.landkreis-muenchen.de/themen/verbraucherschutz-gesundheit/gesundheit/coronavirus/fallzahlen/')
print()
print()

df = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/Brandenburg/Uckermark/data/Uckermark%20old%20csv%20just%20new%20cases.csv',index_col= 0)
print('Today: (expect 0 at weekends)')
print(tod)
print('Uckermark')
print(df[df.columns[-4:]])
print('https://www.uckermark.de/index.phtml?La=1&mNavID=1897.1&object=tx,2203.741.1&kat=&kuo=2&sub=0')
print()
print()

print('Today (if weekend expect last weekday):')
print(tod)
print('Giessen')
st = 'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/Hessen/Giessen/data/LK_Giessen_letzte7_'
try:
  df = pd.read_csv(f'{st}{tod}.csv',index_col=0)
  print(f'data from {tod}')
  print(df[df.columns[-4:]])
  df = pd.read_csv(f'{st}{yes}.csv',index_col=0)
  print(f'data from {yes}')
  print(df[df.columns[-4:]])
except:
  print('no new data for Giessen')
  try:
    df = pd.read_csv(f'{st}{yes}.csv',index_col=0)
    print(f'data from {yes}')
    print(df[df.columns[-4:]])
    df = pd.read_csv(f'{st}{yes2}.csv',index_col=0)
    print(f'data from {yes2}')
    print(df[df.columns[-4:]])
  except:
    try:
      df = pd.read_csv(f'{st}{yes3}.csv',index_col=0)
      print(f'data from {yes3}')
      print(df[df.columns[-4:]])
    except:
      print(f'no new data for Giessen at least since {yes3}')
print('https://corona.lkgi.de/aktuelles/fallzahlen-im-landkreis/')
print()
print()


df = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/RP/Mayen-Koblenz/data/Mayen_current.csv',index_col= 0)
print('Today: (expect 0 at weekends)')
print(tod)
print('Mayen-Koblenz')
print(df[df.columns[0:4]])
print('https://www.kvmyk.de/kv_myk/Corona/Corona-Statistiken')
print()
print()

df = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/RP/Worms/data/Worms_current.csv',index_col= 0)
print('Today: (expect potential non-zero entries only for Monday and Thursday)')
print(tod)
print('Worms')
print(df[df.columns[0:4]])
print('https://www.kreis-alzey-worms.eu/verwaltung/aktuelles/')
print()
print()

df = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/Saarland/Merzig-Wadern/data/Merzig-Wadern_current.csv',index_col= 0)
print('Today:')
print(tod)
print('Merzig')
print(df[df.columns[-4:]])
print('https://docs.google.com/spreadsheets/d/1PDaRlOzlHGu-r-eFRl8N5lLa-_EHvvaGQ1jNvC-WYEs/edit#gid=1345922148')
print('https://www.merzig-wadern.de/Kurzmen%C3%BC/Startseite/-Newsticker-zum-Coronavirus-.php?object=tx,2875.5&ModID=7&FID=2875.1724.1&NavID=1918.1')
print()
print()

df = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/Saarland/Neunkirchen/data/Neunkirchen_for_dw14_7.csv',index_col= 0)
print('Today:')
print(tod)
print('Neunkirchen')
print(df[df.columns[0:4]])
print('https://www.landkreis-neunkirchen.de/index.php?id=3554')
print()
print()

df = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/Saarland/RV_Saarbruecken/data/RV_Saarbruecken_neu.csv',index_col= 0)
print('Today:')
print(tod)
print('Regionalverband Saarbruecken')
print(df[df.columns[-4:]])
print('https://www.regionalverband-saarbruecken.de/corona/')
print()
print()

df = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/Saarland/Saarpfalz-Kreis/data/Saarpfalz-Kreis_current.csv',index_col= 0)
print('Today:')
print(tod)
print('Saarpfalzkreis')
print(df[df.columns[-4:]])
print('https://www.saarpfalz-kreis.de/leben-soziales-gesundheit/gesundheit/coronavirus')
print()
print()

df = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/Saarland/St_Wendel/data/St_Wendel_current.csv',index_col= 0)
print('Today:')
print(tod)
print('St Wendel')
print(df[df.columns[-4:]])
print('https://www.landkreis-st-wendel.de/leben-soziales-gesundheit/gesundheitsamt/informationen-zum-coronavirus#c3084')
print()
print()

print('Today (check link to see when it was last updated):')
print(tod)
print('Sachsen')
st = 'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/Sachsen/data/Sachsen_Staedte_for_rankings_'
todsa = to.strftime('%Y-%m-%d')
try:
  df = pd.read_csv(f'{st}{todsa}.csv',index_col=0)
  print(f'data from {tod}')
  print(df)
except:
  print('Error for Sachsen')
print('https://www.coronavirus.sachsen.de/infektionsfaelle-in-sachsen-4151.html?_cp=%7B%22accordion-content-8665%22%3A%7B%220%22%3Atrue%2C%225%22%3Atrue%2C%226%22%3Atrue%2C%227%22%3Atrue%2C%228%22%3Atrue%2C%229%22%3Atrue%7D%2C%22accordion-content-9123%22%3A%7B%220%22%3Atrue%7D%2C%22previousOpen%22%3A%7B%22group%22%3A%22accordion-content-8665%22%2C%22idx%22%3A0%7D%7D#a-9070')
print()
print()

df = pd.read_csv(f'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Aachen/data/Aachen_{tod}.csv',index_col= 0)
print('Today:')
print(tod)
print('Aachen')
print(df[-8:])
print('https://aachen.de/DE/stadt_buerger/notfall_informationen/corona/aktuelles/index.html')
print()
print()

df = pd.read_csv(f'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Borken/data/Borken_{tod}.csv',index_col= 0)
print('Today:')
print(tod)
print('Borken')
df['Diff'] = df[df.columns[0]]-df[df.columns[1]]
print(df)
print('https://corona.kreis-borken.de/')
print()
print()

print('Today (if weekend expect last weekday):')
print(tod)
print('Coesfeld')
st = 'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Coesfeld/data/Coesfeld_'
try:
  df = pd.read_csv(f'{st}{tod}.csv',index_col=0)
  print(f'data from {tod}')
  print(df)
  df1 = pd.read_csv(f'{st}{yes}.csv',index_col=0)
  print(f'data from {yes}')
  print(df1)
  print(df[df.columns[0]]-df1[df1.columns[0]])
except:
  print('no new data for Coesfeld')
  try:
    df = pd.read_csv(f'{st}{yes}.csv',index_col=0)
    print(f'data from {yes}')
    print(df)
    df1 = pd.read_csv(f'{st}{yes2}.csv',index_col=0)
    print(f'data from {yes2}')
    print(df1)
    print(df[df.columns[0]]-df1[df1.columns[0]])
  except:
    try:
      df1 = pd.read_csv(f'{st}{yes3}.csv',index_col=0)
      print(f'data from {yes3}')
      print(df1)
      print(df[df.columns[0]]-df1[df1.columns[0]])
    except:
      print(f'no new data for Coesfeld at least since {yes3}')
print('https://kvc.maps.arcgis.com/apps/dashboards/3c68f54a38674775bc6133fdea01309c')
print()
print()

print('Today:')
print(tod)
print('Dueren')
st = 'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Dueren/data/Dueren_'
try:
  df = pd.read_csv(f'{st}{tod}.csv',index_col=0)
  print(f'data from {tod}')
  print(df)
  df1 = pd.read_csv(f'{st}{yes}.csv',index_col=0)
  print(f'data from {yes}')
  print(df1)
  print(df[df.columns[0]]-df1[df1.columns[0]])
except:
  print('no new data for Dueren')
  try:
    df = pd.read_csv(f'{st}{yes}.csv',index_col=0)
    print(f'data from {yes}')
    print(df)
    df1 = pd.read_csv(f'{st}{yes2}.csv',index_col=0)
    print(f'data from {yes2}')
    print(df1)
    print(df[df.columns[0]]-df1[df1.columns[0]])
  except:
    print(f'no new data for Dueren at least since {yes2}')
print('https://experience.arcgis.com/experience/3cea0537042b42c0bc4e53becc2d963f')
print()
print()

print('Today (if weekend expect last weekday):')
print(tod)
print('Ennepe Ruhr Kreis')
st = 'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/ERK/data/ERK_'
try:
  df = pd.read_csv(f'{st}{tod}.csv',index_col=0)
  print(f'data from {tod}')
  print(df)
  df1 = pd.read_csv(f'{st}{yes}.csv',index_col=0)
  print(f'data from {yes}')
  print(df1)
  print(df[df.columns[0]]-df1[df1.columns[0]])
except:
  print('no new data for ERK')
  try:
    df = pd.read_csv(f'{st}{yes}.csv',index_col=0)
    print(f'data from {yes}')
    print(df)
    df1 = pd.read_csv(f'{st}{yes2}.csv',index_col=0)
    print(f'data from {yes2}')
    print(df1)
    print(df[df.columns[0]]-df1[df1.columns[0]])
  except:
    try:
      df1 = pd.read_csv(f'{st}{yes3}.csv',index_col=0)
      print(f'data from {yes3}')
      print(df1)
      print(df[df.columns[0]]-df1[df1.columns[0]])
    except:
      print(f'no new data for ERK at least since {yes3}')
print('https://www.enkreis.de/gesundheitsoziales/gesundheit/faq-corona/zahlen-und-statistiken.html')
print()
print()

df = pd.read_csv(f'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Guetersloh/data/Guetersloh_{tod}.csv',index_col= 0)
print('Today:')
print(tod)
print('Guetersloh')
print(df[-20:])
print('https://www.kreis-guetersloh.de/aktuelles/corona/')
print()
print()

df = pd.read_csv(f'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Heinsberg/data/LK_Heinsberg_neu.csv',index_col= 0)
print('Today:')
print(tod)
print('Heinsberg')
print(df[df.columns[0:4]])
print('https://www.gangelt.de/news/226-erster-corona-fall-in-nrw')
print()
print()

print('Today:')
print(tod)
print('Hochsauerlandkreis')
st = 'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Hochsauerlandkreis/data/Hochsauerlandkreis_'
try:
  df = pd.read_csv(f'{st}{tod}.csv',index_col=0)
  print(f'data from {tod}')
  print(df)
  df1 = pd.read_csv(f'{st}{yes}.csv',index_col=0)
  print(f'data from {yes}')
  print(df1)
  print(df[df.columns[0]]-df1[df1.columns[0]])
except:
  print('no new data for HSK')
  try:
    df = pd.read_csv(f'{st}{yes}.csv',index_col=0)
    print(f'data from {yes}')
    print(df)
    df1 = pd.read_csv(f'{st}{yes2}.csv',index_col=0)
    print(f'data from {yes2}')
    print(df1)
    print(df[df.columns[0]]-df1[df1.columns[0]])
  except:
    print(f'no new data for HSK at least since {yes2}')
print('https://www.hochsauerlandkreis.de/regionale-themen/corona-aktuell')
print()
print()

print('Today:')
print(tod)
print('Hoexter')
st = 'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Hoexter/data/H%C3%B6xter_'
try:
  df = pd.read_csv(f'{st}{tod}.csv',index_col=0)
  print(f'data from {tod}')
  print(df)
  df1 = pd.read_csv(f'{st}{yes}.csv',index_col=0)
  print(f'data from {yes}')
  print(df1)
  print(df[df.columns[0]]-df1[df1.columns[0]])
except:
  print('no new data for Hoexter')
  try:
    df = pd.read_csv(f'{st}{yes}.csv',index_col=0)
    print(f'data from {yes}')
    print(df)
    df1 = pd.read_csv(f'{st}{yes2}.csv',index_col=0)
    print(f'data from {yes2}')
    print(df1)
    print(df[df.columns[0]]-df1[df1.columns[0]])
  except:
    print(f'no new data for Hoexter at least since {yes2}')
print('https://www.radiohochstift.de/nachrichten/infos-zum-coronavirus/corona-aktuell-zahlen-fuer-den-kreis-hoexter.html')
print()
print()

print('Today (if Sat expect last weekday):')
print(tod)
print('Kleve')
st = 'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Kleve/data/Kleve_'
try:
  df = pd.read_csv(f'{st}{tod}.csv',index_col=0)
  print(f'data from {tod}')
  print(df)
  df1 = pd.read_csv(f'{st}{yes}.csv',index_col=0)
  print(f'data from {yes}')
  print(df1)
  print(df[df.columns[0]]-df1[df1.columns[0]])
except:
  try:
    df = pd.read_csv(f'{st}{yes}.csv',index_col=0)
    print(f'data from {yes}')
    print(df)
    df1 = pd.read_csv(f'{st}{yes2}.csv',index_col=0)
    print(f'data from {yes2}')
    print(df1)
    print(df[df.columns[0]]-df1[df1.columns[0]])
  except:
    try:
      df1 = pd.read_csv(f'{st}{yes2}.csv',index_col=0)
      print(f'data from {yes2}')
      print(df1)
      print(df[df.columns[0]]-df1[df1.columns[0]])
    except:
      print(f'no new data for Kleve at least since {yes2}')
print('https://www.goch.de/de/aktuelles/corona/')
print()
print()

print('Today:')
print(tod)
print('Lippe')
st = 'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Lippe/data/Lippe_'
try:
  df = pd.read_csv(f'{st}{tod}.csv',index_col=0)
  print(f'data from {tod}')
  print(df)
  df1 = pd.read_csv(f'{st}{yes}.csv',index_col=0)
  print(f'data from {yes}')
  print(df1)
  print(df[df.columns[0]]-df1[df1.columns[0]])
except:
  print('no new data for Lippe')
  try:
    df = pd.read_csv(f'{st}{yes}.csv',index_col=0)
    print(f'data from {yes}')
    print(df)
    df1 = pd.read_csv(f'{st}{yes2}.csv',index_col=0)
    print(f'data from {yes2}')
    print(df1)
    print(df[df.columns[0]]-df1[df1.columns[0]])
  except:
    print(f'no new data for Lippe at least since {yes2}')
print('https://experience.arcgis.com/experience/154464700ab6436da13e1558ff8293f9')
print()
print()

df = pd.read_csv(f'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/MK/data/M%C3%A4rkischer_Kreis_{tod}.csv',index_col= 0)
print('Today:')
print(tod)
print('Maerkischer Kreis')
print(f'data from {tod}')
print(df)
df = pd.read_csv(f'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/MK/data/M%C3%A4rkischer_Kreis_{yes}.csv',index_col= 0)
print(f'data from {yes}')
print(df)
print('https://experience.arcgis.com/experience/a5e50d7a402e4c28bec3fe6e7ca9a05e/page/page_0/')
print()
print()

print('Today:')
print(tod)
print('Mettmann')
st = 'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Mettmann/data/Mettmann_'
try:
  df = pd.read_csv(f'{st}{tod}.csv',index_col=0)
  print(f'data from {tod}')
  print(df)
  df1 = pd.read_csv(f'{st}{yes}.csv',index_col=0)
  print(f'data from {yes}')
  print(df1)
  print(df[df.columns[0]]-df1[df1.columns[0]])
except:
  print('no new data for Mettmann')
  try:
    df = pd.read_csv(f'{st}{yes}.csv',index_col=0)
    print(f'data from {yes}')
    print(df)
    df1 = pd.read_csv(f'{st}{yes2}.csv',index_col=0)
    print(f'data from {yes2}')
    print(df1)
    print(df[df.columns[0]]-df1[df1.columns[0]])
  except:
    print(f'no new data for Mettmann at least since {yes2}')
print('https://www.kreis-mettmann-corona.de/Aktuelle-Meldungen/')
print()
print()

print('Today:')
print(tod)
print('Minden-Luebbecke')
st = 'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Minden-Luebbecke/data/Minden-L%C3%BCbbecke_'
try:
  df = pd.read_csv(f'{st}{tod}.csv',index_col=0)
  print(f'data from {tod}')
  print(df)
  df1 = pd.read_csv(f'{st}{yes}.csv',index_col=0)
  print(f'data from {yes}')
  print(df1)
  print(df[df.columns[0]]-df1[df1.columns[0]])
except:
  print('no new data for ML')
  try:
    df = pd.read_csv(f'{st}{yes}.csv',index_col=0)
    print(f'data from {yes}')
    print(df)
    df1 = pd.read_csv(f'{st}{yes2}.csv',index_col=0)
    print(f'data from {yes2}')
    print(df1)
    print(df[df.columns[0]]-df1[df1.columns[0]])
  except:
    print(f'no new data for ML at least since {yes2}')
print('https://www.radiowestfalica.de/nachrichten/corona-kreis-minden-luebbecke/zahlen.html')
print()
print()

df = pd.read_csv(f'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Olpe/data/Olpe_{tod}.csv',index_col= 0)
print('Today:')
print(tod)
print('Olpe')
print(f'data from {tod}')
print(df)
df = pd.read_csv(f'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Olpe/data/Olpe_{yes}.csv',index_col= 0)
print(f'data from {yes}')
print(df)
print('https://www.kreis-olpe.de/Themen/Coronavirus/Corona-Virus-Alle-Infos-auf-einen-Blick/')
print()
print()

df = pd.read_csv(f'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Paderborn/data/Paderborn_new_{tod}.csv',index_col= 0)
print('Today:')
print(tod)
print('Paderborn')
print(f'data from {tod}')
print(df)
print('https://www.kreis-paderborn.de/kreis_paderborn/aktuelles/pressemitteilungen/Informationen-zu-Coronaviren.php?pageId8a6517e4=41')
print()
print()

df = pd.read_csv(f'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Recklinghausen/data/Recklinghausen_{tod}.csv',index_col= 0)
print('Today:')
print(tod)
print('Recklinghausen')
print(f'data from {tod}')
print(df)
df = pd.read_csv(f'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Recklinghausen/data/Recklinghausen_{yes}.csv',index_col= 0)
print(f'data from {yes}')
print(df)
print('https://infogram.com/1prlze1gwz52zkfg2105gzn9yecm3z5vrgn')
print()
print()

print('Today (if Sunday expect Saturday):')
print(tod)
print('Rhein-Erft-Kreis')
st = 'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/REK/data/Rhein-Erft-Kreis_'
try:
  df = pd.read_csv(f'{st}{tod}.csv',index_col=0)
  print(f'data from {tod}')
  print(df)
  df1 = pd.read_csv(f'{st}{yes}.csv',index_col=0)
  print(f'data from {yes}')
  print(df1)
  print(df[df.columns[0]]-df1[df1.columns[0]])
except:
  try:
    df = pd.read_csv(f'{st}{yes}.csv',index_col=0)
    print(f'data from {yes}')
    print(df)
    df1 = pd.read_csv(f'{st}{yes2}.csv',index_col=0)
    print(f'data from {yes2}')
    print(df1)
    print(df[df.columns[0]]-df1[df1.columns[0]])
  except:
    try:
      df1 = pd.read_csv(f'{st}{yes2}.csv',index_col=0)
      print(f'data from {yes2}')
      print(df1)
      print(df[df.columns[0]]-df1[df1.columns[0]])
    except:
      print(f'no new data for REK at least since {yes2}')
print('https://www.arcgis.com/apps/dashboards/6bd759ccf569448182e9551134183300')
print()
print()

print('Today:')
print(tod)
print('Rheinisch-Bergischer Kreis')
st = 'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/RBK/data/Rheinisch-Bergischer-Kreis_'
try:
  df = pd.read_csv(f'{st}{tod}.csv',index_col=0)
  print(f'data from {tod}')
  print(df)
  df1 = pd.read_csv(f'{st}{yes}.csv',index_col=0)
  print(f'data from {yes}')
  print(df1)
  print(df[df.columns[0]]-df1[df1.columns[0]])
except:
  print('no new data for RBK')
  try:
    df = pd.read_csv(f'{st}{yes}.csv',index_col=0)
    print(f'data from {yes}')
    print(df)
    df1 = pd.read_csv(f'{st}{yes2}.csv',index_col=0)
    print(f'data from {yes2}')
    print(df1)
    print(df[df.columns[0]]-df1[df1.columns[0]])
  except:
    print(f'no new data for RBK at least since {yes2}')
print('https://rbk-direkt.maps.arcgis.com/apps/dashboards/252af02201ee4a70bf4190b339731eee')
print()
print()

print('Today:')
print(tod)
print('Rhein-Kreis-Neuss')
st = 'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/RKN/data/Rhein-Kreis-Neuss_'
try:
  df = pd.read_csv(f'{st}{tod}.csv',index_col=0)
  print(f'data from {tod}')
  print(df)
  df1 = pd.read_csv(f'{st}{yes}.csv',index_col=0)
  print(f'data from {yes}')
  print(df1)
  print(df[df.columns[0]]-df1[df1.columns[0]])
except:
  print('no new data for RKN')
  try:
    df = pd.read_csv(f'{st}{yes}.csv',index_col=0)
    print(f'data from {yes}')
    print(df)
    df1 = pd.read_csv(f'{st}{yes2}.csv',index_col=0)
    print(f'data from {yes2}')
    print(df1)
    print(df[df.columns[0]]-df1[df1.columns[0]])
  except:
    print(f'no new data for RKN at least since {yes2}')
print('https://www.status-neuss.de/IndexDashboard?dashboardID=VerteilungPostleitzahlen')
print()
print()

print('Today:')
print(tod)
print('Rhein-Sieg-Kreis')
st = 'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/RSK/data/Rhein-Sieg-Kreis_'
try:
  df = pd.read_csv(f'{st}{tod}.csv',index_col=0)
  print(f'data from {tod}')
  print(df)
  df1 = pd.read_csv(f'{st}{yes}.csv',index_col=0)
  print(f'data from {yes}')
  print(df1)
  print(df[df.columns[0]]-df1[df1.columns[0]])
except:
  print('no new data for RSK')
  try:
    df = pd.read_csv(f'{st}{yes}.csv',index_col=0)
    print(f'data from {yes}')
    print(df)
    df1 = pd.read_csv(f'{st}{yes2}.csv',index_col=0)
    print(f'data from {yes2}')
    print(df1)
    print(df[df.columns[0]]-df1[df1.columns[0]])
  except:
    print(f'no new data for RSK at least since {yes2}')
print('https://civitec.maps.arcgis.com/apps/dashboards/0453cba02245458e869241f4070a4393')
print()
print()

df = pd.read_csv('https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/SW/data/Siegen-Wittgenstein_cur.csv',index_col=0)
print('Today(if Sunday, expect 0):')
print(tod)
print('Siegen-Wittgenstein')
print(df[df.columns[0:4]])
print('https://www.siegen-wittgenstein.de/Kreisverwaltung/Themen-und-Projekte/Coronavirus/index.php?&object=tx,3417.5&ModID=255&FID=3415.784.1&kat=&kuo=1&call=0&k_sub=0&La=1')
print()
print()

print('Today (if weekend expect last weekday):')
print(tod)
print('Soest')
st = 'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Soest/data/Soest_'
try:
  df = pd.read_csv(f'{st}{tod}.csv',index_col=0)
  print(f'data from {tod}')
  print(df)
  df1 = pd.read_csv(f'{st}{yes}.csv',index_col=0)
  print(f'data from {yes}')
  print(df1)
  print(df[df.columns[0]]-df1[df1.columns[0]])
except:
  try:
    df = pd.read_csv(f'{st}{yes}.csv',index_col=0)
    print(f'data from {yes}')
    print(df)
    df1 = pd.read_csv(f'{st}{yes2}.csv',index_col=0)
    print(f'data from {yes2}')
    print(df1)
    print(df[df.columns[0]]-df1[df1.columns[0]])
  except:
    try:
      df = pd.read_csv(f'{st}{yes3}.csv',index_col=0)
      print(f'data from {yes3}')
      print(df)
    except:
      print(f'no new data for Soest at least since {yes3}')
print('https://gis.kreis-soest.de/portal/apps/opsdashboard/index.html#/b171ef41df51456593d459884d33344b')
print()
print()

print('Today (if weekend expect last weekday):')
print(tod)
print('Stadtkreise')
st = 'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/SKs/data/SKs_'
try:
  df = pd.read_csv(f'{st}{tod}.csv',index_col=0)
  print(f'data from {tod}')
  print(df)
  df1 = pd.read_csv(f'{st}{yes}.csv',index_col=0)
  print(f'data from {yes}')
  print(df1)
  print(df[df.columns[4]]-df1[df1.columns[4]])
except:
  try:
    df = pd.read_csv(f'{st}{yes}.csv',index_col=0)
    print(f'data from {yes}')
    print(df)
    df1 = pd.read_csv(f'{st}{yes2}.csv',index_col=0)
    print(f'data from {yes2}')
    print(df1)
    print(df[df.columns[4]]-df1[df1.columns[4]])
  except:
    try:
      df = pd.read_csv(f'{st}{yes3}.csv',index_col=0)
      print(f'data from {yes3}')
      print(df)
    except:
      print(f'no new data for SKs at least since {yes3}')
print('https://vbrunsch.github.io/rankings/Germany.html')
print()
print()

df = pd.read_csv(f'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Steinfurt/data/Steinfurt_{tod}.csv',index_col= 0)
print('Today:')
print(tod)
print('Steinfurt')
df['Diff'] = df[df.columns[0]]-df[df.columns[1]]
print(df)
print('https://kreis-steinfurt.maps.arcgis.com/apps/opsdashboard/index.html#/3f73221d4b384791b9a52c7327b72151')
print()
print()


print('Today (if weekend expect last weekday):')
print(tod)
print('Unna')
try:
  df = pd.read_csv(f'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Unna/data/Unna_{tod}.csv',index_col= 0)
  print(df)
except:
  try:
    df = pd.read_csv(f'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Unna/data/Unna_{yes}.csv',index_col= 0)
    print(df)
  except:
    try:
      df = pd.read_csv(f'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Unna/data/Unna_{yes2}.csv',index_col= 0)
      print(df)
    except:
      print(f'No new data for Unna since at least {yes3}')
print('https://www.kreis-unna.de/nachrichten/n/update-coronavirus-1/')
print()
print()

print('Today (if weekend expect last weekday):')
print(tod)
print('Viersen')
st = 'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Viersen/data/Viersen_'
try:
  df = pd.read_csv(f'{st}{tod}.csv',index_col=0)
  print(f'data from {tod}')
  print(df)
  df1 = pd.read_csv(f'{st}{yes}.csv',index_col=0)
  print(f'data from {yes}')
  print(df1)
  print(df[df.columns[0]]-df1[df1.columns[0]])
except:
  try:
    df = pd.read_csv(f'{st}{yes}.csv',index_col=0)
    print(f'data from {yes}')
    print(df)
    df1 = pd.read_csv(f'{st}{yes2}.csv',index_col=0)
    print(f'data from {yes2}')
    print(df1)
    print(df[df.columns[0]]-df1[df1.columns[0]])
  except:
    try:
      df = pd.read_csv(f'{st}{yes3}.csv',index_col=0)
      print(f'data from {yes3}')
      print(df)
    except:
      print(f'no new data for Viersen at least since {yes3}')
print('https://www.presse-service.de/meldungen.aspx?ps_id=1381')
print()
print()

print('Today (if Saturday expect last weekday):')
print(tod)
print('Warendorf')
st = 'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Warendorf/data/Warendorf_'
try:
  df = pd.read_csv(f'{st}{tod}.csv',index_col=0)
  print(f'data from {tod}')
  print(df)
  df1 = pd.read_csv(f'{st}{yes}.csv',index_col=0)
  print(f'data from {yes}')
  print(df1)
  print(df[df.columns[0]]-df1[df1.columns[0]])
except:
  try:
    df = pd.read_csv(f'{st}{yes}.csv',index_col=0)
    print(f'data from {yes}')
    print(df)
    df1 = pd.read_csv(f'{st}{yes2}.csv',index_col=0)
    print(f'data from {yes2}')
    print(df1)
    print(df[df.columns[0]]-df1[df1.columns[0]])
  except:
    try:
      df1 = pd.read_csv(f'{st}{yes2}.csv',index_col=0)
      print(f'data from {yes2}')
      print(df1)
      print(df[df.columns[0]]-df1[df1.columns[0]])
    except:
      print(f'no new data for Warendorf at least since {yes2}')
print('https://www.radiowaf.de/nachrichten/infos-zum-coronavirus/corona-aktuell-zahlen-im-kreis-warendorf.html')
print()
print()

print('Today (if weekend expect last weekday):')
print(tod)
print('Wesel')
st = 'https://raw.githubusercontent.com/vbrunsch/rankings/main/Germany/NRW/Wesel/data/Wesel_'
try:
  df = pd.read_csv(f'{st}{tod}.csv',index_col=0)
  print(f'data from {tod}')
  print(df)
  df1 = pd.read_csv(f'{st}{yes}.csv',index_col=0)
  print(f'data from {yes}')
  print(df1)
  print(df[df.columns[0]]-df1[df1.columns[0]])
except:
  try:
    df = pd.read_csv(f'{st}{yes}.csv',index_col=0)
    print(f'data from {yes}')
    print(df)
    df1 = pd.read_csv(f'{st}{yes2}.csv',index_col=0)
    print(f'data from {yes2}')
    print(df1)
    print(df[df.columns[0]]-df1[df1.columns[0]])
  except:
    try:
      df = pd.read_csv(f'{st}{yes3}.csv',index_col=0)
      print(f'data from {yes3}')
      print(df)
    except:
      print(f'no new data for Wesel at least since {yes3}')    
print('https://www.kreis-wesel.de/de/inhalt/presse/')
print('Pdfs:')
print('https://www.kreis-wesel.de/de/themen/corona-fallzahlen/')
print()
print()
