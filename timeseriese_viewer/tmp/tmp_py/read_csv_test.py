# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 18:36:22 2017

@author: Terada
"""

import csv

fname = "data.csv"

f = open(fname, 'r')

reader = csv.reader(f)
header = next(reader)
for row in reader:
    print (row)

f.close()