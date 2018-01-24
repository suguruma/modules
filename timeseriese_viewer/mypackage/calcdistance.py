#!/usr/bin/env python
import sys
import numpy as np
import numpy.linalg as ln
from collections import deque
from dtw import dtw

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

# DTW + diffparts
# Median + selectionModel

class CalcTimeserieseDistance():
    def __init__(self, parent=None):
        self.distanceList = deque([])
        self.distance = -1
        self.targetData = None
        self.modelData = None

    def setNum(self, num):
        self.distanceList.append(num)
        
    def getNum(self):
        return self.distanceList

    def generateLabel(self, randnum):
        from numpy.random import rand, randn
        n = (rand(randnum) + 0.5)
        return n

    def setTargetData(self, _targetData):
        self.targetData = _targetData

    def setModelData(self, _modelData):
        self.modelData = _modelData

    def runDTW(self):
        func = lambda x1, y1: ln.norm(x1 - y1, ord=1) #差の絶対値を関数として定義
        dist, cost, acc, path = dtw(self.targetData, self.modelData, dist=func)
        self.distance = dist
        
if __name__ == "__main__":

    from line_profiler import LineProfiler

    A = np.array([0, 3, 3, 3, 5, 5, 2, 2, 1, 1, 1, 2]).reshape(-1, 1)
    B = np.array([0, 3, 3, 5, 5, 5, 5, 5, 5, 2, 2, 2, 1, 1, 1, 1, 1]).reshape(-1, 1) 

    ctd = CalcTimeserieseDistance()
    n1 = ctd.generateLabel(300)
    n2 = ctd.generateLabel(300)   
    A = n1.reshape(-1, 1)
    B = n2.reshape(-1, 1)

    ctd.setTargetData(A)
    ctd.setModelData(B)
    ctd.runDTW()
    print(ctd.distance)
    
    prf = LineProfiler()
    prf.add_function( ctd.runDTW )
    prf.runcall( ctd.runDTW )
    prf.print_stats()
    
