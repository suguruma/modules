#!/usr/bin/env python
import sys
import os
import numpy as np
from collections import deque

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt, QTimer)
from PyQt5.QtGui import (QBrush, QColor, QPainter)
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QGridLayout, QVBoxLayout, QHBoxLayout, QSizePolicy,
                             QLabel, QLineEdit, QPushButton)
from PyQt5.QtWidgets import (QMainWindow, QWidget, QLCDNumber, QSlider, QTextEdit, QCheckBox, 
                             QTableWidget, QTableWidgetItem, QAction, QDialog, QSpinBox, QFileDialog)


class SubWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sub window') 
        self.resize(640,480)
        sub_frame = QWidget()
        label = QLabel()
        label.setText('Features')
        table = QTableWidget()
        table.setRowCount(10)
        table.setColumnCount(10)
        table.setItem(0,0, QTableWidgetItem("1"))
        table.setItem(0,1, QTableWidgetItem("2"))
        table.setItem(1,0, QTableWidgetItem("3"))
        table.setItem(1,1, QTableWidgetItem("4"))
        
        grid = QGridLayout()
        grid.addWidget(label)
        grid.addWidget(table)
        sub_frame.setLayout(grid)
        self.setCentralWidget(sub_frame)

class MainPlot():
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
        colorlist = ["b", "g", "r", "c", "m", "y", "k", "w", '#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf']
        
        if self.display_x:
            self.axes.plot(self.x, self.y1, color=colorlist[0])
        if self.display_y:
            self.axes.plot(self.x, self.y2, color=colorlist[1])
        if self.display_z:
            self.axes.plot(self.x, self.y3, color=colorlist[2])
        self.canvas.draw()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.initUI()

        ### Setting
        self.skip_header = True
        self.runOn = False

    def initUI(self):
        self.setWindowTitle('Main window') 
        main_frame = QWidget()
        self.main_plot = MainPlot(main_frame)

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
        self.pltnum_qsb.setValue(100)
        self.pltnum_sld = QSlider(Qt.Horizontal, self)
        self.pltnum_sld.setRange(10, 1000)
        self.pltnum_sld.setValue(100)
        self.pltnum_sld.setFixedWidth(300)
        self.pltnum_sld.valueChanged.connect(self.sliderbar_display_plotnum)

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
        self.sldv1.setValue(30)
        self.sldv1.setFixedHeight(200)
        self.sldv1qsb = QSpinBox()
        self.sldv1qsb.setRange(1, 9999)
        self.sldv1qsb.setValue(self.sldv1.value())
        self.sldv1.valueChanged.connect(self.sliderbar_display1)
        self.sldv2 = QSlider(Qt.Vertical, self)
        self.sldv2.setRange(-200, 0)
        self.sldv2.setValue(-5)
        self.sldv2.setFixedHeight(200)
        self.sldv2qsb = QSpinBox()
        self.sldv2qsb.setRange(-9999, 0)
        self.sldv2qsb.setValue(self.sldv2.value())
        self.sldv2.valueChanged.connect(self.sliderbar_display2)

        ### display graph
        self.framelabel = QLabel()
        self.framelabel.setText("Frame:{0}".format(0))
        restopBtn = QPushButton("Stop | Restart")
        restopBtn.clicked.connect(self.process_stop_restart)
        refreshBtn = QPushButton("Refresh")
        refreshBtn.clicked.connect(self.update_plot_data)
        self.cbx = QCheckBox('X', self)
        self.cby = QCheckBox('Y', self)
        self.cbz = QCheckBox('Z', self)
        self.cbx.toggle()
        self.grid_cb = QCheckBox('Grid', self)
        self.grid_cb.toggle()

        ### set file layout
        self.fnameQle = QLineEdit(self)
        self.fnameQle.setText("data.csv")
        self.openfile_Btn = QPushButton('Open File')
        self.openfile_Btn.clicked.connect(self.open_file)
        self.openfolder_Btn = QPushButton('Open Folder')
        self.openfolder_Btn.clicked.connect(self.open_folder)
        hbox0 = QHBoxLayout()
        hbox0.addWidget(self.openfile_Btn)
        #hbox0.addWidget(self.openfolder_Btn)
        hbox0.addWidget(self.fnameQle)

        ### set layout
        hbox = QHBoxLayout()
        hbox.addWidget(upinlabel)
        hbox.addWidget(lcd)
        hbox.addWidget(mslabel)
        hbox.addWidget(self.sld)
        hbox.addStretch(1)
        hbox.addWidget(registBtn)
        hbox.addWidget(pnlabel)
        hbox.addWidget(self.pnameQle)
        
        ### set Layout2
        hbox2 = QHBoxLayout()
        hbox2.addWidget(restopBtn)
        hbox2.addWidget(self.framelabel)
        hbox2.addStretch(1)
        hbox2.addWidget(self.grid_cb)
        hbox2.addStretch(1)
        hbox2.addWidget(pltnum_label)
        hbox2.addWidget(self.pltnum_sld)
        hbox2.addWidget(self.pltnum_qsb)
        hbox2.addWidget(refreshBtn)
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
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox0)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        main_frame.setLayout(vbox)

        ### set widget
        self.setCentralWidget(main_frame)
   
        ###
        self.exitActionUI()
        self.readActionUI()
        self.connectActionUI()
        self.opensubWindowActionUI()
        
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.exitAction)

        toolbar = self.addToolBar('MainToolBar')
        toolbar.addAction(self.readAction)
        toolbar.addAction(self.connectAction)
        toolbar.addAction(self.openwindowAction)

    ### ################
    def exitActionUI(self):
        self.exitAction = QAction('Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(self.close)

    def readActionUI(self):
        self.readAction = QAction('Start', self)
        self.readAction.setStatusTip('Start to read the data from the text file')
        self.readAction.triggered.connect(self.read_csvfile) 
    
    def connectActionUI(self):
        self.connectAction = QAction('Connect', self)
        self.connectAction.setStatusTip('Connect to get the data by the NamedPipes from other application')
        self.connectAction.triggered.connect(self.connect_namedpipe)
    
    def opensubWindowActionUI(self):
        self.openwindowAction= QAction('Display', self)
        self.openwindowAction.setShortcut('Ctrl+W')
        self.openwindowAction.setStatusTip('Open the table window of features')
        self.openwindowAction.triggered.connect(self.open_subwindow) 

    def declareCommonVal(self):
        self.counter = 0
        self.fval1 = deque([])
        self.fval2 = deque([])
        self.fval3 = deque([])        

    ### namedpipe 
    def regist_namedpipe(self):
        self.pname = self.pnameQle.text()
        
    def connect_namedpipe(self):
        if self.runOn:
            return 0

        self.declareCommonVal()
        if self.setting_pipename(self.pname) > 0:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_figure)
            self.timer.start(self.sld.value()) #(ms)
        
    def setting_pipename(self, pname):
        try:
            self.f = open(r'\\.\pipe\\' + pname, 'r+b', 0)
            self.flagOfDecode = True
            #print("Connect:{0}".format(pname))
            return 1
        except:
            #print("Not Connect:{0}".format(pname))
            return -1

    ### text
    def read_csvfile(self):
        if self.runOn:
            return 0
            
        self.declareCommonVal()
        if self.setting_textname(self.fnameQle.text()) > 0:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_figure)
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
        self.fnameQle.setText(foldername)

    ### window refresh
    def sliderbar_display1(self):
        self.sldv1qsb.setValue(self.sldv1.value())
    def sliderbar_display2(self):
        self.sldv2qsb.setValue(self.sldv2.value())
    def sliderbar_display_plotnum(self):
        self.pltnum_qsb.setValue(self.pltnum_sld.value())

    #### new form
    def open_subwindow(self):
        subWindow = SubWindow(self)
        subWindow.show()

    ### graph update
    def update_figure(self):
        self.counter += 1
        self.update_data()
        self.update_plot_data()        
        self.runOn = self.timer.isActive()
    
    def update_plot_data(self):
        self.main_plot.x = self.x
        self.main_plot.y1 = self.y1
        self.main_plot.y2 = self.y2
        self.main_plot.y3 = self.y3
        self.main_plot.display_x = self.cbx.checkState()
        self.main_plot.display_y = self.cby.checkState()
        self.main_plot.display_z = self.cbz.checkState()
        self.main_plot.xlim_max = self.pltnum_qsb.value()
        self.main_plot.ylim_max =  self.sldv1qsb.value()
        self.main_plot.ylim_min =  self.sldv2qsb.value()
        self.main_plot.grid_flag = self.grid_cb.checkState()

        self.main_plot.draw()
    
    def skip_space_csv(self, str_data):
        for i in range(len(str_data)):
            if len(str_data[i]) == 0:
                str_data[i] = 0
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

                self.fval1.append(features[0])
                self.fval2.append(features[1])
                self.fval3.append(features[2])
                
                if self.counter - 1 > self.pltnum_qsb.value():
                    self.fval1.popleft()
                    self.fval2.popleft()
                    self.fval3.popleft()

                self.x = np.arange(len(self.fval1))
                self.y1 = self.fval1
                self.y2 = self.fval2
                self.y3 = self.fval3
                
                self.framelabel.setText("Frame:{0}".format(self.counter - 1))


def main(args):
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main(sys.argv)