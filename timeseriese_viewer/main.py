#!/usr/bin/env python
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

#from PyQt5.QtGui import QGuiApplication
#from PyQt5.QtCore import (QLineF, QPointF, QRectF)
#from PyQt5.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsItem, QListWidget)
#from PyQt5.QtQuick import QQuickView
#from PyQt5.QtQml import QQmlApplicationEngine

from mypackage.plotdisplay_test import MainPlotWindow
from mypackage.qmldisplay_test import QMLWindow
from mypackage.subdisplay_test import SubWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.initUI()

        ### Setting
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

    def initUI(self):
        self.setWindowTitle('Main window')
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
        self.pltnum_sld.valueChanged.connect(self.sliderbar_display_plotnum)
        self.pltnum_qsb.valueChanged.connect(self.qspinbox_display_plotnum)

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
        self.sldv1.valueChanged.connect(self.sliderbar_display1)
        self.sldv1qsb.valueChanged.connect(self.spinbox_display1)
        self.sldv2 = QSlider(Qt.Vertical, self)
        self.sldv2.setRange(-200, 0)
        self.sldv2.setValue(-1)
        self.sldv2.setFixedHeight(200)
        self.sldv2qsb = QSpinBox()
        self.sldv2qsb.setRange(-9999, 0)
        self.sldv2qsb.setValue(self.sldv2.value())
        self.sldv2.valueChanged.connect(self.sliderbar_display2)
        self.sldv2qsb.valueChanged.connect(self.spinbox_display2)

        ### display graph
        self.framelabel = QLabel()
        self.framelabel.setText("Frame:{0}".format(0))
        restopBtn = QPushButton("Stop | Restart")
        restopBtn.clicked.connect(self.process_stop_restart)
        refreshBtn = QPushButton("Refresh")
        refreshBtn.clicked.connect(self.update_plot_data)

        self.combo = QComboBox(self)
        self.combo.addItem("SpineBase")
        self.combo.addItem("SpineMid")
        self.combo.addItem("Neck")
        self.combo.addItem("Head")
        self.combo.addItem("ShoulderLeft")
        self.combo.addItem("ElbowLeft")
        self.combo.addItem("WristLeft")
        self.combo.addItem("HandLeft")
        self.combo.addItem("ShoulderRight")
        self.combo.addItem("ElbowRight")
        self.combo.addItem("WristRight")
        self.combo.addItem("HandRight")
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
        self.sldh1.valueChanged.connect(self.sliderbar_display3)
        self.sldh1qsb.valueChanged.connect(self.spinbox_display3)
        self.sldh2 = QSlider(Qt.Horizontal, self)
        self.sldh2.setRange(1, 1000)
        self.sldh2.setValue(150)
        self.sldh2qsb = QSpinBox()
        self.sldh2qsb.setRange(1, 9999)
        self.sldh2qsb.setValue(self.sldh2.value())
        self.sldh2.valueChanged.connect(self.sliderbar_display4)
        self.sldh2qsb.valueChanged.connect(self.spinbox_display4)
        self.autoScrollqb = QCheckBox('Auto', self)
        self.autoScrollLabel = QLabel()
        self.autoScrollLabel.setText('Span:')
        self.autoScrollSpanNum_qsb = QSpinBox()
        self.autoScrollSpanNum_qsb.setRange(10, 1000)
        self.autoScrollSpanNum_qsb.setValue(100)

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
        hbox3_vbox = QVBoxLayout()
        hbox3_vbox.addWidget(self.sldv1)
        hbox3_vbox.addWidget(self.sldv1qsb)
        hbox3_vbox.addStretch(1)
        hbox3_vbox.addWidget(self.sldv2qsb)
        hbox3_vbox.addWidget(self.sldv2)
        hbox3.addLayout(hbox3_vbox)
        hbox3.addWidget(self.main_plot.canvas)

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
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        main_frame.setLayout(vbox)

        ### set widget
        self.setCentralWidget(main_frame)

        ###
        self.exitActionUI()
        self.readActionUI()
        self.connectActionUI()
        self.opensubWindowActionUI()
        self.openQMLWindowActionUI()

        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.exitAction)

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
            self.declareCommonVal()
            self.timer.start(self.sld.value()) #(ms)

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
        filename = QFileDialog.getOpenFileName(self, 'Open file') #, os.path.expanduser('~') + '/Desktop')
        self.fnameQle.setText(filename[0])

    def open_folder(self):
        foldername = QFileDialog.getExistingDirectory(self, 'Open Directory') #, os.path.expanduser('~') + '/Desktop')
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
    def sliderbar_display1(self):
        self.sldv1qsb.setValue(self.sldv1.value())
    def sliderbar_display2(self):
        self.sldv2qsb.setValue(self.sldv2.value())
    def sliderbar_display_plotnum(self):
        self.pltnum_qsb.setValue(self.pltnum_sld.value())
    def qspinbox_display_plotnum(self):
        self.pltnum_sld.setValue(self.pltnum_qsb.value())
    def sliderbar_display3(self):
        self.sldh1qsb.setValue(self.sldh1.value())
    def sliderbar_display4(self):
        self.sldh2qsb.setValue(self.sldh2.value())
    def spinbox_display1(self):
        self.sldv1.setValue(self.sldv1qsb.value())
    def spinbox_display2(self):
        self.sldv2.setValue(self.sldv2qsb.value())
    def spinbox_display3(self):
        self.sldh1.setValue(self.sldh1qsb.value())
    def spinbox_display4(self):
        self.sldh2.setValue(self.sldh2qsb.value())
    def autoScrollMode(self):
        if self.autoScrollqb.isChecked():
            self.sldh1.setValue(len(self.fval)-self.autoScrollSpanNum_qsb.value())
            self.sldh2.setValue(len(self.fval))

    #### new form
    def open_subwindow(self):
        subWindow = SubWindow(self)
        subWindow.show()

    ### QML
    def open_qmlwindow(self):
        QMLform = QMLWindow(self)
        QMLform.show()

    ### graph update
    def update_figure(self):
        self.counter += 1
        self.update_data()
        self.update_plot_data()
        self.runOn = self.timer.isActive()

    def updateTargetData(self):
        self.x = np.arange(len(self.fval))
        fvalT = np.array(self.fval).T
        self.y1 = fvalT[0 + 3 * self.parts_dict[self.combo.currentText()]]
        self.y2 = fvalT[1 + 3 * self.parts_dict[self.combo.currentText()]]
        self.y3 = fvalT[2 + 3 * self.parts_dict[self.combo.currentText()]]

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
        self.main_plot.ylim_max =  self.sldv1qsb.value()
        self.main_plot.ylim_min =  self.sldv2qsb.value()
        self.main_plot.grid_flag = self.grid_cb.checkState()

        self.main_plot.draw()

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
                self.framelabel.setText("Frame:{0}".format(self.counter - 1))

def main(args):
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main(sys.argv)
