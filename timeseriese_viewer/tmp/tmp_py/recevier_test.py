# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 20:00:25 2017
@author: Terada
"""

import time
import numpy as np

pipename = "NPtest"

def nptest1():
    f = open(r'\\.\pipe\\' + pipename, 'r+b', 0)
    i = 0
    while True:
        try:
            s = 'Message[{0}]'.format(i)
            i += 1
        
            s = f.readline()
            str_data = s.decode('utf-8').split('\r\n')[0]            
            if str_data == '':
                break
            
            features = str_data.split(',')
            features = np.array(features)
            print("{2:3d} {0:0}:{1}".format(len(features), features[1], int(i/30) ))
            time.sleep(0.0333)
            
            
        except:
            break
    f.close()

nptest1()