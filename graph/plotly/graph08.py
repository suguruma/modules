# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 07:31:32 2017

@author: Terada
"""

import plotly.offline as offline
import plotly.figure_factory as ff

import numpy as np

# 距離は今回適当に作ります．
X = np.random.rand(10, 10)
names = ['Jack', 'Oxana', 'John', 'Chelsea', 'Mark', 'Alice', 'Charlie', 'Rob', 'Lisa', 'Lily']

fig = ff.create_dendrogram(X, orientation='left', labels=names)

# figのタイトルや画像のサイズの定義
fig["layout"].update({"title":"dendrograms example", 'width':800, 'height':800})

"""
Note

figは辞書型です．

import plotly.graph_objs as go
layout = go.Layout(title="dendrograms example")
fig["layout"] = layout

などとすることでタイトルを記入できますが，こうすると軸がめちゃくちゃになってしまいます．

これは create_dendrogram のメソッド内でlayoutを最初から整えてくれているからです．
上のように代入してしまうと，layoutが初期化されてしまうわけですね．

以上のことから，
基本的にはfigure_factoryを扱う際は，
updateを使い，自分の定義したいものだけ加えていくのが最善だと思います．
"""

offline.plot(fig, filename='dendrogram_with_labels', image="png")
