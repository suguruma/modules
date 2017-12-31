#!/usr/bin/env python
import sys
import numpy as np
from collections import deque

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import (Qt, QUrl, QTimer)
from PyQt5.QtGui import (QStandardItemModel, QStandardItem, QPixmap)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
                               QPushButton, QComboBox, QCheckBox, QLabel, QSpinBox, QLineEdit, QListView,
                               QLCDNumber, QSlider, QTableWidget, QTableWidgetItem, QAction, QFileDialog)
from PyQt5.QtQuickWidgets import QQuickWidget

#from PyQt5.QtGui import QGuiApplication
#from PyQt5.QtCore import (QLineF, QPointF, QRectF)
#from PyQt5.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsItem, QListWidget)
#from PyQt5.QtQuick import QQuickView
#from PyQt5.QtQml import QQmlApplicationEngine

class KeyActivityTime():
    def __init__(self, parent=None):
        self.FPS = 30
        self.classLabelNum = 0
        self.classLabelID = None
        self.labelFrame = deque([])
        self.runOn = False
        self.mainActivityFrame = 0
        self.keyActivityFrame = 0

    def setFrameLabel(self, _sLabel):
        self.labelFrame.append(_sLabel)

    def initFrameLabel(self):
        self.labelFrame = deque([])

    # Local Function
    def eachClassCounter(self):
        _pastLabel = self.labelFrame[0]
        _counter = 0
        _eachClassCount = deque([])
        _eachClassLabel = deque([])

        for i in range(len(self.labelFrame)):
            if _pastLabel == self.labelFrame[i]:
                _counter += 1
            else:
                _eachClassLabel.append(_pastLabel)
                _eachClassCount.append(_counter)
                _pastLabel = self.labelFrame[i]
                _counter = 1

        _eachClassCount.append(_counter)
        _eachClassLabel.append(_pastLabel)
        return _eachClassCount, _eachClassLabel

    def displayLabel(self):
        #pandas整理
        #print(self.eachClassCounter())
        self.calcActivityTime()
        #pass
    def clasteringLabel(self, features):
        pass

    def selectClassMaxCount(self):

        ### Key Phase
        key_max_count = 0
        key_2nd_count = 0
        key_max_num = -1
        key_2nd_num = -1
        class_num = 0
        for id, labelnum in zip(self.classLabelID, self.classLabelNum):
            if id == 1 and key_max_count < labelnum:
                key_2nd_count = key_max_count
                key_max_count = labelnum
                key_2nd_num = key_max_num
                key_max_num = class_num
                #print("id:0 {0}, {1}".format(key_2nd_count, key_max_count))

            elif id == 1 and key_2nd_count < labelnum:
                key_2nd_count = labelnum
                key_2nd_num = class_num
                #print("id:1 {0}, {1}".format(key_2nd_count, key_max_count))
            class_num += 1
        #print('label id:', "class_num", "count")
        #print('label 1:', key_max_num, key_max_count)
        #print('label 1:', key_2nd_num, key_2nd_count)

        ### Main Phase
        main_max_count = 0
        main_max_num = -1
        class_num = 0
        for id, labelnum in zip(self.classLabelID, self.classLabelNum):
            if id == 0 and main_max_count < labelnum:
                if (key_2nd_num <= class_num and class_num <= key_max_num) or (key_2nd_num >= class_num and class_num >= key_max_num):
                    main_max_count = labelnum
                    main_max_num = class_num
            class_num += 1
        ## key main key
        #print('label id:', "class_num", "count")
        #print('label 0:', main_max_num, main_max_count)

        ### SetFrame
        self.mainActivityFrame = main_max_count
        self.keyActivityFrame = key_max_count

    def determineKeyFrame(self):
        self.mainActivityTime = self.mainActivityFrame / self.FPS

    def calcActivityTime(self):
        self.classLabelNum, self.classLabelID = self.eachClassCounter()
        self.selectClassMaxCount()
        self.determineKeyFrame()


def generateLabel(randnum):
    from numpy.random import rand, randn
    n = (rand(randnum) + 0.5).astype(np.int)
    return n

if __name__ == "__main__":

    keyfunc = KeyActivityTime()
    n = generateLabel(100)
    for i in range(100):
        keyfunc.setFrameLabel(1,n[i])
    keyfunc.calcActivityTime()