# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 07:21:51 2017

@author: Terada
"""

# import plotly as offline mode
import plotly.offline as offline
import plotly.graph_objs as go
offline.init_notebook_mode()

from sklearn.datasets import load_digits
import pandas as pd
import numpy as np

# dl the digits data
digits = load_digits()

# 今回はlabelだけ使います．
label = digits.target
N = label.shape[0]
freq = np.zeros(10)

for i in range(10):
    count = N - np.count_nonzero(label - i)
    freq[i] = count

# make trace
# 棒グラフではtraceの作成にBarを用います．
trace = go.Bar(
    x = [_ for _ in range(10)],
    y = freq,
    marker = dict(color="rgba(255, 165, 0, 0.7)")) #markerでstyleを変更できます．


# define layout
layout = go.Layout(
    title = "digits",
    xaxis = dict(title="number"),
    yaxis = dict(title="number of data"),

    # annotationsを定義することで，棒グラフの頭に直接数字を表示できます．
    # ただ自分で分析する際は，マウスをホバーさせれば詳細を表示できるので，私は必要ないと思ってます．
    # 分析に用いた図を直接プレゼンに使用したいときなどはアノテーションを定義するべきだと思います．
    annotations=[
        dict(x=xi, y=yi, text=str(int(yi)), showarrow=False)
        for xi, yi in zip([_ for _ in range(10)], freq)
        ]
    )

data = [trace]

fig = dict(data=data, layout=layout)

offline.plot(fig, filename='sample-bar-digits') #, image="png"