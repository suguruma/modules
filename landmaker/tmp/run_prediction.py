# -*- coding: utf-8 -*-
"""
@author: Terada
"""

import read_image as imread_mod
import read_text as txtread_mod

import numpy as np
import matplotlib.pyplot as plt
import re

from keras.models import model_from_json
    
'''
 Image, Textのファイル名チェック
 共通ファイル名のファイルパス出力
'''
def common_filename_check(_fname1, _fname2, _fname1_str = 'Image', _fname2_str = 'land', _fname1_ext = 'jpg', _fname2_ext = 'txt'):


    _1to2name = [re.sub(_fname1_str, _fname2_str, _fname1[i].split(_fname1_ext)[0]) for i in range(len(_fname1))]
    _com_name = []

    for i in range(len(_1to2name)):
        for j in range(len(_fname2)):
            if _1to2name[i] in _fname2[j]:
                _com_name.append(_1to2name[i].split(_fname2_str)[1])
                break

    iext= np.array([_fname1_ext]*len(_com_name))
    _com_fname1 = np.core.defchararray.add(_com_name, iext)
    _com_fname1 = [re.sub('^', _fname1_str, _com_fname1[i]) for i in range(len(_com_fname1))]

    text= np.array([_fname2_ext]*len(_com_name))
    _com_fname2 = np.core.defchararray.add(_com_name, text)    
    _com_fname2 = [re.sub('^', _fname2_str, _com_fname2[i]) for i in range(len(_com_fname2))]
    
    return _com_fname1, _com_fname2

def load_data(_image_path, _label_path, _io_fname, _img_size, _input_size, data_check = True):

    ## Read image
    X, _iname = imread_mod.main(_image_path, _input_size)
    #print("X.shape == {}; X.min == {:.1f}; X.max == {:.1f}".format(X.shape, X.min(), X.max()))

    ## Read text
    y, _tname = txtread_mod.main(_label_path, _io_fname, _img_size, False)
    #print("y.shape == {}; y.min == {:.3f}; y.max == {:.3f}".format(y.shape, y.min(), y.max()))

    if data_check:
        _iname, _tname = common_filename_check(_iname, _tname)        
        print("Common Files : {0}".format(len(_iname)))            
        _iname_path = []
        _tname_path = []
        for i in range(len(_iname)):
            _iname_path.append(_image_path.split('*')[0] + _iname[i])
            _tname_path.append(_label_path.split('*')[0] + _tname[i])

        X, _ = imread_mod.main(_iname_path, _input_size)
        y, _ = txtread_mod.main(_tname_path, _io_fname, _img_size, False)
   
    return X, y

'''
 y[0/1::2] : 0/1要素からスタート, 次の2つ目
'''
def plot_sample(_x, _y, _img_size):
    img = _x.reshape(_img_size[0], _img_size[1])

    half_size = _img_size.max() / 2
    
    plt.imshow(img, cmap='gray')
    plt.scatter(_y[0::2] * half_size + half_size, _y[1::2] * half_size + half_size, marker='x', s=20)

def plot_2samples(x1, y1, x2, y2, _img_size):
    img1 = x1.reshape(_img_size[0], _img_size[1])
    img2 = x2.reshape(_img_size[0], _img_size[1])

    half_size = _img_size.max() / 2

    plt.figure(figsize=(10, 6)) # figure(縦,横の大きさ)
    
    plt.subplot(1,2,1) # figure内の枠の大きさと配置:subplot(行の数,列の数,配置番目)
    plt.imshow(img1, cmap='gray')
    plt.scatter(y1[0::2] * half_size + half_size, y1[1::2] * half_size + half_size, marker='x', color='b',s=20)
        
    plt.subplot(1,2,2)
    plt.imshow(img2, cmap='gray')
    plt.scatter(y2[0::2] * half_size + half_size, y2[1::2] * half_size + half_size, marker='x', color='r', s=20)

def model_predict(_X_test, _model):
    y_test = _model.predict(_X_test)
    return y_test

def main():
    
    ## Image Data
    img_size = np.array([400, 360])  #[h, w]
    input_size = img_size / 4
    input_size = input_size.astype(np.int)
  
    ### モデル名
    model_name = 'model/mdl_ep10/mdl_ep10'
    json_name = '{0}_architecture.json'.format(model_name)
    weights_name = '{0}_weights.h5'.format(model_name)
    
    ### モデル読み込み  
    model = model_from_json(open(json_name).read())
    model.load_weights(weights_name)

    ### 予測
    ## Testing Data Path
    image_path = 'data/img3dTo2d/before/*.jpg'
    label_path = 'data/txt3dTo2d/before/*.txt'
    io_fname = 'data\label.csv'
    X_test, y_test = load_data(image_path, label_path, io_fname, img_size, input_size)
    y_predict = model_predict(X_test, model)
    No = 250
    plot_2samples(X_test[No], y_test[No], X_test[No], y_predict[No], input_size)

    plt.show()

if __name__ == "__main__":
    main()