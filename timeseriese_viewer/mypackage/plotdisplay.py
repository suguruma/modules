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
        self.display_y = True
        self.xlim_min = 0
        self.xlim_max = 100
        self.ylim_max = 50
        self.ylim_min = 0
        self.grid_flag = True
        self.th_x = 0.1
        self.th_y = 0.0
        self.th_z = -0.1
        self.th_x_max = 0
        self.th_y_max = 0
        self.th_z_max = 0
        self.th_x_min = 0
        self.th_y_min = 0
        self.th_z_min = 0
        self.current_x = 0

    def draw(self):
        self.axes.clear()
        self.axes.grid(self.grid_flag)
        self.axes.set_xlim([self.xlim_min, self.xlim_max])
        self.axes.set_ylim([self.ylim_min, self.ylim_max])
        colorlist = ["b", "g", "r", "c", "m", "y", "k", "w",
                     '#377eb8','#4daf4a', '#e41a1c', '#000000',
                     '#ff7f00', '#ffff33', '#a65628', '#f781bf']
        linestyles = ['-', '--', '-.', ':']

        if self.display_x:
            self.axes.plot(self.x, self.y1, color=colorlist[0])

            # threshold line
            self.axes.hlines(self.th_x , self.xlim_min, self.xlim_max, colorlist[8], linestyles[3])
            self.axes.hlines(self.th_x_max , self.xlim_min, self.xlim_max, colorlist[8], linestyles[1], alpha=0.5)
            self.axes.hlines(self.th_x_min , self.xlim_min, self.xlim_max, colorlist[8], linestyles[1], alpha=0.5)
        if self.display_y:
            self.axes.plot(self.x, self.y2, color=colorlist[1])
            self.axes.hlines(self.th_y , self.xlim_min, self.xlim_max, colorlist[9], linestyles[3])
            self.axes.hlines(self.th_y_max , self.xlim_min, self.xlim_max, colorlist[9], linestyles[1], alpha=0.5)
            self.axes.hlines(self.th_y_min , self.xlim_min, self.xlim_max, colorlist[9], linestyles[1], alpha=0.5)
        if self.display_z:
            self.axes.plot(self.x, self.y3, color=colorlist[2])
            self.axes.hlines(self.th_z , self.xlim_min, self.xlim_max, colorlist[10], linestyles[3])
            self.axes.hlines(self.th_z_max , self.xlim_min, self.xlim_max, colorlist[10], linestyles[1], alpha=0.5)
            self.axes.hlines(self.th_z_min , self.xlim_min, self.xlim_max, colorlist[10], linestyles[1], alpha=0.5)

        self.axes.vlines(self.current_x , self.ylim_min, self.ylim_max, colorlist[11], linestyles[0], alpha=0.7)
        self.canvas.draw()