#!wget https://github.com/plotly/orca/releases/download/v1.2.1/orca-1.2.1-x86_64.AppImage -O /usr/local/bin/orca

#!chmod +x /usr/local/bin/orca

#!apt-get install xvfb libgtk2.0-0 libgconf-2-4
#!pip install kaleido

import pandas as pd
import numpy as np
#!pip install cif
from cif import cif
data = cif.createDataFrameFromOECD(countries = ['AUS','BEL','CAN','FRA','DEU','ITA','JPN','KOR','NLD','NZL','SWE','CHE','GBR','USA','EU27_2020','OECDE','OECD','IND'], dsname = 'QNA', subject = ['B1_GE'], measure = ['VPVOBARSA'], frequency = 'Q', startDate = '2018-Q4')#, endDate = '2022-Q1')

df = data[0]
df.index.name = None
df.columns = ['Australia','Belgium','Canada','France','Germany','Italy','Japan','Korea','Netherlands','New Zealand','Sweden','Switzerland','United Kingdom','United States','European Union – 27 countries (from 01/02/2020)','OECD - Europe','OECD - Total','India']
df = df.reset_index(inplace=False)
df.rename(columns = {'index':'TIME'}, inplace = True)
df = df.melt(id_vars=['TIME'])
df.columns = ['TIME','Country','Value']
df= df[['Country','TIME','Value']]
df['Value'] = df['Value']/4000000
df['PctChange'] = df['Value'].pct_change()
print(df)

d_ch = cif.createDataFrameFromOECD(countries = ['CHN'], dsname = 'QNA', subject = ['B1_GE'], measure = ['GPSA'], frequency = 'Q', startDate = '2018-Q4')#, endDate = '2022-Q1')

ch = d_ch[0]
ch.columns = ['China']
cc = []
for i in ch['China']:
  cc.append(i)
#print(cc)

# China real GDP for 2019 in million 2015 US Dollar was $19892289.6925
df.loc[len(df.index)] = ['China', '2018-Q4',4.73669583183, cc[0]/100]
df.loc[len(df.index)] = ['China', '2019-Q1',4.78406279015, cc[1]/100]
df.loc[len(df.index)] = ['China', '2019-Q2',4.84147154363, cc[2]/100]
df.loc[len(df.index)] = ['China', '2019-Q3',4.90925214524, cc[3]/100]
df.loc[len(df.index)] = ['China', '2019-Q4',19892289.6925/4000000, cc[4]/100]

tcc = ['2018-Q4','2019-Q1','2019-Q2','2019-Q3','2019-Q4','2020-Q1','2020-Q2','2020-Q3','2020-Q4','2021-Q1','2021-Q2','2021-Q3','2021-Q4','2022-Q1','2022-Q2','2022-Q3','2022-Q4','2023-Q1','2023-Q2','2023-Q3','2023-Q4','2024-Q1','2024-Q2','2024-Q3','2024-Q4','2025-Q1','2025-Q2','2025-Q3','2025-Q4','2026-Q1','2026-Q2','2026-Q3','2026-Q4','2027-Q1','2027-Q2','2027-Q3','2027-Q4','2028-Q1','2028-Q2','2028-Q3','2028-Q4','2029-Q1','2029-Q2','2029-Q3','2029-Q4','2030-Q1','2030-Q2','2030-Q3','2030-Q4']

for i in range(5,len(cc)):
  df.loc[len(df.index)] = ['China', tcc[i],df['Value'][len(df)-1]+df['Value'][len(df)-1]*cc[i]/100, cc[i]/100]

