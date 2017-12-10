# -*- coding: utf-8 -*-
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import Scatter, Figure, Layout
from plotly.graph_objs import *
    
init_notebook_mode(connected=True)

def test01():
    plot([Scatter(x=[1, 2, 3], y=[3, 1, 6])])
    #iplot([{"x": [1, 2, 3], "y": [3, 1, 6]}])
    
def test02():
    import numpy as np

    x = np.random.randn(2000)
    y = np.random.randn(2000)
    plot([Histogram2dContour(x=x, y=y, contours=Contours(coloring='heatmap')),
          Scatter(x=x, y=y, mode='markers', marker=Marker(color='white', size=3, opacity=0.3))], show_link=False)

def test03():
    import cufflinks as cf
    plot(cf.datagen.lines().iplot(asFigure=True,
         kind='scatter',xTitle='Dates',yTitle='Returns',title='Returns')) #, image='png'

def test04():
    import plotly.plotly as py 
    fig = py.get_figure('https://plot.ly/~jackp/8715', raw=True)
    plot(fig)
    
def test05():
    import plotly.offline as offline
    import plotly.graph_objs as go
    
    offline.init_notebook_mode()
    offline.plot({'data': [{'y': [4, 2, 3, 4]}],'layout': {'title': 'Test Plot', 'font': dict(size=16)}},image='png')

def test06():
    import plotly.offline as offline
    import plotly.graph_objs as go

    offline.plot({'data': [{'y': [4, 2, 3, 4]}], 
                  'layout': {'title': 'Test Plot', 
                  'font': dict(size=16)}}, image='png')

test03()