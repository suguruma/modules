# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 07:25:04 2017

@author: Terada
"""

import plotly.offline as offline
import plotly.graph_objs as go
offline.init_notebook_mode()

import numpy as np

x = np.random.randn(500)
y = np.random.randn(500) + 1
trace = go.Histogram2d(
        x = x,
        y = y,
        name = "data1",
        opacity = 0.75,
        colorscale="YIGnBu"
)

layout = go.Layout(
    title = "2d histograms",
    xaxis = dict(title="data1"),
    yaxis = dict(title="data2"),
)

fig = dict(data=[trace], layout=layout)

offline.plot(fig, filename='2d_histogram', image="png")