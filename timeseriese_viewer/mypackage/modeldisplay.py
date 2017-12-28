import sys
import numpy as np
from collections import deque
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import (Qt, QUrl, QTimer)
from PyQt5.QtGui import (QStandardItemModel, QStandardItem, QPixmap)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
                               QPushButton, QComboBox, QCheckBox, QLabel, QSpinBox, QLineEdit, QListView,
                               QLCDNumber, QSlider, QTableWidget, QTableWidgetItem, QAction, QFileDialog,
                               QGroupBox, QScrollArea, QSizePolicy
                             )
from PyQt5.QtQuickWidgets import QQuickWidget
from mypackage.plotdisplay import MainPlotWindow

class ModelWindow(QMainWindow):
    def setupUI(self, mui):
        self.initUI(mui)

    def initUI(self, mui):
        self.setWindowTitle('Model Window')
        self.setGeometry(300, 100, 1000, 350)
        sub_frame = QWidget()

        self.textname = ""
        self.imglist = deque([])
        self.skip_header = True
        self.flag_readFile = False
        self.counter = 0
        self.fval = deque([])
        self.model_timer = QTimer(self)
        self.model_timer.timeout.connect(lambda : self.update_model_frame(mui))
        self.flagFront = False
        self.thread_stop = False

        self.textActionUI(mui)
        self.windowActionUI(mui)

        toolbar = self.addToolBar('ToolBar')
        toolbar.addAction(self.textAction)
        toolbar.addAction(self.windowAction)

        scrollArea_image = QScrollArea()
        self.lbl_image = QLabel()
        self.lbl_image.setMinimumWidth(520)
        self.lbl_image.setMinimumHeight(400)
        scrollArea_image.setWidget(self.lbl_image)
        scrollArea_image.setMinimumWidth(500)

        ## Figure
        self.model_plot = MainPlotWindow()
        self.x = deque([])
        self.y = deque([])
        self.model_plot.axes.plot(self.x, self.y)

        ### |1|
        vbox1 = QVBoxLayout()
        vbox1.addWidget(scrollArea_image)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.model_plot.canvas)

        grid = QGridLayout()
        grid.addLayout(vbox1, 1, 0)
        grid.addLayout(vbox2, 1, 1)

        sub_frame.setLayout(grid)
        self.setCentralWidget(sub_frame)

    def update_model_frame(self, mui):
        if self.textname == "":
            return -1
        if self.flag_readFile:
            self.setting_textname(self.textname)
            self.flag_readFile = False
        self.updateImage(mui)
        self.updateFigure(mui)

    def loop_update(self, mui, num):
        for i in range(num):
            self.thread_stop = False
            self.updateImage(mui)
            self.updateFigure(mui)
        self.thread_stop = True

    def update_model_frame_last(self, mui):
        if self.textname == "":
            return -1

        import threading
        num = self.maxFrameNum - self.counter
        self.th_me = threading.Thread(target=self.loop_update, name="th_me", args=(mui,num,))
        self.th_me.start()
        #self.model_timer.start(mui.sld.value())

    def updateImage(self, mui):
        #if mui.frameNumbSpb.value() < len(self.imglist):
        #    self.lbl_image.setPixmap(QPixmap(self.imglist[mui.frameNumbSpb.value()]))
        if self.counter < self.maxFrameNum - 1:
            self.lbl_image.setPixmap(QPixmap(self.imglist[self.counter]))

    def updateFigure(self, mui):
        self.counter += 1
        self.update_data(mui)
        self.model_plot.display_x = mui.cbx.checkState()
        self.model_plot.display_y = mui.cby.checkState()
        self.model_plot.display_z = mui.cbz.checkState()
        self.model_plot.xlim_min = mui.sldh1.value()
        self.model_plot.xlim_max = mui.sldh2.value()
        self.model_plot.ylim_max = mui.sldv1qsb.value()
        self.model_plot.ylim_min = mui.sldv2qsb.value()
        self.model_plot.grid_flag = mui.grid_cb.checkState()
        self.model_plot.draw()

    def update_data(self, mui):
        try:
            s = self.f.readline()
            proc_on = True
        except:
            proc_on = False
            self.f.close()
        finally:
            pass

        if(proc_on):
            str_data = s.split('\n')[0]
            if str_data == '':
                self.f.close()
                #self.model_timer.stop()
                self.x = deque([])
                self.fval = deque([])
            else:
                features = str_data.split(',')
                features = self.skip_space_csv(features)
                features = np.array(features).astype(np.float64)

                self.fval.append(features)

                #if self.counter - 1 > self.pltnum_qsb.value():
                #    self.fval.popleft()
                self.x = np.arange(len(self.fval))
                fvalT = np.array(self.fval).T
                self.y1 = fvalT[0 + 3 * mui.parts_dict[mui.combo.currentText()]]
                self.y2 = fvalT[1 + 3 * mui.parts_dict[mui.combo.currentText()]]
                self.y3 = fvalT[2 + 3 * mui.parts_dict[mui.combo.currentText()]]

                self.model_plot.x = self.x
                self.model_plot.y1 = self.y1
                self.model_plot.y2 = self.y2
                self.model_plot.y3 = self.y3
                #self.updateTargetData()
                #self.frameNumbSpb.setValue(self.counter - 1)
                #self.framelabel.setText("Frame:") #{0}".format(self.counter - 1))

    def setting_textname(self, fname):
        try:
            self.f = open(fname, 'r')
            if self.skip_header:
                next(self.f)
            return 1
        except:
            return -1

    def skip_space_csv(self, str_data):
        for i in range(len(str_data)):
            if len(str_data[i]) == 0:
                str_data[i] = np.nan
        return str_data

    def read_csvfile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '.')[0]
        self.textname = fname
        if (not fname == ""):
            self.textname = fname
            self.setWindowTitle('Model Window : {0}'.format(self.textname))
            if self.setting_textname(self.textname) > 0:
                self.getFrameImages()
                self.flag_readFile = False
            self.maxFrameNum = len(self.imglist)

    def getFrameImages(self):
        self.imglist = deque([])
        str_path = self.textname
        str_path = str_path.replace("coordinate", "img").split('.csv')[0]
        imageFolder = str_path + "/*"

        import glob
        import re
        def numericalSort(value):
            numbers = re.compile(r'(\d+)')
            parts = numbers.split(value)
            parts[1::2] = map(int, parts[1::2])
            return parts

        files = sorted(glob.glob(imageFolder), key=numericalSort)
        for filename in files:
            self.imglist.append(filename)

    def textActionUI(self, mui):
        self.textAction = QAction('Open')
        self.textAction.setShortcut('Ctrl+O')
        self.textAction.triggered.connect(self.read_csvfile)

    def windowActionUI(self, mui):
        self.windowAction = QAction('Front/Back')
        self.windowAction.setShortcut('Ctrl+F')
        self.windowAction.triggered.connect(self.changeWindowMode)

    def changeWindowMode(self):
        if (self.flagFront):
            self.setWindowFlags(Qt.WindowStaysOnBottomHint)
            self.flagFront = False
        else:
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.flagFront = True
        self.show()
