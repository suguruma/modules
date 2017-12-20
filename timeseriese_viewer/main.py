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

from mypackage.plotdisplay import MainPlotWindow
from mypackage.qmldisplay_test import QMLWindow
from mypackage.subdisplay_test import FeaturesWindow
from mypackage.calcactivity import KeyActivityTime
from mypackage.timedisplay import OperatingTimeWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        ### Setting Graph
        self.th_x = 0.5
        self.th_x_variance = 0.2
        self.th_x_max = self.th_x + self.th_x_variance
        self.th_x_min = self.th_x - self.th_x_variance
        self.th_y = 0.5
        self.th_y_variance = 0.2
        self.th_y_max = self.th_y + self.th_y_variance
        self.th_y_min = self.th_y - self.th_y_variance
        self.th_z = 0.5
        self.th_z_variance = 0.2
        self.th_z_max = self.th_z + self.th_z_variance
        self.th_z_min = self.th_z - self.th_z_variance

        ### Setting Main Window
        self.skip_header = True
        self.runOn = False
        self.fval = None
        self.loop_connnect_timer = QTimer(self)
        self.parts_dict = { "SpineBase":0, "SpineMid":1, "Neck":2, "Head":3,
                            "ShoulderLeft":4, "ElbowLeft":5, "WristLeft":6, "HandLeft":7,
                            "ShoulderRight":8, "ElbowRight":9, "WristRight":10, "HandRight":11,
                            "SpineShoulder":12, "HandTipLeft":13, "HandTipRight":14
        }
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_figure)
        self.initUI()

        ### Activity Parameter
        self.flagKeyActiveX = False
        self.flagKeyActiveY = False
        self.flagKeyActiveZ = False

        ### Key Acitivity
        self.keyfunc = KeyActivityTime()
        self.timeWindow = OperatingTimeWindow()
        self.timeWindow.show()

        ### Check Features
        self.featuresWindow = FeaturesWindow()

    def initUI(self):
        self.setWindowTitle('Time Seriese Analysis ver.0.1')
        main_frame = QWidget()
        self.main_plot = MainPlotWindow(main_frame)

        ### set Slider for refresh
        upinlabel = QLabel()
        upinlabel.setText('Update Interval:')
        mslabel = QLabel()
        mslabel.setText('msec')
        lcd = QLCDNumber(self)
        lcd.display(30)
        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setRange(1, 1000)
        self.sld.setValue(30)
        self.sld.setFixedWidth(300)
        self.sld.setTickPosition(QSlider.TicksBothSides)
        self.sld.valueChanged.connect(lcd.display)

        ### set Spinbox
        pltnum_label = QLabel()
        pltnum_label.setText('Plot Num:')
        self.pltnum_qsb = QSpinBox()
        self.pltnum_qsb.setRange(10, 9999)
        self.pltnum_qsb.setValue(300)
        self.pltnum_sld = QSlider(Qt.Horizontal, self)
        self.pltnum_sld.setRange(10, 1000)
        self.pltnum_sld.setValue(300)
        self.pltnum_sld.setFixedWidth(300)
        self.pltnum_sld.valueChanged.connect(self.refreshGraphSpinBox)
        self.pltnum_qsb.valueChanged.connect(self.refreshGraphSlider)

        ### set Button, TextBox
        self.pnameQle = QLineEdit(self)
        self.pnameQle.setText("NPtest")
        pnlabel = QLabel()
        pnlabel.setText('Pipe Name:')
        registBtn = QPushButton("Register")
        registBtn.clicked.connect(self.regist_namedpipe)
        self.regist_namedpipe()

        ###
        self.sldv1 = QSlider(Qt.Vertical, self)
        self.sldv1.setRange(1, 200)
        self.sldv1.setValue(1)
        self.sldv1.setFixedHeight(200)
        self.sldv1qsb = QSpinBox()
        self.sldv1qsb.setRange(1, 9999)
        self.sldv1qsb.setValue(self.sldv1.value())
        self.sldv1.valueChanged.connect(self.refreshGraphSpinBox)
        self.sldv1qsb.valueChanged.connect(self.refreshGraphSlider)
        self.sldv2 = QSlider(Qt.Vertical, self)
        self.sldv2.setRange(-200, 0)
        self.sldv2.setValue(-1)
        self.sldv2.setFixedHeight(200)
        self.sldv2qsb = QSpinBox()
        self.sldv2qsb.setRange(-9999, 0)
        self.sldv2qsb.setValue(self.sldv2.value())
        self.sldv2.valueChanged.connect(self.refreshGraphSpinBox)
        self.sldv2qsb.valueChanged.connect(self.refreshGraphSlider)

        ### display graph
        self.framelabel = QLabel()
        self.framelabel.setText("Frame:{0}".format(0))
        restopBtn = QPushButton("Stop | Restart")
        restopBtn.clicked.connect(self.process_stop_restart)
        refreshBtn = QPushButton("Refresh")
        refreshBtn.clicked.connect(self.update_plot_data)

        self.combo = QComboBox(self)
        self.combo.addItem("SpineBase")
        self.combo.addItem("HandLeft")
        self.combo.addItem("HandRight")
        self.combo.addItem("ShoulderLeft")
        self.combo.addItem("ShoulderRight")
        self.combo.addItem("Head")
        self.combo.addItem("SpineMid")
        self.combo.addItem("Neck")
        self.combo.addItem("ElbowLeft")
        self.combo.addItem("WristLeft")
        self.combo.addItem("ElbowRight")
        self.combo.addItem("WristRight")
        self.combo.addItem("SpineShoulder")
        self.combo.addItem("HandTipLeft")
        self.combo.addItem("HandTipRight")
        self.combo.currentTextChanged.connect(self.update_plot_data)

        self.cbx = QCheckBox('X', self)
        self.cby = QCheckBox('Y', self)
        self.cbz = QCheckBox('Z', self)
        self.cbx.toggle()
        self.cby.toggle()
        self.cbz.toggle()
        self.grid_cb = QCheckBox('Grid', self)
        self.grid_cb.toggle()
        self.loop_connnect_cb = QCheckBox('Loop', self)
        self.loop_connnect_cb.stateChanged.connect(self.loop_connect_namedpipe)

        ###
        self.sldh1 = QSlider(Qt.Horizontal, self)
        self.sldh1.setRange(-10, 1000)
        self.sldh1.setValue(0)
        self.sldh1qsb = QSpinBox()
        self.sldh1qsb.setRange(-100, 9999)
        self.sldh1qsb.setValue(self.sldh1.value())
        self.sldh1.valueChanged.connect(self.refreshGraphSpinBox)
        self.sldh1qsb.valueChanged.connect(self.refreshGraphSlider)
        self.sldh2 = QSlider(Qt.Horizontal, self)
        self.sldh2.setRange(1, 1000)
        self.sldh2.setValue(150)
        self.sldh2qsb = QSpinBox()
        self.sldh2qsb.setRange(1, 9999)
        self.sldh2qsb.setValue(self.sldh2.value())
        self.sldh2.valueChanged.connect(self.refreshGraphSpinBox)
        self.sldh2qsb.valueChanged.connect(self.refreshGraphSlider)
        self.autoScrollqb = QCheckBox('Auto', self)
        self.autoScrollLabel = QLabel()
        self.autoScrollLabel.setText('Span:')
        self.autoScrollSpanNum_qsb = QSpinBox()
        self.autoScrollSpanNum_qsb.setRange(10, 1000)
        self.autoScrollSpanNum_qsb.setValue(100)

        ### display frame image
        self.lbl_image = QLabel(self)
        #self.lbl_image.setPixmap(QPixmap("./data/bg.jpg"))
        self.frameNumbSpb = QSpinBox()
        self.frameNumbSpb.setRange(0, 9999)
        self.frameNumbSpb.setValue(0)
        self.frameNumbSpb.valueChanged.connect(self.updateWrapper)

        ### set file layout
        self.fnameQle = QLineEdit(self)
        self.fnameQle.setText("data.csv")
        self.openfile_Btn = QPushButton('Open File')
        self.openfile_Btn.clicked.connect(self.open_file)
        self.openfolder_Btn = QPushButton('Open Folder')
        self.openfolder_Btn.clicked.connect(self.open_folder)
        self.fextQle = QLineEdit(self)
        self.fextQle.setText("csv")
        self.fextQle.setFixedWidth(75)
        setFileBtn = QPushButton("Set File")
        setFileBtn.clicked.connect(self.setfile_from_filelist)

        self.qlistview = QListView(self)
        self.qlw_model = QStandardItemModel(self)
        self.qlistview.setModel(self.qlw_model)

        hbox0 = QHBoxLayout()
        hbox0.addWidget(self.openfile_Btn)
        hbox0.addWidget(self.fnameQle)

        hbox01 = QHBoxLayout()
        vbox_hbox01 = QVBoxLayout()
        vbox_hbox01.addWidget(self.openfolder_Btn)
        vbox_hbox01.addWidget(self.fextQle)
        vbox_hbox01.addWidget(setFileBtn)
        hbox01.addLayout(vbox_hbox01)
        hbox01.addWidget(self.qlistview)

        ### threshold set UI
        self.th_sldv_baseX_qsb = QSpinBox()
        self.th_sldv_baseX_qsb.setRange(1, 1000)
        self.th_sldv_baseX_qsb.setValue(20)
        self.th_sldv_baseY_qsb = QSpinBox()
        self.th_sldv_baseY_qsb.setRange(1, 1000)
        self.th_sldv_baseY_qsb.setValue(20)
        self.th_sldv_baseZ_qsb = QSpinBox()
        self.th_sldv_baseZ_qsb.setRange(1, 1000)
        self.th_sldv_baseZ_qsb.setValue(20)

        self.th_sldvX = QSlider(Qt.Vertical, self)
        self.th_sldvX.setRange(-50, 50)
        self.th_sldvX.setValue(0)
        self.th_sldvXqsb = QSpinBox()
        self.th_sldvXqsb.setRange(-50, 50)
        self.th_sldvXqsb.setValue(self.th_sldvX.value())
        self.th_sldvX.valueChanged.connect(self.setGraphParameter)
        self.th_sldvX.valueChanged.connect(self.refreshGraphSlider)

        self.th_sldvY = QSlider(Qt.Vertical, self)
        self.th_sldvY.setRange(-50, 50)
        self.th_sldvY.setValue(0)
        self.th_sldvYqsb = QSpinBox()
        self.th_sldvYqsb.setRange(-50, 50)
        self.th_sldvYqsb.setValue(self.th_sldvY.value())
        self.th_sldvY.valueChanged.connect(self.setGraphParameter)
        self.th_sldvY.valueChanged.connect(self.refreshGraphSlider)

        self.th_sldvZ = QSlider(Qt.Vertical, self)
        self.th_sldvZ.setRange(-50, 50)
        self.th_sldvZ.setValue(0)
        self.th_sldvZqsb = QSpinBox()
        self.th_sldvZqsb.setRange(-50, 50)
        self.th_sldvZqsb.setValue(self.th_sldvZ.value())
        self.th_sldvZ.valueChanged.connect(self.setGraphParameter)
        self.th_sldvZ.valueChanged.connect(self.refreshGraphSlider)

        ###
        self.th_varianceXqsb = QSpinBox()
        self.th_varianceXqsb.setRange(0, 1000)
        self.th_varianceXqsb.valueChanged.connect(self.refreshGraphSpinBox)
        self.th_varianceYqsb = QSpinBox()
        self.th_varianceYqsb.setRange(0, 1000)
        self.th_varianceYqsb.valueChanged.connect(self.refreshGraphSpinBox)
        self.th_varianceZqsb = QSpinBox()
        self.th_varianceZqsb.setRange(0, 1000)
        self.th_varianceZqsb.valueChanged.connect(self.refreshGraphSpinBox)

        ### set layout
        hbox1 = QHBoxLayout()
        hbox1.addWidget(upinlabel)
        hbox1.addWidget(lcd)
        hbox1.addWidget(mslabel)
        hbox1.addWidget(self.sld)
        hbox1.addStretch(1)
        hbox1.addWidget(registBtn)
        hbox1.addWidget(pnlabel)
        hbox1.addWidget(self.pnameQle)

        ### set Layout2
        hbox2 = QHBoxLayout()
        hbox2.addWidget(restopBtn)
        hbox2.addWidget(self.framelabel)
        hbox2.addWidget(self.frameNumbSpb)
        hbox2.addStretch(1)
        hbox2.addWidget(self.grid_cb)
        hbox2.addWidget(self.loop_connnect_cb)
        hbox2.addStretch(1)
        hbox2.addWidget(pltnum_label)
        hbox2.addWidget(self.pltnum_sld)
        hbox2.addWidget(self.pltnum_qsb)
        hbox2.addWidget(refreshBtn)
        hbox2.addWidget(self.combo)
        hbox2.addWidget(self.cbx)
        hbox2.addWidget(self.cby)
        hbox2.addWidget(self.cbz)

        ### set Layout3
        hbox3 = QHBoxLayout()

        ## set image
        hbox3.addWidget(self.lbl_image)

        hbox3_vbox = QVBoxLayout()
        hbox3_vbox.addWidget(self.sldv1)
        hbox3_vbox.addWidget(self.sldv1qsb)
        hbox3_vbox.addStretch(1)
        hbox3_vbox.addWidget(self.sldv2qsb)
        hbox3_vbox.addWidget(self.sldv2)

        ## set threshold param
        hbox3.addLayout(hbox3_vbox)
        hbox3.addWidget(self.main_plot.canvas, 10)
        hbox3_th = QHBoxLayout()
        hbox3_vbox_th1 = QVBoxLayout()
        hbox3_vbox_th1.addWidget(self.th_sldvXqsb)
        hbox3_vbox_th1.addWidget(self.th_sldvX)
        hbox3_vbox_th1.addWidget(self.th_sldv_baseX_qsb)
        hbox3_vbox_th1.addWidget(self.th_varianceXqsb)
        hbox3_th.addLayout(hbox3_vbox_th1)
        hbox3_vbox_th2 = QVBoxLayout()
        hbox3_vbox_th2.addWidget(self.th_sldvYqsb)
        hbox3_vbox_th2.addWidget(self.th_sldvY)
        hbox3_vbox_th2.addWidget(self.th_sldv_baseY_qsb)
        hbox3_vbox_th2.addWidget(self.th_varianceYqsb)
        hbox3_th.addLayout(hbox3_vbox_th2)
        hbox3_vbox_th3 = QVBoxLayout()
        hbox3_vbox_th3.addWidget(self.th_sldvZqsb)
        hbox3_vbox_th3.addWidget(self.th_sldvZ)
        hbox3_vbox_th3.addWidget(self.th_sldv_baseZ_qsb)
        hbox3_vbox_th3.addWidget(self.th_varianceZqsb)
        hbox3_th.addLayout(hbox3_vbox_th3)
        hbox3.addLayout(hbox3_th)

        ### set Layout4
        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.sldh1)
        hbox4.addWidget(self.sldh1qsb)
        hbox4.addWidget(self.autoScrollLabel)
        hbox4.addWidget(self.autoScrollSpanNum_qsb)
        hbox4.addWidget(self.autoScrollqb)
        hbox4.addWidget(self.sldh2qsb)
        hbox4.addWidget(self.sldh2)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox0)
        vbox.addLayout(hbox01)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3, 10)
        vbox.addLayout(hbox4)
        main_frame.setLayout(vbox)

        ### set widget
        self.setCentralWidget(main_frame)

        ### set UI
        self.exitActionUI()
        self.readActionUI()
        self.connectActionUI()
        self.opensubWindowActionUI()
        self.openQMLWindowActionUI()

        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.exitAction)
        menubar.addMenu('&Run')
        menubar.addMenu('&Tool')
        menubar.addMenu('&Window')
        menubar.addMenu('&Help')

        toolbar = self.addToolBar('MainToolBar')
        toolbar.addAction(self.readAction)
        toolbar.addAction(self.connectAction)
        toolbar.addAction(self.openwindowAction)
        toolbar.addAction(self.openQMLAction)

    ### ################
    def exitActionUI(self):
        self.exitAction = QAction('Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(self.close)

    def readActionUI(self):
        self.readAction = QAction('Start', self)
        self.readAction.setShortcut('Ctrl+S')
        self.readAction.setStatusTip('Start to read the data from the text file')
        self.readAction.triggered.connect(self.read_csvfile)

    def connectActionUI(self):
        self.connectAction = QAction('Connect', self)
        self.connectAction.setShortcut('Ctrl+C')
        self.connectAction.setStatusTip('Connect to get the data by the NamedPipes from other application')
        self.connectAction.triggered.connect(self.connect_namedpipe)

    def opensubWindowActionUI(self):
        self.openwindowAction= QAction('Display', self)
        self.openwindowAction.setShortcut('Ctrl+W')
        self.openwindowAction.setStatusTip('Open the table window of features')
        self.openwindowAction.triggered.connect(self.open_subwindow)

    def openQMLWindowActionUI(self):
        self.openQMLAction= QAction('QML', self)
        self.openQMLAction.setShortcut('Ctrl+M')
        self.openQMLAction.setStatusTip('QML')
        self.openQMLAction.triggered.connect(self.open_qmlwindow)

    def declareCommonVal(self):
        self.counter = 0
        self.fval = deque([])
        self.imglist = deque([])
        self.keyfunc.initFrameLabel()

    ### namedpipe
    def regist_namedpipe(self):
        self.pname = self.pnameQle.text()

    def connect_namedpipe(self):
        if self.runOn:
            return 0
        if self.setting_pipename(self.pname) > 0:
            self.declareCommonVal()
            self.timer.start(self.sld.value()) #(ms)

    def loop_connect_namedpipe(self):
        if self.loop_connnect_cb.checkState():
            self.loop_connnect_timer.timeout.connect(self.connect_namedpipe)
            self.loop_connnect_timer.start(1000)
        else:
            self.loop_connnect_timer.stop()

    def setting_pipename(self, pname):
        try:
            self.f = open(r'\\.\pipe\\' + pname, 'r+b', 0)
            self.flagOfDecode = True
            if self.skip_header:
                next(self.f)
            #print("Connect:{0}".format(pname))
            return 1
        except:
            #print("Not Connect:{0}".format(pname))
            return -1

    ### text
    def read_csvfile(self):
        if self.runOn:
            return 0
        if self.setting_textname(self.fnameQle.text()) > 0:
            #print("Start: Data Analysis ...")
            self.declareCommonVal()
            self.getFrameImages()
            self.timer.start(self.sld.value()) #(ms)

    # set frame images
    def getFrameImages(self):
        str_path = self.fnameQle.text()
        str_path = str_path.replace("coordinate", "img").split('.csv')[0]
        self.imageFolder = str_path + "/*"

        import glob
        import re
        def numericalSort(value):
            numbers = re.compile(r'(\d+)')
            parts = numbers.split(value)
            parts[1::2] = map(int, parts[1::2])
            return parts

        files = sorted(glob.glob(self.imageFolder), key=numericalSort)
        for filename in files:
            self.imglist.append(filename)

    def setting_textname(self, fname):
        try:
            self.f = open(fname, 'r')
            self.flagOfDecode = False

            if self.skip_header:
                next(self.f)

            #print("Connect:{0}".format(fname))
            return 1
        except:
            #print("Not Connect:{0}".format(fname))
            return -1

    def process_stop_restart(self):
        if self.runOn:
            self.timer.stop()
            self.runOn = self.timer.isActive()
        else:
            self.timer.start()
            self.runOn = self.timer.isActive()

    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', '.') #, os.path.expanduser('~') + '/Desktop')
        self.fnameQle.setText(filename[0])

    def open_folder(self):
        foldername = QFileDialog.getExistingDirectory(self, 'Open Directory', '.') #, os.path.expanduser('~') + '/Desktop')
        self.qlw_model.clear()

        import glob
        path = foldername + '\\' + '*' + self.fextQle.text()  #'C:\Python35\\*.txt'
        files = glob.glob(path)
        for filename in files:
            self.qlw_model.appendRow(QStandardItem(filename))

    def setfile_from_filelist(self):
        idx = self.qlistview.selectionModel().currentIndex()
        item = self.qlw_model.itemFromIndex(idx)
        self.fnameQle.setText(item.text())

    ### window refresh
    def refreshGraphSpinBox(self):
        self.sldv1qsb.setValue(self.sldv1.value())
        self.sldv2qsb.setValue(self.sldv2.value())
        self.sldh1qsb.setValue(self.sldh1.value())
        self.sldh2qsb.setValue(self.sldh2.value())
        self.pltnum_qsb.setValue(self.pltnum_sld.value())
        if not self.runOn:
            self.update_plot_data()

    def refreshGraphSlider(self):
        self.sldv1.setValue(self.sldv1qsb.value())
        self.sldv2.setValue(self.sldv2qsb.value())
        self.sldh1.setValue(self.sldh1qsb.value())
        self.sldh2.setValue(self.sldh2qsb.value())
        self.pltnum_sld.setValue(self.pltnum_qsb.value())
        if not self.runOn:
            self.update_plot_data()

    def autoScrollMode(self):
        if self.autoScrollqb.isChecked():
            self.sldh1.setValue(len(self.fval)-self.autoScrollSpanNum_qsb.value())
            self.sldh2.setValue(len(self.fval))

    def setGraphParameter(self):
        self.th_sldvXqsb.setValue(self.th_sldvX.value())
        self.th_sldvYqsb.setValue(self.th_sldvY.value())
        self.th_sldvZqsb.setValue(self.th_sldvZ.value())

    #### new form
    def open_subwindow(self):
        self.featuresWindow.show()

    ### QML
    def open_qmlwindow(self):
        QMLform = QMLWindow(self)
        QMLform.show()

    def calcActivityStatus(self):
        self.flagKeyActiveX = not self.cbx.checkState()
        self.flagKeyActiveY = not self.cby.checkState()
        self.flagKeyActiveZ = not self.cbz.checkState()
        num = len(self.x) - 1
        if self.th_x_min <= self.y1[num] and self.y1[num] <= self.th_x_max:
            self.flagKeyActiveX = True
        if self.th_y_min <= self.y2[num] and self.y2[num] <= self.th_y_max:
            self.flagKeyActiveY = True
        if self.th_z_min <= self.y3[num] and self.y3[num] <= self.th_z_max:
            self.flagKeyActiveZ = True

        if self.flagKeyActiveX and self.flagKeyActiveY and self.flagKeyActiveZ:
            self.keyfunc.setFrameLabel(1) #"key")
            #print("Key Frame:{0}".format(self.counter))
        else:
            self.keyfunc.setFrameLabel(0) # "main")
            #print("Main Frame:{0}".format(self.counter))

    ### graph update
    def update_figure(self):
        self.counter += 1
        self.update_data()
        self.update_plot_data()
        self.runOn = self.timer.isActive()

        if not self.runOn:
            #print("Analysis End")
            self.keyfunc.FPS = self.timeWindow.fpsSb.value()
            self.keyfunc.displayLabel()
            self.timeWindow.calcOprTimeLabel.setText("{0:.2f}".format(self.keyfunc.mainActivityTime))
            self.timeWindow.calcDifferenceOperatingTime()

    def updateTargetData(self):
        self.x = np.arange(len(self.fval))
        fvalT = np.array(self.fval).T
        self.y1 = fvalT[0 + 3 * self.parts_dict[self.combo.currentText()]]
        self.y2 = fvalT[1 + 3 * self.parts_dict[self.combo.currentText()]]
        self.y3 = fvalT[2 + 3 * self.parts_dict[self.combo.currentText()]]
        self.th_x = self.th_sldvXqsb.value() / self.th_sldv_baseX_qsb.value()
        self.th_y = self.th_sldvYqsb.value() / self.th_sldv_baseY_qsb.value()
        self.th_z = self.th_sldvZqsb.value() / self.th_sldv_baseZ_qsb.value()
        self.th_x_variance = self.th_varianceXqsb.value() / self.th_sldv_baseX_qsb.value()
        self.th_x_max = self.th_x + self.th_x_variance
        self.th_x_min = self.th_x - self.th_x_variance
        self.th_y_variance = self.th_varianceYqsb.value() / self.th_sldv_baseY_qsb.value()
        self.th_y_max = self.th_y + self.th_y_variance
        self.th_y_min = self.th_y - self.th_y_variance
        self.th_z_variance = self.th_varianceZqsb.value() / self.th_sldv_baseZ_qsb.value()
        self.th_z_max = self.th_z + self.th_z_variance
        self.th_z_min = self.th_z - self.th_z_variance

    def update_plot_data(self):
        self.updateTargetData()
        self.autoScrollMode()
        self.main_plot.x = self.x
        self.main_plot.y1 = self.y1
        self.main_plot.y2 = self.y2
        self.main_plot.y3 = self.y3
        self.main_plot.display_x = self.cbx.checkState()
        self.main_plot.display_y = self.cby.checkState()
        self.main_plot.display_z = self.cbz.checkState()
        self.main_plot.xlim_min = self.sldh1.value()
        self.main_plot.xlim_max = self.sldh2.value()
        self.main_plot.ylim_max = self.sldv1qsb.value()
        self.main_plot.ylim_min = self.sldv2qsb.value()
        self.main_plot.grid_flag = self.grid_cb.checkState()
        self.main_plot.th_x = self.th_x
        self.main_plot.th_x_max = self.th_x_max
        self.main_plot.th_x_min = self.th_x_min
        self.main_plot.th_y = self.th_y
        self.main_plot.th_y_max = self.th_y_max
        self.main_plot.th_y_min = self.th_y_min
        self.main_plot.th_z = self.th_z
        self.main_plot.th_z_max = self.th_z_max
        self.main_plot.th_z_min = self.th_z_min
        self.main_plot.current_x = self.frameNumbSpb.value()
        self.updateImage()
        self.calcActivityStatus()
        self.main_plot.draw()

    def updateImage(self):
        if self.frameNumbSpb.value() < len(self.imglist):
            self.lbl_image.setPixmap(QPixmap(self.imglist[self.frameNumbSpb.value()]))

    def updateWrapper(self):
        if not self.runOn and 0 < self.counter - 1:
            self.update_plot_data()

    def skip_space_csv(self, str_data):
        for i in range(len(str_data)):
            if len(str_data[i]) == 0:
                str_data[i] = np.nan
        return str_data

    def update_data(self):
        try:
            s = self.f.readline()
            proc_on = True
        except:
            proc_on = False
            self.f.close()
            self.timer.stop()
            #print("Can't get the data")
        finally:
            pass

        if(proc_on):
            ## decode flag
            if(self.flagOfDecode):
                str_data = s.decode('utf-8').split('\r\n')[0]
            else:
                str_data = s.split('\n')[0];

            if str_data == '':
                self.timer.stop() #タイマーを起動させ続けると動作が重くなるため注意
                self.f.close()
            else:
                features = str_data.split(',')
                features = self.skip_space_csv(features)
                features = np.array(features).astype(np.float64)

                self.fval.append(features)

                if self.counter - 1 > self.pltnum_qsb.value():
                    self.fval.popleft()

                self.updateTargetData()
                self.frameNumbSpb.setValue(self.counter - 1)
                self.framelabel.setText("Frame:") #{0}".format(self.counter - 1))

def main(args):
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main(sys.argv)