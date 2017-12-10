#!/usr/bin/env python
import sys
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt, QTimer)
from PyQt5.QtGui import (QBrush, QColor, QPainter)
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QGridLayout, QVBoxLayout, QHBoxLayout, QSizePolicy,
                             QLabel, QLineEdit, QPushButton)
from PyQt5.QtWidgets import (QMainWindow, QWidget, QLCDNumber, QSlider, QTextEdit, 
                             QTableWidget, QTableWidgetItem, QAction, QDialog)


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
        self.y = None

    def draw(self):
        self.axes.clear()
        self.axes.grid()
        self.axes.set_ylim([-5, 1000])
        self.axes.plot(self.x, self.y)
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
        self.sld.setRange(10, 1000)
        self.sld.setValue(30)
        self.sld.setFixedWidth(300)
        self.sld.setTickPosition(QSlider.TicksBothSides)
        self.sld.valueChanged.connect(lcd.display)
        
        ### set Button, TextBox
        self.pnameQle = QLineEdit(self)
        self.pnameQle.setText("NPtest")
        pnlabel = QLabel()
        pnlabel.setText('PipeName:')
        registBtn = QPushButton("Register")
        registBtn.clicked.connect(self.regist_namedpipe)
        self.regist_namedpipe()
        
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
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.main_plot.canvas)
        main_frame.setLayout(vbox)

        ### set widget
        self.setCentralWidget(main_frame)
   
        ###
        self.exitActionUI()
        self.connectActionUI()
        self.opensubWindowActionUI()
        
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.exitAction)

        toolbar = self.addToolBar('MainToolBar')
        toolbar.addAction(self.connectAction)
        toolbar.addAction(self.openwindowAction)

    ###################
    def exitActionUI(self):
        self.exitAction = QAction('Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(self.close)

    def connectActionUI(self):
        self.connectAction = QAction('Connect', self)
        self.connectAction.setStatusTip('Connect the data from other application')
        self.connectAction.triggered.connect(self.connect_namedpipe) 
    
    def opensubWindowActionUI(self):
        self.openwindowAction= QAction('Display', self)
        self.openwindowAction.setShortcut('Ctrl+W')
        self.openwindowAction.setStatusTip('Open the table window of features')
        self.openwindowAction.triggered.connect(self.open_subwindow) 

    ##################
    def regist_namedpipe(self):
        self.pname = self.pnameQle.text()
        
    def connect_namedpipe(self):
        if self.setting_pipename(self.pname) > 0:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_figure)
            self.timer.start(self.sld.value()) #(ms)
        
    def open_subwindow(self):
        subWindow = SubWindow(self)
        subWindow.show()

    def update_figure(self):
        self.update_data()
        self.main_plot.x = self.x
        self.main_plot.y = self.y
        self.main_plot.draw()
        
    def setting_pipename(self, pname):
        try:
            self.f = open(r'\\.\pipe\\' + pname, 'r+b', 0)
            #print("Connect:{0}".format(pname))
            return 1
        except:
            #print("Not Connect:{0}".format(pname))
            return -1

    def update_data(self):
        try:
            s = self.f.readline()
            proc_on = True
        except:
            proc_on = False
            self.f.close()
            print("Can't get data from the namedpipe")
        finally:
            pass    
        
        if(proc_on):
            str_data = s.decode('utf-8').split('\r\n')[0]
            if str_data == '':               
                self.x = self.feature
                self.y = self.feature
                self.timer.stop() #タイマーを起動させ続けると動作が重くなるため注意
                #print("{0:0}:{1}".format(len(self.x), self.x))
            else:
                features = np.array(str_data.split(','))
                self.x = features
                self.y = np.roll(features, -1)
                self.feature = features
                #print("{0:0}:{1}".format(len(features), features))

def main(args):
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main(sys.argv)