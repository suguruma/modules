# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 07:30:16 2017

@author: Terada
"""

import plotly.offline as offline
import plotly.graph_objs as go

import pandas as pd
import seaborn as sns

df = sns.load_dataset('flights')

x = df.year.unique()
y = df.month.unique()
z = df.passengers.reshape([12, 12])

# Heatmapメソッドでzに値，xとyに軸を定義します．
# colorscaleはお好みで．デフォルトは結構ダサいので注意！
data = [go.Heatmap(z=z, x=x, y=list(y), colorscale="Viridis")]
layout = go.Layout(
    title = "flight passengers",
    xaxis = dict(title="year"),
    yaxis = dict(title='')
)

fig = go.Figure(data=data, layout=layout)
offline.plot(fig, filename='labelled-heatmap', image="png")