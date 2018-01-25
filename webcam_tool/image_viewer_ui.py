import sys
import numpy as np
from collections import deque
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import (Qt, QUrl, QTimer, QRect)
from PyQt5.QtGui import (QStandardItemModel, QStandardItem, QPixmap)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
                               QPushButton, QComboBox, QCheckBox, QLabel, QSpinBox, QLineEdit, QListView,
                               QLCDNumber, QSlider, QTableWidget, QTableWidgetItem, QAction, QFileDialog,
                               QGroupBox, QScrollArea, QSizePolicy
                             )
from PyQt5.QtQuickWidgets import QQuickWidget

class UI_MainWindow(object):
    def setupUi(self, mainwindow):
        mainwindow.setObjectName("MainWindow")

        ### UI
        self.initUI(mainwindow)
        self.mainUI(mainwindow)

    def initUI(self, mainwindow):
        pass

    def mainUI(self, mainwindow):
        ### main
        mainframe = QWidget()

        lbl_vURL = QLabel("Video URL:")
        self.ledit_vURL = QLineEdit()
        self.combobox_vURL = QComboBox()
        self.combobox_vURL.addItem("0")
        self.combobox_vURL.addItem("http://10.232.163.38/mjpg/1/video.mjpg")
        self.combobox_vURL.addItem("http://10.232.163.38/jpg/1/image.jpg")
        self.combobox_vURL.currentTextChanged.connect(self.mainUI_combobox)
        btn_run = QPushButton("Run")
        btn_run.clicked.connect(lambda : self.mainUI_btn_run(mainwindow))

        grid = QGridLayout()
        grid.addWidget(lbl_vURL, 0, 0, 1, 1)
        grid.addWidget(self.ledit_vURL, 0, 1, 1, 2)
        grid.addWidget(btn_run, 1, 0)
        grid.addWidget(self.combobox_vURL, 1, 1)

        mainframe.setLayout(grid)
        mainwindow.setCentralWidget(mainframe)

    def mainUI_combobox(self):
        self.ledit_vURL.setText(self.combobox_vURL.currentText())

    def mainUI_btn_run(self, mainwindow):
        mainwindow.cam.set_sensor(int(self.ledit_vURL.text()))
        mainwindow.cam.videoCameraView()
        print(self.ledit_vURL.text())