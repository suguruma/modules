#!/usr/bin/env python

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt, QTimer)
from PyQt5.QtGui import (QBrush, QColor, QPainter)
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QGridLayout, QVBoxLayout, QHBoxLayout, QSizePolicy,
                             QLabel, QLineEdit, QPushButton)
from PyQt5.QtWidgets import (QMainWindow, QWidget, QLCDNumber, QSlider)

import numpy as np

# FigureCanvas inherits QWidget
class MainWindow(FigureCanvas):
    def __init__(self, parent=None, width=4, height=3, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.hold(False)

        super(MainWindow, self).__init__(fig)
        self.setParent(parent)
        self.setWindowTitle("Curve")
        
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        btn1 = QPushButton("Connect", self)
        btn1.move(50, 10)
        btn1.clicked.connect(self.buttonClicked)      
        
    def buttonClicked(self):
        if self.setting_pipename("NPtest") > 0:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_figure)
            self.timer.start(100) #(ms)
            #sender = self.sender()
            #self.statusBar().showMessage(sender.text() + ' was pressed')

    def update_figure(self):
        self.update_data()
        self.axes.plot(self.x, self.y)
        self.draw()
        
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

        
if __name__ == '__main__':
    #nptest1()

    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())