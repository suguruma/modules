#!/usr/bin/env python
import sys
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
                             QTableWidget, QTableWidgetItem, QAction, QDialog, QSpinBox)


## 1：波形を選択できるようにする

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
        table.setItem(0,0, QTableWidgetItem("Tom"))
        table.setItem(0,1, QTableWidgetItem("15"))
        table.setItem(1,0, QTableWidgetItem("Ken"))
        table.setItem(1,1, QTableWidgetItem("40"))
        
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
        self.xlimmax = 100

    def draw(self):
        self.axes.clear()
        self.axes.grid()
        self.axes.set_xlim([0, self.xlimmax])
        self.axes.set_ylim([-5, 50])
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
        qsblabel = QLabel()
        qsblabel.setText('Plot Num:')
        self.qsb = QSpinBox()
        self.qsb.setRange(10, 1000)
        self.qsb.setValue(100)
        
        ### set Button, TextBox
        self.pnameQle = QLineEdit(self)
        self.pnameQle.setText("NPtest")
        pnlabel = QLabel()
        pnlabel.setText('Pipe Name:')
        registBtn = QPushButton("Register")
        registBtn.clicked.connect(self.regist_namedpipe)
        self.regist_namedpipe()
        
        ### display graph
        self.framelabel = QLabel()
        self.framelabel.setText("Frame:{0}".format(0))
        restopBtn = QPushButton("Stop|Restart")
        restopBtn.clicked.connect(self.process_stop_restart)
        refreshBtn = QPushButton("Refresh")
        refreshBtn.clicked.connect(self.update_plot_data)
        self.cbx = QCheckBox('X', self)
        self.cby = QCheckBox('Y', self)
        self.cbz = QCheckBox('Z', self)
        self.cbx.toggle()

        ### 
        self.fname = "data.csv"
        self.skip_header = True
        self.runOn = False
        
        ### set layout
        hbox = QHBoxLayout()
        hbox.addWidget(upinlabel)
        hbox.addWidget(lcd)
        hbox.addWidget(mslabel)
        hbox.addWidget(self.sld)
        hbox.addStretch(1)
        hbox.addWidget(qsblabel)
        hbox.addWidget(self.qsb)
        hbox.addWidget(registBtn)
        hbox.addWidget(pnlabel)
        hbox.addWidget(self.pnameQle)
        
        ### set Layout2
        hbox2 = QHBoxLayout()
        hbox2.addWidget(restopBtn)
        hbox2.addWidget(self.framelabel)
        hbox2.addStretch(1)
        hbox2.addWidget(refreshBtn)
        hbox2.addWidget(self.cbx)
        hbox2.addWidget(self.cby)
        hbox2.addWidget(self.cbz)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.main_plot.canvas)
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

    ###################
    def exitActionUI(self):
        self.exitAction = QAction('Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(self.close)

    def readActionUI(self):
        self.readAction = QAction('Read', self)
        self.readAction.setStatusTip('Read the data from text file')
        self.readAction.triggered.connect(self.read_csvfile) 
    
    def connectActionUI(self):
        self.connectAction = QAction('Connect', self)
        self.connectAction.setStatusTip('Connect the data from other application')
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
        if self.setting_textname(self.fname) > 0:
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
        self.main_plot.xlimmax = self.qsb.value()
        self.main_plot.draw()
                
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
                str_data = s;
                
            if str_data == '':               
                self.timer.stop() #タイマーを起動させ続けると動作が重くなるため注意
                self.f.close()
            else:
                features = np.array(str_data.split(','))

                counter_lim = self.counter
                self.fval1.append(features[0])
                self.fval2.append(features[1])
                self.fval3.append(features[2])
                
                if counter_lim > self.qsb.value():
                    counter_lim = self.qsb.value()
                    self.fval1.popleft()
                    self.fval2.popleft()
                    self.fval3.popleft()
                   
                self.x = np.arange(counter_lim)
                self.y1 = self.fval1
                self.y2 = self.fval2
                self.y3 = self.fval3
                
                self.framelabel.setText("Frame:{0}".format(self.counter))


def main(args):
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main(sys.argv)