clist = ['China','Australia','Belgium','Canada','France','Germany','Italy','Japan','Korea','Netherlands','New Zealand','Sweden','Switzerland','United Kingdom','United States','European Union – 27 countries (from 01/02/2020)','OECD - Europe','OECD - Total','India']
dfl = pd.DataFrame()
dfl2 = pd.DataFrame()
import matplotlib.pyplot as plt
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
for i in clist:
  try:
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
  except:
          
      dft = df[df['Country']==i]
      rate = dft['PctChange'][1:5].mean()
      dft['SlopeVal'] = (np.arange(len(dft)) + -4)*rate*dft['Value'].iloc[4] + dft['Value'].iloc[4]
      dft2 = dft['SlopeVal'][4:]-dft['Value'][4:]
      dft2 = dft2.reset_index(drop=True)
      dft2.loc[len(dft2.index)] = np.nan
      dft3 = dft['Value'].iloc[4]-dft['Value'][4:]
      dft3 = dft3.reset_index(drop=True)
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
    layout = dict(template="simple_white", xaxis = dict(showgrid=False, ticks='outside', mirror=True,showline=True, tickformat = '%d-%b'),
                    yaxis = dict(showgrid=False, ticks='outside', mirror = True, showline = True, title = 'Quarterly GDP in trillion US$ (2015)',title_font_size = 17),
                    font=dict(size=18),showlegend = True, legend=dict(xanchor='right', x = 0.98, yanchor='bottom', y = 0.1,traceorder='reversed',font=dict(size= 10),bgcolor = 'rgba(0,0,0,0)'),
                    margin=go.layout.Margin(
                        l=0, #left margin
                        r=0, #right margin
                        b=0, #bottom margin
                        t=0  #top margin
                    ))
    fig = go.Figure(data=data, layout=layout)
    fig.add_annotation(text="European Union - 27 countries",
                  xref="paper", yref="paper",
                  x=0, y=1, showarrow=False)
    #fig.show()

    

    fig.write_html(r'EU_GDP.html',config=dict(
                  displayModeBar=False), default_height = '400px', default_width = '700px' )
    
    
    fig.write_image('EU_GDP.png')

  else:

    layout = dict(template="simple_white", xaxis = dict(showgrid=False, ticks='outside', mirror=True,showline=True, tickformat = '%d-%b'),
                    yaxis = dict(showgrid=False, ticks='outside', mirror = True, showline = True, title = 'Quarterly GDP in trillion US$ (2015)',title_font_size = 17),
                    font=dict(size=18),showlegend = True, legend=dict(xanchor='right', x = 0.98, yanchor='bottom', y = 0.1,traceorder='reversed',font=dict(size= 10),bgcolor = 'rgba(0,0,0,0)'),
                    margin=go.layout.Margin(
                        l=0, #left margin
                        r=0, #right margin
                        b=0, #bottom margin
                        t=0  #top margin
                    ))
    fig = go.Figure(data=data, layout=layout)
    fig.add_annotation(text=i,
                  xref="paper", yref="paper",
                  x=0, y=1, showarrow=False)
    #fig.show()

    

    fig.write_html(r'%s_GDP.html'%i,config=dict(
                  displayModeBar=False), default_height = '400px', default_width = '700px' )
    fig.write_image(r'%s_GDP.png'%i)

dfc = dfl.cumsum()
dfc = dfc*-1
dfc = dfc.rename(columns={"European Union – 27 countries (from 01/02/2020)":"EU (27)"})
dfc2 = dfl2.cumsum()
dfc2 = dfc2*-1
dfc2 = dfc2.rename(columns={"European Union – 27 countries (from 01/02/2020)":"EU (27)"})

layout = dict(template="simple_white", title = 'Accumulated GDP Gain/Loss with respect to 2019 growth rate', title_x = 0.5, xaxis = dict(showgrid=False, ticks='outside', mirror=True,showline=True, tickformat = '%d-%b'),
                    yaxis = dict(showgrid=False, ticks='outside', mirror = True, showline = True, title = 'Trillion US$ (2015)'),
                    font=dict(size=18),showlegend = True)#, legend=dict(xanchor='right', x = 0.98, yanchor='bottom', y = 0.1,traceorder='reversed'))

colors = px.colors.qualitative.Plotly
fig = go.Figure(layout = layout)
for i in range(0,10):
  fig.add_traces(go.Scatter(x=['2019-Q4','2020-Q1','2020-Q2','2020-Q3','2020-Q4','2021-Q1','2021-Q2','2021-Q3','2021-Q4'], y = dfc[dfc.columns[i]], mode = 'lines', name = dfc.columns[i], line=dict(color=colors[i])))
#fig.show()
fig.write_html(r'Acc_GDP_Gain_Loss_rate1.html',config=dict(
                  displayModeBar=False), default_height = '550px', default_width = '900px' )
fig.write_image(file='Acc_GDP_Gain_Loss_rate1.png')

fig = go.Figure(layout = layout)
for i in range(0,9):
  fig.add_traces(go.Scatter(x=['2019-Q4','2020-Q1','2020-Q2','2020-Q3','2020-Q4','2021-Q1','2021-Q2','2021-Q3','2021-Q4'], y = dfc[dfc.columns[i+10]], mode = 'lines', name = dfc.columns[i+10], line=dict(color=colors[i])))
