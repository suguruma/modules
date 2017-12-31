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


class FeaturesWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Features Window')
        self.resize(640,480)
        sub_frame = QWidget()
        label = QLabel()
        label.setText('Features')
        self.table = QTableWidget()
        #table.setRowCount(10)
        #table.setColumnCount(10)
        #table.setItem(0,0, QTableWidgetItem("1"))
        #table.setItem(0,1, QTableWidgetItem("2"))
        #table.setItem(1,0, QTableWidgetItem("3"))
        #table.setItem(1,1, QTableWidgetItem("4"))

        grid = QGridLayout()
        grid.addWidget(label)
        grid.addWidget(self.table)
        sub_frame.setLayout(grid)
        self.setCentralWidget(sub_frame)
