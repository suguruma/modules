# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 07:24:09 2017

@author: Terada
"""

import plotly.offline as offline
import plotly.graph_objs as go
offline.init_notebook_mode()

import numpy as np

x1 = np.random.randn(500)
x2 = np.random.randn(500) + 1
trace1 = go.Histogram(
        x = x1,
        name = "data1",
        marker = dict(color='#FFD7E9'),
        opacity = 0.75
)
trace2 = go.Histogram(
        x = x2,
        name = "data2",
        marker = dict(color='#EB89B5'),
        opacity = 0.75
)

layout = go.Layout(
    title = "two histograms",
    xaxis = dict(title="value"),
    yaxis = dict(title="Count"),
    bargap=0.2, # barの間隔を指定します
    bargroupgap=0.1
)

fig = dict(data=[trace1, trace2], layout=layout)

offline.plot(fig, filename='basic histogram', image="png")