#fig.show()
fig.write_html(r'Acc_GDP_Gain_Loss_rate2.html',config=dict(
                  displayModeBar=False), default_height = '550px', default_width = '900px' )
fig.write_image(file='Acc_GDP_Gain_Loss_rate2.png')

dfc2 = dfc2[['Australia','Belgium','Korea','Netherlands','New Zealand','Sweden','Switzerland','Canada','Japan','Italy','Germany','France','United Kingdom','India','China','United States','EU (27)','OECD - Europe', 'OECD - Total']]
layout = dict(template="simple_white", title = 'Accumulated GDP Loss relative to Q4 2019', title_x = 0.5, xaxis = dict(showgrid=False, ticks='outside', mirror=True,showline=True, tickformat = '%d-%b'),
                    yaxis = dict(showgrid=False, ticks='outside', mirror = True, showline = True, title = 'Trillion US$ (2015)'),
                    font=dict(size=18),showlegend = True, legend=dict(xanchor='left', x = 0, yanchor='bottom', y = 0,font=dict(size= 10),bgcolor = 'rgba(0,0,0,0)'))#,traceorder='normal'))

colors = px.colors.qualitative.G10
# marker_color = px.colors.qualitative.G10[1],line = dict(width=4, dash = 'dash'))
fig = go.Figure(layout = layout)
for i in range(0,7):
  #if i == 8:
  #  fig.add_traces(go.Scatter(x=['2019-Q4','2020-Q1','2020-Q2','2020-Q3','2020-Q4','2021-Q1','2021-Q2','2021-Q3','2021-Q4'], y = dfc2[dfc2.columns[i]], mode = 'lines', name = dfc2.columns[i], line=dict(color='black', width = 4)))  
  #else:
  fig.add_traces(go.Scatter(x=tcc[4:4+dfc2[dfc2.columns[i]].count()], y = dfc2[dfc2.columns[i]], mode = 'lines', name = dfc2.columns[i], line=dict(color=colors[i], width = 4)))
fig.show()
fig.write_html(r'Acc_GDP_Gain_Loss_Q4_1.html',config=dict(
                  displayModeBar=False), default_height = '400px', default_width = '700px' )
fig.write_image(file='Acc_GDP_Gain_Loss_Q4_1.png')

fig = go.Figure(layout = layout)
for i in range(0,6):
  #if i in [7,8,9]:
  #  fig.add_traces(go.Scatter(x=['2019-Q4','2020-Q1','2020-Q2','2020-Q3','2020-Q4','2021-Q1','2021-Q2','2021-Q3','2021-Q4'], y = dfc2[dfc2.columns[i+9]], mode = 'lines', name = dfc2.columns[i+9], line=dict(color=colors[i],width = 4, dash = 'dash')))
  #else:
  fig.add_traces(go.Scatter(x=tcc[4:4+dfc2[dfc2.columns[i+7]].count()], y = dfc2[dfc2.columns[i+7]], mode = 'lines', name = dfc2.columns[i+7], line=dict(color=colors[i],width = 4)))
fig.show()
fig.write_html(r'Acc_GDP_Gain_Loss_Q4_2.html',config=dict(
                  displayModeBar=False), default_height = '400px', default_width = '700px' )
fig.write_image(file='Acc_GDP_Gain_Loss_Q4_2.png')
fig = go.Figure(layout = layout)
for i in range(0,6):
  #if i in [7,8,9]:
  #  fig.add_traces(go.Scatter(x=['2019-Q4','2020-Q1','2020-Q2','2020-Q3','2020-Q4','2021-Q1','2021-Q2','2021-Q3','2021-Q4'], y = dfc2[dfc2.columns[i+9]], mode = 'lines', name = dfc2.columns[i+9], line=dict(color=colors[i],width = 4, dash = 'dash')))
  #else:
  fig.add_traces(go.Scatter(x=tcc[4:4+dfc2[dfc2.columns[i+13]].count()], y = dfc2[dfc2.columns[i+13]], mode = 'lines', name = dfc2.columns[i+13], line=dict(color=colors[i],width = 4)))
fig.show()
fig.write_html(r'Acc_GDP_Gain_Loss_Q4_3.html',config=dict(
                  displayModeBar=False), default_height = '400px', default_width = '700px' )
fig.write_image(file='Acc_GDP_Gain_Loss_Q4_3.png')
