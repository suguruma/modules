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

    def draw(self):
        self.axes.clear()
        self.axes.grid(self.grid_flag)
        self.axes.set_xlim([self.xlim_min, self.xlim_max])
        self.axes.set_ylim([self.ylim_min, self.ylim_max])
        colorlist = ["b", "g", "r", "c", "m", "y", "k", "w",
                     '#e41a1c', '#377eb8', '#4daf4a', '#984ea3',
                     '#ff7f00', '#ffff33', '#a65628', '#f781bf']

        if self.display_x:
            self.axes.plot(self.x, self.y1, color=colorlist[0])
        if self.display_y:
            self.axes.plot(self.x, self.y2, color=colorlist[1])
        if self.display_z:
            self.axes.plot(self.x, self.y3, color=colorlist[2])
        self.canvas.draw()