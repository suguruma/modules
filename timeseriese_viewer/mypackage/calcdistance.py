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

# DTW + diffparts
# Median + selectionModel
class CalcTimeserieseDistance():
    def __init__(self, parent=None):
        self.distanceList = []
    def main(self):
        pass

    def setNum(self, num):
        self.distanceList.append(num)
    def getNum(self):
        return self.distanceList

    def generateLabel(self, randnum):
        from numpy.random import rand, randn
        n = (rand(randnum) + 0.5)
        return n

if __name__ == "__main__":

    ctd = CalcTimeserieseDistance()
    n = ctd.generateLabel(100)
    for i in range(100):
        ctd.setNum(n[i])
    print(ctd.getNum())