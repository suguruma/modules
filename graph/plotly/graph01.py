# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 05:55:04 2017

@author: Terada
"""

# import plotly as offline mode
import plotly.offline as offline
import plotly.graph_objs as go
offline.init_notebook_mode()

from sklearn.datasets import load_iris
import pandas as pd
import numpy as np

iris = load_iris()
columns = iris.feature_names

# make dataframe
df = pd.DataFrame(iris.data, columns=columns)

# make trace
trace = go.Scatter(
    x = np.array(df[columns[0]]),
    y = np.array(df[columns[1]]),
    mode = "markers")

# define layout
layout = go.Layout(
    title='Iris sepal length-width',
    xaxis=dict(title='sepal legth(cm)'),
    yaxis=dict(title='sepal width(cm)'),
    showlegend=False)

data = [trace]
fig = dict(data=data, layout=layout)

offline.plot(fig, filename="Iris-sample-scatter", image="png")