import pandas as pd
import numpy as np

df = pd.read_csv('gdp/OECD_GDP_from2018Q4.csv')
df = df[['Country','TIME','Value']]
df['Value'] = df['Value']/4000000
df['PctChange'] = df['Value'].pct_change()

# China real GDP for 2019 in million 2015 US Dollar was $19892289.6925
cc = [1.5, 1, 1.2, 1.4, 1.3, -10.5, 11.6, 3.4, 2.6, 0.3, 1.3, 0.7, 1.6]

df.loc[len(df.index)] = ['China', '2018-Q4',4.73669583183, cc[0]/100]
df.loc[len(df.index)] = ['China', '2019-Q1',4.78406279015, cc[1]/100]
df.loc[len(df.index)] = ['China', '2019-Q2',4.84147154363, cc[2]/100]
df.loc[len(df.index)] = ['China', '2019-Q3',4.90925214524, cc[3]/100]
df.loc[len(df.index)] = ['China', '2019-Q4',19892289.6925/4000000, cc[4]/100]
df.loc[len(df.index)] = ['China', '2020-Q1',df['Value'][len(df)-1]+df['Value'][len(df)-1]*cc[5]/100, cc[5]/100]
df.loc[len(df.index)] = ['China', '2020-Q2',df['Value'][len(df)-1]+df['Value'][len(df)-1]*cc[6]/100, cc[6]/100]
df.loc[len(df.index)] = ['China', '2020-Q3',df['Value'][len(df)-1]+df['Value'][len(df)-1]*cc[7]/100, cc[7]/100]
df.loc[len(df.index)] = ['China', '2020-Q4',df['Value'][len(df)-1]+df['Value'][len(df)-1]*cc[8]/100, cc[8]/100]
df.loc[len(df.index)] = ['China', '2021-Q1',df['Value'][len(df)-1]+df['Value'][len(df)-1]*cc[9]/100, cc[9]/100]
df.loc[len(df.index)] = ['China', '2021-Q2',df['Value'][len(df)-1]+df['Value'][len(df)-1]*cc[10]/100, cc[10]/100]
df.loc[len(df.index)] = ['China', '2021-Q3',df['Value'][len(df)-1]+df['Value'][len(df)-1]*cc[11]/100, cc[11]/100]
df.loc[len(df.index)] = ['China', '2021-Q4',df['Value'][len(df)-1]+df['Value'][len(df)-1]*cc[12]/100, cc[12]/100]

dfl = pd.DataFrame()
dfl2 = pd.DataFrame()
import matplotlib.pyplot as plt
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
for i in df['Country'].unique():
  if i != 'New Zealand' and i!= 'OECD - Total':
    dft = df[df['Country']==i]
    rate = dft['PctChange'][1:5].mean()
    dft['SlopeVal'] = (np.arange(len(dft)) + -4)*rate*dft['Value'].iloc[4] + dft['Value'].iloc[4]
    dft2 = dft['SlopeVal'][4:]-dft['Value'][4:]
    dft3 = dft['Value'].iloc[4]-dft['Value'][4:]
    dfl[i] = dft2.values
    dfl2[i] = dft3.values
    dft = dft.set_index('TIME')
    print(rate)
    fig = plt.figure(figsize = (8,8))
    ax = dft['Value'].plot(grid=True, label="GDP in %s in trillion (2015) US$"%i, legend=True, title = i)
    plt.axhline(y=dft['Value'][4], color='g', linestyle='-')
    dft['SlopeVal'].plot(grid=True, label="2019 rate", legend=True)
  else:
    dft = df[df['Country']==i]
    rate = dft['PctChange'][1:5].mean()
    dft['SlopeVal'] = (np.arange(len(dft)) + -4)*rate*dft['Value'].iloc[4] + dft['Value'].iloc[4]
    dft2 = dft['SlopeVal'][4:]-dft['Value'][4:]
    dft2.loc[len(dft2.index)] = np.nan
    dft3 = dft['Value'].iloc[4]-dft['Value'][4:]
    dft3.loc[len(dft3.index)] = np.nan
    dfl[i] = dft2.values
    dfl2[i] = dft3.values
    dft = dft.set_index('TIME')
    print(rate)
    fig = plt.figure(figsize = (8,8))
    ax = dft['Value'].plot(grid=True, label="GDP in %s in trillion (2015) US$"%i, legend=True, title = i)
    plt.axhline(y=dft['Value'][4], color='g', linestyle='-')
    dft['SlopeVal'].plot(grid=True, label="2019 rate", legend=True)

    #ax.axline((3, 12), slope=rate, color='C0', label='2019 rate')
    #ax.set_xticklabels(df.TIME)
  gdp = go.Scatter(
      x=dft.index,
      y=dft['Value'], name = 'GDP', marker_color = px.colors.qualitative.D3[2], line = dict(width=4))
  slope = go.Scatter(
      x=dft.index,
      y=dft['SlopeVal'], name = '2019 rate', marker_color = px.colors.qualitative.G10[2],line = dict(width=4, dash = 'dash'))
  q4_2019 = go.Scatter(
      x=dft.index,
      y=np.full(len(dft.index),dft['Value'].iloc[4]), name = '2019 Q4 GDP', marker_color = px.colors.qualitative.G10[0],line = dict(width=4, dash = 'dash'))


  data = [q4_2019,slope,gdp]

  if i == 'European Union – 27 countries (from 01/02/2020)':
    layout = dict(template="simple_white", title = 'European Union - 27 countries', title_x = 0.5, xaxis = dict(showgrid=False, ticks='outside', mirror=True,showline=True, tickformat = '%d-%b'),
                    yaxis = dict(showgrid=False, ticks='outside', mirror = True, showline = True, title = 'Quarterly GDP in trillion 2015 US$'),
                    font=dict(size=18),showlegend = True, legend=dict(xanchor='right', x = 0.98, yanchor='bottom', y = 0.1,traceorder='reversed'))
    fig = go.Figure(data=data, layout=layout)
    #fig.show()

    

    fig.write_html(r'EU_GDP.html',config=dict(
                  displayModeBar=False), default_height = '550px', default_width = '900px' )

  else:

    layout = dict(template="simple_white", title = i, title_x = 0.5, xaxis = dict(showgrid=False, ticks='outside', mirror=True,showline=True, tickformat = '%d-%b'),
                    yaxis = dict(showgrid=False, ticks='outside', mirror = True, showline = True, title = 'Quarterly GDP in trillion 2015 US$'),
                    font=dict(size=18),showlegend = True, legend=dict(xanchor='right', x = 0.98, yanchor='bottom', y = 0.1,traceorder='reversed'))
    fig = go.Figure(data=data, layout=layout)
    #fig.show()

    

    fig.write_html(r'%s_GDP.html'%i,config=dict(
                  displayModeBar=False), default_height = '550px', default_width = '900px' )
