# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 02:35:56 2017

@author: Terada
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()

def ani01():
    def plot(data):
        plt.cla()                      # 現在描写されているグラフを消去
        plt.ylim(ymin=-5, ymax=5)
        rand = np.random.randn(100)    # 100個の乱数を生成
        plt.plot(rand)            # グラフを生成
    
    animation.FuncAnimation(fig, plot, interval=100, frames=10)
    plt.show()

def ani02():
    x = np.arange(0, 10, 0.1)

    ims = []
    for a in range(50):
        y = np.sin(x - a)
        im = plt.plot(x, y, "r")
        ims.append(im)
    
    animation.ArtistAnimation(fig, ims)
    plt.show()
    
ani01()