# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 07:29:01 2017

@author: Terada
"""

# import plotly as offline mode
import plotly.offline as offline
import plotly.figure_factory as ff
offline.init_notebook_mode()

from sklearn.datasets import load_iris
import pandas as pd

iris = load_iris()
columns = ["label"] + iris.feature_names

label = iris.target.reshape([150,1])
labeled = np.hstack([label,iris.data])

# make dataframe
df = pd.DataFrame(labeled, columns=columns)

# setosaのsepal-lengthとsepal-widthを使います．
setosa = df[df["label"] == 0]

x = setosa['sepal length (cm)']
y = setosa['sepal width (cm)']

# define colorscale
colorscale = ['#7A4579', '#D56073', 'rgb(236,158,105)', (1, 1, 0.2), (0.98,0.98,0.98)]

fig = ff.create_2d_density(
    x, y, colorscale=colorscale,
    hist_color='rgb(0, 128, 222)', point_size=3,
)

offline.plot(fig, filename="2d-density", image="png")