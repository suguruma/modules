import sys
import numpy as np
from collections import deque
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import (Qt, QUrl, QTimer)
from PyQt5.QtGui import (QStandardItemModel, QStandardItem)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
                               QPushButton, QComboBox, QCheckBox, QLabel, QSpinBox, QLineEdit, QListView,
                               QLCDNumber, QSlider, QTableWidget, QTableWidgetItem, QAction, QFileDialog)
from PyQt5.QtQuickWidgets import QQuickWidget

class MainPlotWindow():
    def __init__(self, parent=None):
        self.dpi = 100
        self.fig = Figure((10,5), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(parent)
        self.axes = self.fig.add_subplot(111)
        self.x = None
        self.y1 = None
        self.y2 = None
        self.y3 = None
        self.display_x = True
        self.display_y = True
        self.display_z = True
        self.display_th_x1 = False
        self.display_th_x2 = False
        self.display_th_y1 = False
        self.display_th_y2 = False
        self.display_th_z1 = False
        self.display_th_z2 = False
        self.xlim_min = 0
        self.xlim_max = 100
        self.ylim_max = 50
        self.ylim_min = 0
        self.grid_flag = True
        self.th_x1 = 0.1
        self.th_y1 = 0.0
        self.th_z1 = -0.1
        self.th_x1_max = 0
        self.th_y1_max = 0
        self.th_z1_max = 0
        self.th_x1_min = 0
        self.th_y1_min = 0
        self.th_z1_min = 0
        self.th_x2 = 0.1
        self.th_y2 = 0.0
        self.th_z2 = -0.1
        self.th_x2_max = 0
        self.th_y2_max = 0
        self.th_z2_max = 0
        self.th_x2_min = 0
        self.th_y2_min = 0
        self.th_z2_min = 0
        self.current_x = 0
        self.colorlist = ["b", "g", "r", "c", "m", "y", "k", "w",
                     '#377eb8','#4daf4a', '#e41a1c', '#000000',
                     '#000080', '#008080', '#800000', '#f781bf']
        self.linestyles = ['-', '--', '-.', ':']

    def draw(self):
        self.axes.clear()
        self.axes.grid(self.grid_flag)
        self.axes.set_xlim([self.xlim_min, self.xlim_max])
        self.axes.set_ylim([self.ylim_min, self.ylim_max])

        if self.display_x:
            self.axes.plot(self.x, self.y1, color=self.colorlist[0])
        if self.display_th_x1:
            self.axes.hlines(self.th_x1 , self.xlim_min, self.xlim_max, self.colorlist[8], self.linestyles[3])
            self.axes.hlines(self.th_x1_max , self.xlim_min, self.xlim_max, self.colorlist[8], self.linestyles[1], alpha=0.5)
            self.axes.hlines(self.th_x1_min , self.xlim_min, self.xlim_max, self.colorlist[8], self.linestyles[1], alpha=0.5)
        if self.display_th_x2:
            self.axes.hlines(self.th_x2 , self.xlim_min, self.xlim_max, self.colorlist[12], self.linestyles[3])
            self.axes.hlines(self.th_x2_max , self.xlim_min, self.xlim_max, self.colorlist[12], self.linestyles[1], alpha=0.5)
            self.axes.hlines(self.th_x2_min , self.xlim_min, self.xlim_max, self.colorlist[12], self.linestyles[1], alpha=0.5)

        if self.display_y:
            self.axes.plot(self.x, self.y2, color=self.colorlist[1])
        if self.display_th_y1:
            self.axes.hlines(self.th_y1 , self.xlim_min, self.xlim_max, self.colorlist[9], self.linestyles[3])
            self.axes.hlines(self.th_y1_max , self.xlim_min, self.xlim_max, self.colorlist[9], self.linestyles[1], alpha=0.5)
            self.axes.hlines(self.th_y1_min , self.xlim_min, self.xlim_max, self.colorlist[9], self.linestyles[1], alpha=0.5)
        if self.display_th_y2:
            self.axes.hlines(self.th_y2 , self.xlim_min, self.xlim_max, self.colorlist[13], self.linestyles[3])
            self.axes.hlines(self.th_y2_max , self.xlim_min, self.xlim_max, self.colorlist[13], self.linestyles[1], alpha=0.5)
            self.axes.hlines(self.th_y2_min , self.xlim_min, self.xlim_max, self.colorlist[13], self.linestyles[1], alpha=0.5)

        if self.display_z:
            self.axes.plot(self.x, self.y3, color=self.colorlist[2])
        if self.display_th_z1:
            self.axes.hlines(self.th_z1 , self.xlim_min, self.xlim_max, self.colorlist[10], self.linestyles[3])
            self.axes.hlines(self.th_z1_max , self.xlim_min, self.xlim_max, self.colorlist[10], self.linestyles[1], alpha=0.5)
            self.axes.hlines(self.th_z1_min , self.xlim_min, self.xlim_max, self.colorlist[10], self.linestyles[1], alpha=0.5)
        if self.display_th_z2:
            self.axes.hlines(self.th_z2 , self.xlim_min, self.xlim_max, self.colorlist[14], self.linestyles[3])
            self.axes.hlines(self.th_z2_max , self.xlim_min, self.xlim_max, self.colorlist[14], self.linestyles[1], alpha=0.5)
            self.axes.hlines(self.th_z2_min , self.xlim_min, self.xlim_max, self.colorlist[14], self.linestyles[1], alpha=0.5)
        self.axes.vlines(self.current_x , self.ylim_min, self.ylim_max, self.colorlist[11], self.linestyles[0], alpha=0.7)
        self.canvas.draw()