# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 18:16:14 2017

@author: Terada
"""

from PySide import QtCore, QtGui

import matplotlib.pyplot as plt

import matplotlib
matplotlib.rcParams['backend.qt4'] = 'PySide'

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.fig = plt.Figure()
        self.graph01 = FigureCanvas(self.fig)
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)

        self.graph01.setObjectName("graph01")
        self.verticalLayout.addWidget(self.graph01)

        self.psbtn = QtGui.QPushButton(self.centralwidget)
        self.psbtn.setObjectName("psbtn")
        self.psbtn.setText("Plot")
        self.verticalLayout.addWidget(self.psbtn)
        QtCore.QObject.connect(self.psbtn, QtCore.SIGNAL("clicked()"), self.plot)

    def plot(self):
        frq1 = 10.0
        frq2 = 30.0
        frq3 = 50.0
        duration = 1.0
        samples = 1001

        x1 = np.linspace(0, duration, samples)
        rad1 = np.linspace(0, 2 * np.pi * frq1, samples)
        rad2 = np.linspace(0, 2 * np.pi * frq2, samples)
        rad3 = np.linspace(0, 2 * np.pi * frq3, samples)
        y1 = np.sin(rad1) + np.sin(rad2) + np.sin(rad3) 

        x2 = np.linspace(0,1001,1001)[0:np.floor(len(y1)/2)]
        y2 = abs(np.fft.fft(y1))[0:np.floor(len(y1)/2)]

        self.ax1.plot(x1, y1)
        self.ax2.plot(x2, y2)
        self.graph01.draw()#zettai iru

import sys
import numpy as np

class ControlMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    sys.exit(app.exec_())
