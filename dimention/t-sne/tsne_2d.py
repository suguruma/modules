# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 05:35:18 2017

@author: Terada
"""

import os
import numpy as np
import cv2
from sklearn.manifold import TSNE
from sklearn import preprocessing

import plotly.offline as offline
import plotly.graph_objs as go
offline.init_notebook_mode()

# 画像の前処理．標準化やらL2正規化やら．
def preprocess_image(path, size):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    resized = cv2.resize(img, (size, size), cv2.INTER_LINEAR).astype("float")
    normalized = cv2.normalize(resized, None, 0.0, 1.0, cv2.NORM_MINMAX)
    timg = normalized.reshape(np.prod(normalized.shape))
    return timg/np.linalg.norm(timg) 

ROOT = "./data/coil-20-proc"
ls = os.listdir(ROOT)

# 名前からラベルを持って来ます．
obj_ls = [name.split("_")[0] for name in ls]

ALL_IMAGE_PATH = [ROOT+"/"+path for path in ls]

# 全画像に対して前処理する
preprocess_images_as_vecs = [preprocess_image(path, 32) for path in ALL_IMAGE_PATH]

# tsneを実行
tsne = TSNE(
    n_components=3, #ここが削減後の次元数です．
    init='random',
    random_state=101,
    method='barnes_hut',
    n_iter=1000,
    verbose=2
).fit_transform(preprocess_images_as_vecs)


trace = go.Scatter(
    x=tsne[:,0],
    y=tsne[:,1],
    mode='markers',
    marker=dict(
        sizemode='diameter',
        color = preprocessing.LabelEncoder().fit_transform(obj_ls),
        colorscale = 'Portland',
        line=dict(color='rgb(255, 255, 255)'),
        opacity=0.9,
        size=4
    )
)

data=[trace]
layout=dict(height=800, width=800, title='coil-20 tsne exmaple 2D')
fig=dict(data=data, layout=layout)
offline.iplot(fig, filename='tsne2D_example')

offline.plot(fig, filename='tsne2D_example')

