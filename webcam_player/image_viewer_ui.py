import sys
import numpy as np
from collections import deque
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import (Qt, QUrl, QTimer, QRect)
from PyQt5.QtGui import (QStandardItemModel, QStandardItem, QPixmap, QImage )
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
                               QPushButton, QComboBox, QCheckBox, QLabel, QSpinBox, QLineEdit, QListView,
                               QLCDNumber, QSlider, QTableWidget, QTableWidgetItem, QAction, QFileDialog,
                               QGroupBox, QScrollArea, QSizePolicy, QGraphicsScene, QGraphicsPixmapItem
                             )
from PyQt5.QtQuickWidgets import QQuickWidget

class UI_MainWindow(object):
    def setupUi(self, mainwindow):
        mainwindow.setObjectName("MainWindow")

        ### UI
        self.initUI(mainwindow)
        self.mainUI(mainwindow)
        self.videoUI(mainwindow)
        self.imageUI(mainwindow)
        self.playUI(mainwindow)

    def initUI(self, mainwindow):
        self.gb_setting_video = QGroupBox("Video Setting")
        self.gb_display_frame = QGroupBox("Video Frame")
        self.gb_recode_frame = QGroupBox("Record Frame")

    def mainUI(self, mainwindow):
        ### main
        mainframe = QWidget()
        grid = QGridLayout()
        grid.addWidget(self.gb_setting_video, 0, 0, 1, 2)
        grid.addWidget(self.gb_display_frame, 1, 0)
        grid.addWidget(self.gb_recode_frame, 1, 1)
        mainframe.setLayout(grid)
        mainwindow.setCentralWidget(mainframe)

    def playUI(self, mainwindow):

        hbox =QHBoxLayout()
        btn_set = QPushButton("Parameter Set")
        btn_set.clicked.connect(mainwindow.videoSet)
        btn_start = QPushButton("Play")
        btn_start.clicked.connect(mainwindow.videoStart)
        btn_stop = QPushButton("Stop")
        btn_stop.clicked.connect(mainwindow.videoStop)
        btn_test = QPushButton("Test")
        btn_test.clicked.connect(mainwindow.videoTest)

        hbox.addWidget(btn_set)
        hbox.addWidget(btn_start)
        hbox.addWidget(btn_stop)
        hbox.addWidget(btn_test)

        vbox = QVBoxLayout()
        scrollArea_image = QScrollArea()
        mainwindow.lbl_image2 = QLabel()
        mainwindow.lbl_image2.setFixedSize(640, 460)
        scrollArea_image.setWidget(mainwindow.lbl_image2)

        vbox.addLayout(hbox)
        vbox.addWidget(scrollArea_image)
        self.gb_recode_frame.setLayout(vbox)

    def imageUI(self, mainwindow):

        hbox =QHBoxLayout()
        btn_set = QPushButton("Parameter Set")
        btn_set.clicked.connect(mainwindow.videoSet)
        btn_start = QPushButton("Play")
        btn_start.clicked.connect(mainwindow.videoStart)
        btn_stop = QPushButton("Stop")
        btn_stop.clicked.connect(mainwindow.videoStop)
        btn_test = QPushButton("Test")
        btn_test.clicked.connect(mainwindow.videoTest)

        hbox.addWidget(btn_set)
        hbox.addWidget(btn_start)
        hbox.addWidget(btn_stop)
        hbox.addWidget(btn_test)

        vbox = QVBoxLayout()
        scrollArea_image = QScrollArea()
        mainwindow.lbl_image = QLabel()
        mainwindow.lbl_image.setFixedSize(640, 460)
        scrollArea_image.setWidget(mainwindow.lbl_image)

        vbox.addLayout(hbox)
        vbox.addWidget(scrollArea_image)
        self.gb_display_frame.setLayout(vbox)
        
    def videoUI(self, mainwindow):

        self.ledit_vURL = QLineEdit()
        lbl_vURL = QLabel("Select Video URL:")
        lbl_vURL.setFixedWidth(150)
        self.combobox_vURL = QComboBox()
        self.btn_run = QPushButton("Connect")
        self.btn_run.setFixedWidth(150)
        lbl_rMode = QLabel("Recording Mode")
        self.sb_recordingMode = QSpinBox()
        self.sb_recordingMode.setRange(-1, 1)
        self.sb_recordingMode.setValue(-1)

        self.cb_data_mode = QComboBox()

        self.cb_resize = QCheckBox('Resize')
        self.cb_resize.setFixedWidth(150)
        self.sb_width = QSpinBox()
        self.sb_width.setRange(10, 9000)
        self.sb_width.setValue(640)
        self.sb_height = QSpinBox()
        self.sb_height.setRange(10, 9000)
        self.sb_height.setValue(480)
        lbl_x = QLabel(" x ")
        lbl_x.setAlignment(Qt.AlignCenter)
        self.cb_imgproc = QCheckBox('Image Processing')

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.btn_run)
        hbox1.addWidget(self.ledit_vURL)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(lbl_vURL)
        hbox2.addWidget(self.combobox_vURL)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.cb_resize)
        hbox3.addWidget(self.sb_width)
        hbox3.addWidget(lbl_x)
        hbox3.addWidget(self.sb_height)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(lbl_rMode)
        hbox4.addWidget(self.sb_recordingMode)

        hbox5 = QHBoxLayout()
        hbox5.addWidget(self.cb_imgproc)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.cb_data_mode)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)

        self.gb_setting_video.setLayout(vbox)