from sodapy import Socrata


import os
import pandas as pd
import numpy as np
import plotly.plotly as py
from plotly.graph_objs import *
import plotly
import collections
import plotly.graph_objs as go

client = Socrata("data.cityofchicago.org", "9ugcPuahbyTpHmzfeCefy30Ni", username="haochenzou2019@u.northwestern.edu", password="320102Zhc")
metadata=client.get_metadata("cwig-ma7x")
plotly.tools.set_credentials_file(username='alextifa7', api_key='jINELDLWjEHsJLDibvbI')

socrata_token = os.environ.get("SODAPY_APPTOKEN")
results = client.get("cwig-ma7x",limit=170000)
df = pd.DataFrame.from_dict(results)
mapbox_access_token='pk.eyJ1IjoiYWxleHRpZmE3IiwiYSI6ImNqZ2x5aDR1NDF1cGgyd21qNW5kcWp0NzUifQ.5qMfl1OmJPDwIonDZergiA'
lan=[]
lon=[]
unique_name=[]
u=[]
for i in range(len(df['dba_name'])):

    if [df['dba_name'][i],df['address'][i]] in u:
        if df['results'][i]=='Fail':
            index=u.index([df['dba_name'][i],df['address'][i]])
            unique_name[index][3]+=1
        else:
            index = u.index([df['dba_name'][i], df['address'][i]])
            unique_name[index][2] += 1


    else:
        if df['results'][i]=='Fail':
            unique_name.append([df['dba_name'][i],df['address'][i],0,1])
            lan.append(df['latitude'][i])
            lon.append(df['longitude'][i])
            u.append([df['dba_name'][i],df['address'][i]])
        else:
            unique_name.append([df['dba_name'][i], df['address'][i], 1, 0])
            lan.append(df['latitude'][i])
            lon.append(df['longitude'][i])
            u.append([df['dba_name'][i], df['address'][i]])
pass_rate=[]
for item in unique_name:
    pass_rate.append(item[2]/(item[2]+item[3]))
rate_name=[]
for i in range(len(pass_rate)):
    rate_name.append(unique_name[i][0]+'   '+'Pass rate:'+str(pass_rate[i]*100)+'%')

scl = [ [0,"rgb(61, 255, 1)"],[0.35,"rgb(214, 255, 1)"],[0.5,"rgb(255, 248, 1)"],\
    [0.6,"rgb(255, 171, 1)"],[0.7,"rgb(255, 129, 1)"],[1,"rgb(290, 50, 12)"] ]


data = [dict(
    Scattermapbox(
        lat=lan,
        lon=lon,
        mode='markers',
        marker=Marker(
            size=10,
            opacity=0.8,
            reversescale=True,
            autocolorscale=False,


            colorscale = scl,
            cmin = 0,
            color = pass_rate,
            cmax = max(pass_rate),
            colorbar=dict(
                title="Inspection Passing Rate"
            )

        ),
        text=rate_name
    )
)]

layout = Layout(
    title='Inspection passing rate',

    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=41.87,
            lon=-87.62
        ),
        pitch=0,
        zoom=10
    ),
)

fig = dict(data=data, layout=layout)
py.iplot(fig, filename='Chicago Mapbox')


chain=[]
chainame=[]
for item in u:
    chain.append(item[0])

counter=collections.Counter(chain)
for item in counter.keys():
    if counter[item]>=5:
        chainame.append(item)
size_chain=[counter[item] for item in chainame]
chain_prate=[]
risk_chain=[]
for j in range(len(chainame)):
    chain_prate.append(0)

    for i in range(len(chain)):
        if chainame[j]==chain[i]:
            chain_prate[-1]+=pass_rate[i]
    chain_prate[-1]=chain_prate[-1]/size_chain[j]
# x, y, z = np.random.multivariate_normal(np.array([0,0,0]), np.eye(3), 200).transpose()
risk=[]
for item in df['risk']:
    if item == 'Risk 1 (High)':
        risk.append(1)
    elif item == 'Risk 2 (Medium)':
        risk.append(2)
    elif item == 'Risk 3 (Low)':
        risk.append(3)
for j in range(len(chainame)):
    risk_chain.append(0)

    for i in range(len(chain)):
        if chainame[j]==chain[i]:
            risk_chain[-1]+=risk[i]
    risk_chain[-1]=risk_chain[-1]/size_chain[j]

trace1 = go.Scatter3d(
    x=risk_chain,
    y=size_chain,
    z=chain_prate,
    mode='markers',
    text=chainame,
    marker=dict(
        size=[(item/max(size_chain))*200 for item in size_chain],
        line=dict(
            color='rgba(217, 217, 217, 0.14)',
            width=0.5
        ),
        color=chain_prate,
        colorscale='Viridis',
        opacity=0.8,
        cmin = 0,
        cmax = max(chain_prate),
        colorbar=dict(
                title="Passing Rate by Brand"
            )
    )

)

data2 = [trace1]
layout2 = go.Layout(
    title="Passing Rate by Brand",
    margin=dict(

        l=0,
        r=0,
        b=0,
        t=0
    )

)
fig2 = go.Figure(data=data2, layout=layout2)
py.iplot(fig2, filename='Chain Restaurant ')
