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
from mypackage.plotdisplay import MainPlotWindow

class UI_MainWindow(object):
    def setupUi(self, mui):
        mui.setObjectName("MainWindow")

        ### UI
        self.initUI(mui)
        self.mainUI(mui)
        self.barUI(mui)
        self.readDataUI(mui)
        self.connectDataUI(mui)
        self.frameInfomationUI(mui)
        self.figureInfomationUI(mui)
        self.imageUI(mui)

    def initUI(self, mui):
        mui.gb_readData = QGroupBox()
        mui.gb_readData.setVisible(False)
        mui.gb_connectData = QGroupBox()
        mui.gb_connectData.setVisible(False)
        mui.gb_frameInfo = QGroupBox()
        mui.gb_frameInfo.setVisible(False)
        mui.gb_figureInfo = QGroupBox()
        mui.gb_figureInfo.setVisible(False)
        mui.gb_imageInfo = QGroupBox()
        mui.gb_imageInfo.setVisible(False)

    def mainUI(self, mui):
        ### main
        main_frame = QWidget()
        mui.main_plot = MainPlotWindow(main_frame)

        vbox = QVBoxLayout()
        vbox.addWidget(mui.gb_readData)
        vbox.addWidget(mui.gb_connectData)
        vbox.addWidget(mui.gb_frameInfo)
        vbox.addStretch(1)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(mui.gb_imageInfo)
        hbox1.addWidget(mui.gb_figureInfo)
        vbox.addLayout(hbox1)
        main_frame.setLayout(vbox)

        mui.setCentralWidget(main_frame)

    def barUI(self, mui):
        ### Action UI
        self.exitActionUI(mui)
        self.readActionUI(mui)
        self.connectActionUI(mui)
        self.opensubWindowActionUI(mui)
        self.openQMLWindowActionUI(mui)

        ### Add Element
        statusbar = mui.statusBar()
        menubar = mui.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(mui.exitAction)
        menubar.addMenu('&Run')
        menubar.addMenu('&Tool')
        menubar.addMenu('&Window')
        menubar.addMenu('&Help')

        toolbar = mui.addToolBar('MainToolBar')
        toolbar.addAction(mui.readAction)
        toolbar.addAction(mui.connectAction)
        toolbar.addAction(mui.openwindowAction)
        toolbar.addAction(mui.openQMLAction)

    def readDataUI(self, mui):
        ### Add Element
        mui.fnameQle = QLineEdit()
        mui.fnameQle.setText("CSV File")
        mui.openfile_Btn = QPushButton('Open File')
        mui.openfile_Btn.clicked.connect(mui.open_file)
        mui.openfolder_Btn = QPushButton('Open Folder')
        mui.openfolder_Btn.clicked.connect(mui.open_folder)
        mui.fextQle = QLineEdit()
        mui.fextQle.setText("csv")
        mui.fextQle.setFixedWidth(120)
        mui.cb_autoSelectFileOn = QCheckBox("Auto Selection")
        mui.qlistview = QListView()
        mui.qlw_model = QStandardItemModel()
        mui.qlistview.setModel(mui.qlw_model)
        mui.qlistview.clicked.connect(mui.setfile_from_filelist)
        mui.qlistview.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)

        ### -1-
        hbox1 = QHBoxLayout()
        hbox1.addWidget(mui.openfile_Btn)
        hbox1.addWidget(mui.fnameQle)

        ### |1|
        vbox_left = QVBoxLayout()
        vbox_left.addWidget(mui.openfolder_Btn)
        vbox_left.addWidget(mui.fextQle)
        vbox_left.addWidget(mui.cb_autoSelectFileOn)
        ### -2-
        hbox2 = QHBoxLayout()
        hbox2.addLayout(vbox_left)
        hbox2.addWidget(mui.qlistview)
        ### |-1-2-|
        vbox_gb_readData = QVBoxLayout()
        vbox_gb_readData.addLayout(hbox1)
        vbox_gb_readData.addLayout(hbox2)

        mui.gb_readData.setVisible(True)
        mui.gb_readData.setTitle("Read Data")
        mui.gb_readData.setLayout(vbox_gb_readData)

    def connectDataUI(self, mui):
        ### Add Element
        mui.pnameQle = QLineEdit()
        mui.pnameQle.setText("NPtest")
        pnlabel = QLabel()
        pnlabel.setText('Pipe Name:')
        registBtn = QPushButton("Register")
        registBtn.clicked.connect(mui.regist_namedpipe)
        mui.regist_namedpipe()
        mui.loop_connnect_cb = QCheckBox('Loop')
        mui.loop_connnect_cb.stateChanged.connect(mui.loop_connect_namedpipe)

        ### -1-
        hbox_gb_connectData = QHBoxLayout()
        hbox_gb_connectData.addWidget(registBtn)
        hbox_gb_connectData.addWidget(pnlabel)
        hbox_gb_connectData.addWidget(mui.pnameQle)
        hbox_gb_connectData.addWidget(mui.loop_connnect_cb)

        mui.gb_connectData.setVisible(True)
        mui.gb_connectData.setTitle("Connect Data")
        mui.gb_connectData.setLayout(hbox_gb_connectData)

    def frameInfomationUI(self, mui):
        ### Add Element
        mui.timer = QTimer()
        mui.timer.timeout.connect(mui.update_figure)
        upinlabel = QLabel()
        upinlabel.setText('Update Interval:')
        mslabel = QLabel()
        mslabel.setText('msec')
        lcd = QLCDNumber()
        lcd.display(30)
        mui.sld = QSlider(Qt.Horizontal)
        mui.sld.setRange(1, 1000)
        mui.sld.setValue(30)
        mui.sld.setSingleStep(1)
        mui.sld.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        mui.sld.setTickPosition(QSlider.TicksBothSides)
        mui.sld.valueChanged.connect(lcd.display)
        restopBtn = QPushButton("Stop | Restart")
        restopBtn.clicked.connect(mui.process_stop_restart)
        mui.framelabel = QLabel()
        mui.framelabel.setText("Frame:")
        mui.frameNumbSpb = QSpinBox()
        mui.frameNumbSpb.setRange(0, 9999)
        mui.frameNumbSpb.setValue(0)
        mui.frameNumbSpb.valueChanged.connect(mui.updateWrapper)
        mui.frameNumbSpb.valueChanged.connect(mui.refreshGraphSlider)
        mui.sld_frameNum = QSlider(Qt.Horizontal)
        mui.sld_frameNum.setRange(0, 300)
        mui.sld_frameNum.setSingleStep(1)
        mui.sld_frameNum.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        mui.sld_frameNum.valueChanged.connect(mui.refreshGraphSpinBox)
        label_maxFrame = QLabel()
        label_maxFrame.setText('Max Frame:')
        mui.pltnum_qsb = QSpinBox()
        mui.pltnum_qsb.setRange(10, 9999)
        mui.pltnum_qsb.setValue(300)
        mui.pltnum_sld = QSlider(Qt.Horizontal)
        mui.pltnum_sld.setRange(10, 1000)
        mui.pltnum_sld.setValue(300)
        mui.pltnum_sld.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        mui.pltnum_sld.valueChanged.connect(mui.refreshGraphSpinBox)
        mui.pltnum_qsb.valueChanged.connect(mui.refreshGraphSlider)
        ### -1-
        hbox1 = QHBoxLayout()
        hbox1.addWidget(upinlabel)
        hbox1.addWidget(lcd)
        hbox1.addWidget(mslabel)
        hbox1.addWidget(mui.sld)
        ### -2-
        hbox2 = QHBoxLayout()
        hbox2.addWidget(restopBtn)
        hbox2.addWidget(mui.framelabel)
        hbox2.addWidget(mui.frameNumbSpb)
        hbox2.addWidget(mui.sld_frameNum)
        ### -3-
        hbox3 = QHBoxLayout()
        hbox3.addWidget(label_maxFrame)
        hbox3.addWidget(mui.pltnum_qsb)
        hbox3.addWidget(mui.pltnum_sld)
        ### |-1-2-3-|
        vbox_gb_frameInfo = QVBoxLayout()
        vbox_gb_frameInfo.addLayout(hbox1)
        vbox_gb_frameInfo.addLayout(hbox3)
        vbox_gb_frameInfo.addLayout(hbox2)

        mui.gb_frameInfo.setVisible(True)
        mui.gb_frameInfo.setTitle("Frame Information")
        mui.gb_frameInfo.setLayout(vbox_gb_frameInfo)

    def figureInfomationUI(self, mui):
        ### Add Element
        mui.sldv1 = QSlider(Qt.Vertical)
        mui.sldv1.setRange(1, 200)
        mui.sldv1.setValue(1)
        mui.sldv1.setFixedHeight(200)
        mui.sldv1qsb = QSpinBox()
        mui.sldv1qsb.setRange(1, 9999)
        mui.sldv1qsb.setValue(mui.sldv1.value())
        mui.sldv1.valueChanged.connect(mui.refreshGraphSpinBox)
        mui.sldv1qsb.valueChanged.connect(mui.refreshGraphSlider)
        mui.sldv2 = QSlider(Qt.Vertical)
        mui.sldv2.setRange(-200, 0)
        mui.sldv2.setValue(-1)
        mui.sldv2.setFixedHeight(200)
        mui.sldv2qsb = QSpinBox()
        mui.sldv2qsb.setRange(-9999, 0)
        mui.sldv2qsb.setValue(mui.sldv2.value())
        mui.sldv2.valueChanged.connect(mui.refreshGraphSpinBox)
        mui.sldv2qsb.valueChanged.connect(mui.refreshGraphSlider)

        ### display graph
        refreshBtn = QPushButton("Refresh")
        refreshBtn.clicked.connect(mui.update_plot_data)
        mui.combo = QComboBox()
        mui.combo.addItem("SpineBase")
        mui.combo.addItem("HandLeft")
        mui.combo.addItem("HandRight")
        mui.combo.addItem("ShoulderLeft")
        mui.combo.addItem("ShoulderRight")
        mui.combo.addItem("Head")
        mui.combo.addItem("SpineMid")
        mui.combo.addItem("Neck")
        mui.combo.addItem("ElbowLeft")
        mui.combo.addItem("WristLeft")
        mui.combo.addItem("ElbowRight")
        mui.combo.addItem("WristRight")
        mui.combo.addItem("SpineShoulder")
        mui.combo.addItem("HandTipLeft")
        mui.combo.addItem("HandTipRight")
        mui.combo.currentTextChanged.connect(mui.update_plot_data)
        mui.cbx = QCheckBox('X')
        mui.cby = QCheckBox('Y')
        mui.cbz = QCheckBox('Z')
        mui.cbx.setChecked(True)
        mui.cby.setChecked(True)
        mui.cbz.setChecked(True)
        mui.cb_imgDisplay = QCheckBox('Display Image')
        mui.cb_imgDisplay.setChecked(True)
        mui.cb_imgDisplay.stateChanged.connect(mui.isDisplayImageInfomation)
        mui.grid_cb = QCheckBox('Grid')
        mui.grid_cb.setChecked(True)
        mui.cb_Animation = QCheckBox('Animation')
        mui.cb_Animation.setChecked(True)

        ###
        mui.sldh1 = QSlider(Qt.Horizontal)
        mui.sldh1.setRange(-10, 1000)
        mui.sldh1.setValue(0)
        mui.sldh1qsb = QSpinBox()
        mui.sldh1qsb.setRange(-100, 9999)
        mui.sldh1qsb.setValue(mui.sldh1.value())
        mui.sldh1.valueChanged.connect(mui.refreshGraphSpinBox)
        mui.sldh1qsb.valueChanged.connect(mui.refreshGraphSlider)
        mui.sldh2 = QSlider(Qt.Horizontal)
        mui.sldh2.setRange(1, 1000)
        mui.sldh2.setValue(150)
        mui.sldh2qsb = QSpinBox()
        mui.sldh2qsb.setRange(1, 9999)
        mui.sldh2qsb.setValue(mui.sldh2.value())
        mui.sldh2.valueChanged.connect(mui.refreshGraphSpinBox)
        mui.sldh2qsb.valueChanged.connect(mui.refreshGraphSlider)
        mui.autoScrollqb = QCheckBox('Auto')
        mui.autoScrollLabel = QLabel()
        mui.autoScrollLabel.setText('Span:')
        mui.autoScrollSpanNum_qsb = QSpinBox()
        mui.autoScrollSpanNum_qsb.setRange(10, 1000)
        mui.autoScrollSpanNum_qsb.setValue(100)
        ### -1-
        hbox1 = QHBoxLayout()
        hbox1.addWidget(mui.cb_imgDisplay)
        hbox1.addWidget(mui.cb_Animation)
        hbox1.addWidget(refreshBtn)
        hbox1.addWidget(mui.grid_cb)
        hbox1.addWidget(mui.combo)
        hbox1.addWidget(mui.cbx)
        hbox1.addWidget(mui.cby)
        hbox1.addWidget(mui.cbz)
        hbox1.addStretch(1)
        ### |1|
        vbox1 = QVBoxLayout()
        vbox1.addWidget(mui.sldv1)
        vbox1.addWidget(mui.sldv1qsb)
        vbox1.addStretch(1)
        vbox1.addWidget(mui.sldv2qsb)
        vbox1.addWidget(mui.sldv2)
        ### -2-
        hbox2 = QHBoxLayout()
        hbox2.addWidget(mui.sldh1)
        hbox2.addWidget(mui.sldh1qsb)
        hbox2.addWidget(mui.autoScrollLabel)
        hbox2.addWidget(mui.autoScrollSpanNum_qsb)
        hbox2.addWidget(mui.autoScrollqb)
        hbox2.addWidget(mui.sldh2qsb)
        hbox2.addWidget(mui.sldh2)
        ### |2-2-|
        vbox2 = QVBoxLayout()
        vbox2.addWidget(mui.main_plot.canvas, 10)
        vbox2.addLayout(hbox2)
        ### -3|1|2|-
        hbox3 = QHBoxLayout()
        hbox3.addLayout(vbox1)
        hbox3.addLayout(vbox2)
        ### |-1-3-|
        vbox_gb_figureInfo = QVBoxLayout()
        vbox_gb_figureInfo.addLayout(hbox1)
        vbox_gb_figureInfo.addLayout(hbox3)

        mui.gb_figureInfo.setVisible(True)
        mui.gb_figureInfo.setTitle("Figure Information")
        mui.gb_figureInfo.setLayout(vbox_gb_figureInfo)

    def imageUI(self, mui):
        ### Add Element
        mui.le_imgPath = QLineEdit()
        mui.le_imgPath.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        label_imgWidth = QLabel()
        label_imgWidth.setText("Width:")
        mui.spb_imgWidth = QSpinBox()
        mui.spb_imgWidth.setRange(10, 1920)
        mui.spb_imgWidth.setValue(640)
        mui.spb_imgWidth.valueChanged.connect(mui.changeImageSize)
        label_imgHeight = QLabel()
        label_imgHeight.setText("Height:")
        mui.spb_imgHeight = QSpinBox()
        mui.spb_imgHeight.setRange(10, 1680)
        mui.spb_imgHeight.setValue(480)
        mui.spb_imgHeight.valueChanged.connect(mui.changeImageSize)

        # set image display
        scrollArea_image = QScrollArea()
        mui.lbl_image = QLabel()
        mui.lbl_image.setFixedSize(mui.spb_imgWidth.value(), mui.spb_imgHeight.value())
        #mui.lbl_image.setPixmap(QPixmap("./bg.jpg"))
        scrollArea_image.setWidget(mui.lbl_image)

        ### -1-
        hbox1 = QHBoxLayout()
        hbox1.addWidget(mui.le_imgPath)
        hbox1.addWidget(label_imgWidth)
        hbox1.addWidget(mui.spb_imgWidth)
        hbox1.addWidget(label_imgHeight)
        hbox1.addWidget(mui.spb_imgHeight)

        ### |-1-|
        vbox_gb_imageInfo = QVBoxLayout()
        vbox_gb_imageInfo.addLayout(hbox1)
        vbox_gb_imageInfo.addWidget(scrollArea_image)
        mui.gb_imageInfo.setMinimumWidth(520)
        mui.gb_imageInfo.setVisible(True)
        mui.gb_imageInfo.setTitle("Image Information")
        mui.gb_imageInfo.setLayout(vbox_gb_imageInfo)

    ### ActionUI
    def exitActionUI(self, mui):
        mui.exitAction = QAction('Exit')
        mui.exitAction.setShortcut('Ctrl+Q')
        mui.exitAction.setStatusTip('Exit application')
        mui.exitAction.triggered.connect(mui.close)

    def readActionUI(self, mui):
        mui.readAction = QAction('Start')
        mui.readAction.setShortcut('Ctrl+S')
        mui.readAction.setStatusTip('Start to read the data from the text file')
        mui.readAction.triggered.connect(mui.read_csvfile)

    def connectActionUI(self, mui):
        mui.connectAction = QAction('Connect')
        mui.connectAction.setShortcut('Ctrl+C')
        mui.connectAction.setStatusTip('Connect to get the data by the NamedPipes from other application')
        mui.connectAction.triggered.connect(mui.connect_namedpipe)

    def opensubWindowActionUI(self, mui):
        mui.openwindowAction= QAction('Display')
        mui.openwindowAction.setShortcut('Ctrl+W')
        mui.openwindowAction.setStatusTip('Open the table window of features')
        mui.openwindowAction.triggered.connect(mui.open_subwindow)

    def openQMLWindowActionUI(self, mui):
        mui.openQMLAction= QAction('Model')
        mui.openQMLAction.setShortcut('Ctrl+M')
        mui.openQMLAction.setStatusTip('Model')
        mui.openQMLAction.triggered.connect(mui.open_qmlwindow)
