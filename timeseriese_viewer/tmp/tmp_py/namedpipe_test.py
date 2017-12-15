# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 19:08:08 2017

@author: Terada
"""

import time
import struct


def nptest1():
    f = open(r'\\.\pipe\NPtest', 'r+b', 0)
    i = 1
    while True:
        s = 'Message[{0}]'.format(i)
        i += 1
            
        f.write(struct.pack('I', len(s)))
        f.write(s.encode('utf-8'))
        print('Wrote:', s)
    
        x = f.read(4)
        s = f.read(x[0])
        
        print('Read:', s.decode('utf-8'))
        time.sleep(2)
        
        if i > 10:
            break
        #break
    f.close()

def nptest2():
    
    f = open(r'\\.\pipe\testpipe', 'r+b', 0)
    i = 1
    while True:
        s = 'Message[{0}]'.format(i)
        i += 1
    
        f.write(struct.pack('I', len(s)) )# + s)   # Write str length and str
        f.seek(0)                               # EDIT: This is also necessary
        print ('Wrote:', len(s), s)
    
        #n = struct.unpack('I', f.read(4))[0]    # Read str length
        s = f.read(1)                           # Read str
        f.seek(0)                               # Important!!!
        print ('Read:', s)
    
        time.sleep(2)
        break
    f.close

nptest1()