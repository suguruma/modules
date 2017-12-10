# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 13:58:47 2017

@author: Terada
"""

import matplotlib.pyplot as plt
from sklearn import datasets

def pca():
    from sklearn.decomposition import PCA
    digits = datasets.load_digits()
    
    print(digits.data.shape)    # (1797, 64)
    print(digits.target.shape)    # (1797,)
    
    X_reduced = PCA(n_components=2).fit_transform(digits.data)
    
    print(X_reduced.shape)    # (1797, 2)
    
    plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=digits.target)
    plt.colorbar()
    
def tsne():
    
    from sklearn.manifold import TSNE
    
    digits = datasets.load_digits()
    
    print(digits.data.shape)
    print(digits.target.shape)
    
    X_reduced = TSNE(n_components=2, random_state=0).fit_transform(digits.data)
    
    print(X_reduced.shape)
    
    plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=digits.target)
    plt.colorbar()

if __name__ == "__main__":
    
    #pca()
    tsne()

    plt.show()
