import sys
import numpy as np
from collections import deque
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import (Qt, QUrl, QTimer, QStringListModel, QObject)
from PyQt5.QtGui import (QStandardItemModel, QStandardItem, QPixmap, QPainter, QPen, QColor)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
                               QPushButton, QComboBox, QCheckBox, QLabel, QSpinBox, QLineEdit, QListView,
                               QLCDNumber, QSlider, QTableWidget, QTableWidgetItem, QAction, QFileDialog,
                               QGroupBox, QScrollArea, QSizePolicy
                             )
from PyQt5.QtQuickWidgets import QQuickWidget
from PyQt5.QtChart import QChart, QChartView, QBarSet, QHorizontalBarSeries, QBarCategoryAxis, QValueAxis
from mypackage.plotdisplay import MainPlotWindow

from mypackage.calcdistance import CalcTimeserieseDistance

class UI_ModelWindow(object):
    def setupUI(self, smwui):
        self.initUI()
        self.mainUI(smwui)
        self.barUI(smwui)
        self.drawUI(smwui)
        self.analysisUI(smwui)

    def initUI(self):
        self.grid = QGridLayout()
        self.gb_draw = QGroupBox()
        self.gb_analysis = QGroupBox()

    def mainUI(self, smwui):
        smwui.setWindowTitle('Model Window')
        smwui.setGeometry(300, 100, 1000, 800)
        sub_frame = QWidget()

        self.grid.addWidget(self.gb_draw, 0, 0)
        self.grid.addWidget(self.gb_analysis, 1, 0)

        sub_frame.setLayout(self.grid)
        smwui.setCentralWidget(sub_frame)

    def barUI(self, smwui):
        btn_openFile = QPushButton('OpenFile')
        btn_openFile.clicked.connect(smwui.read_csvfile)
        smwui.cb_frontWindow = QCheckBox('Top')
        smwui.cb_frontWindow.stateChanged.connect(smwui.changeWindowStaysMode)
        smwui.cb_drawFigure = QCheckBox('Draw')
        smwui.cb_drawFigure.setChecked(True)

        toolbar = smwui.addToolBar('ToolBar')
        toolbar.addWidget(btn_openFile)
        toolbar.addWidget(smwui.cb_frontWindow)
        toolbar.addWidget(smwui.cb_drawFigure)

    def drawUI(self, smwui):
        ### Image
        scrollArea_image = QScrollArea()
        smwui.lbl_image = QLabel()
        smwui.lbl_image.setMinimumWidth(500)
        smwui.lbl_image.setMinimumHeight(400)
        scrollArea_image.setWidget(smwui.lbl_image)
        scrollArea_image.setMinimumWidth(500)
        ### Figure
        smwui.model_plot = MainPlotWindow()
        smwui.x = deque([])
        smwui.y = deque([])
        smwui.model_plot.axes.plot(smwui.x, smwui.y)
        smwui.model_plot.canvas.setMinimumWidth(1)
        ### |1|
        vbox1 = QVBoxLayout()
        vbox1.addWidget(scrollArea_image)
        ### |2|
        vbox2 = QVBoxLayout()
        vbox2.addWidget(smwui.model_plot.canvas)
        ### *1*2*
        hbox = QHBoxLayout()
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)

        self.gb_draw.setTitle('Model View')
        self.gb_draw.setLayout(hbox)

    def analysisUI(self, smwui):

        btn_refresh = QPushButton('Refresh')
        btn_refresh.clicked.connect(smwui.update_chart)

        smwui.cb_targetAxis1 = QCheckBox('X : Horizontal action')
        smwui.cb_targetAxis1.setChecked(True)
        smwui.cb_targetAxis1.stateChanged.connect(smwui.update_chart)
        smwui.cb_targetAxis2 = QCheckBox('Y : Vertical action')
        smwui.cb_targetAxis2.setChecked(True)
        smwui.cb_targetAxis2.stateChanged.connect(smwui.update_chart)
        smwui.cb_targetAxis3 = QCheckBox('Z : Depth action')
        smwui.cb_targetAxis3.setChecked(True)
        smwui.cb_targetAxis3.stateChanged.connect(smwui.update_chart)

        smwui.cb_targetValue1 = QCheckBox('Head')
        smwui.cb_targetValue1.setChecked(True)
        smwui.cb_targetValue2 = QCheckBox('ShoulderRight')
        smwui.cb_targetValue3 = QCheckBox('ElbowRight')
        smwui.cb_targetValue4 = QCheckBox('HandRight')
        smwui.cb_targetValue4.setChecked(True)
        smwui.cb_targetValue5 = QCheckBox('SpineBase')
        smwui.cb_targetValue6 = QCheckBox('HandLeft')
        smwui.cb_targetValue6.setChecked(True)
        smwui.cb_targetValue7 = QCheckBox('ElbowLeft')
        smwui.cb_targetValue8 = QCheckBox('ShoulderLeft')
        smwui.cb_targetValue9 = QCheckBox('Neck')
        smwui.cb_targetValue1.stateChanged.connect(smwui.update_chart)
        smwui.cb_targetValue2.stateChanged.connect(smwui.update_chart)
        smwui.cb_targetValue3.stateChanged.connect(smwui.update_chart)
        smwui.cb_targetValue4.stateChanged.connect(smwui.update_chart)
        smwui.cb_targetValue5.stateChanged.connect(smwui.update_chart)
        smwui.cb_targetValue6.stateChanged.connect(smwui.update_chart)
        smwui.cb_targetValue7.stateChanged.connect(smwui.update_chart)
        smwui.cb_targetValue8.stateChanged.connect(smwui.update_chart)
        smwui.cb_targetValue9.stateChanged.connect(smwui.update_chart)

        ### chart
        set1 = QBarSet("X")
        set2 = QBarSet("Y")
        set3 = QBarSet("Z")
        set1.setColor(QColor(0, 0, 200, 150))
        set2.setColor(QColor(0, 200, 0, 150))
        set3.setColor(QColor(200, 50, 0, 150))

        series = QHorizontalBarSeries()
        series.append(set1)
        series.append(set2)
        series.append(set3)

        categories = []
        categories.append('Parts')
        axisX = QValueAxis()
        axisX.applyNiceNumbers()
        axisY = QBarCategoryAxis()
        axisY.append(categories)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Timeseries Distance")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setAxisX(axisX, series)
        chart.setAxisY(axisY)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignTop)

        smwui.chartView = QChartView(chart)
        smwui.chartView.setRenderHint(QPainter.Antialiasing)

        ### draw parts
        smwui.viewParts = QQuickWidget()
        smwui.viewParts.setSource(QUrl("./qml/qmlptviewer/main.qml"))
        smwui.viewParts.rootContext().setContextProperty("HandRight", "0,0,0,0")
        smwui.viewParts.rootContext().setContextProperty("HandLeft", "0,0,0,0")
        smwui.viewParts.rootContext().setContextProperty("ElbowRight", "0,0,0,0")
        smwui.viewParts.rootContext().setContextProperty("ElbowLeft", "0,0,0,0")
        smwui.viewParts.rootContext().setContextProperty("Head", "0,0,0,0")
        scrollArea_viewParts = QScrollArea()
        scrollArea_viewParts.setMinimumWidth(420)
        scrollArea_viewParts.setWidget(smwui.viewParts)
        scrollArea_viewParts.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        ### |1|
        vbox1 = QVBoxLayout()
        vbox1.addWidget(smwui.cb_targetAxis1)
        vbox1.addWidget(smwui.cb_targetAxis2)
        vbox1.addWidget(smwui.cb_targetAxis3)
        gb_targetAxis = QGroupBox()
        gb_targetAxis.setTitle('Axis')
        gb_targetAxis.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        gb_targetAxis.setLayout(vbox1)

        ### |2|
        vbox2 = QVBoxLayout()
        vbox2.addWidget(smwui.cb_targetValue1)
        vbox2.addWidget(smwui.cb_targetValue2)
        vbox2.addWidget(smwui.cb_targetValue3)
        vbox2.addWidget(smwui.cb_targetValue4)
        vbox2.addWidget(smwui.cb_targetValue5)
        vbox2.addWidget(smwui.cb_targetValue6)
        vbox2.addWidget(smwui.cb_targetValue7)
        vbox2.addWidget(smwui.cb_targetValue8)
        vbox2.addWidget(smwui.cb_targetValue9)
        gb_targetValue = QGroupBox()
        gb_targetValue.setTitle('Parts')
        gb_targetValue.setLayout(vbox2)

        vbox3 = QVBoxLayout()
        vbox3.addWidget(btn_refresh)
        vbox3.addWidget(gb_targetAxis)
        vbox3.addWidget(gb_targetValue)

        ### -1-
        hbox = QHBoxLayout()
        hbox.addLayout(vbox3)
        hbox.addWidget(smwui.chartView)
        hbox.addWidget(scrollArea_viewParts)

        self.gb_analysis.setFixedHeight(400)
        self.gb_analysis.setTitle("Analysis")
        self.gb_analysis.setLayout(hbox)

class ModelWindow(QMainWindow):
    def closeEvent(self, event):
        self.textname = ""
        self.setWindowTitle('Model Window')
        event.accept()

    def run(self, mui):
        ui = UI_ModelWindow()
        ui.setupUI(self)
        self.setParameter(mui)

    ##### -----
    def changeWindowStaysMode(self):
        if (self.cb_frontWindow.checkState()):
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(Qt.WindowStaysOnBottomHint)
        self.show()

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

    ##### -----
    def setParameter(self, mui):
        self.textname = ""
        self.imglist = deque([])
        self.skip_header = True
        self.flag_readFile = False
        self.counter = 0
        self.fval = deque([])
        self.model_timer = QTimer(self)
        self.model_timer.timeout.connect(lambda: self.update_model_frame(mui))
        self.flagFront = False
        self.thread_stop = False
        self.flag_drawOn = True
        self.thread_stop_i = -1
        self.ctd = CalcTimeserieseDistance()
        self.parts_dict = { "SpineBase":0, "SpineMid":1, "Neck":2, "Head":3,
                            "ShoulderLeft":4, "ElbowLeft":5, "WristLeft":6, "HandLeft":7,
                            "ShoulderRight":8, "ElbowRight":9, "WristRight":10, "HandRight":11,
                            "SpineShoulder":12, "HandTipLeft":13, "HandTipRight":14
        }

    def update_chart(self):

        if not self.cb_targetAxis1.checkState() and not self.cb_targetAxis2.checkState() and not self.cb_targetAxis3.checkState():
            return -1

        ## data
        n = self.ctd.generateLabel(45)
        for i in range(45):
            self.ctd.setNum(n[i])

        ## draw chart
        set1 = QBarSet("X")
        set2 = QBarSet("Y")
        set3 = QBarSet("Z")
        set1.setColor(QColor(0, 0, 200, 180))
        set2.setColor(QColor(0, 200, 0, 180))
        set3.setColor(QColor(200, 100, 0, 180))

        self.categories = []
        self.set1_val = np.array([])
        self.set2_val = np.array([])
        self.set3_val = np.array([])
        for i in range(len(self.parts_dict)):
            flag_add = False
            if self.parts_dict[self.cb_targetValue1.text()] == i and self.cb_targetValue1.checkState():
                flag_add = True
                self.categories.append(self.cb_targetValue1.text())
            elif self.parts_dict[self.cb_targetValue2.text()] == i and self.cb_targetValue2.checkState():
                flag_add = True
                self.categories.append(self.cb_targetValue2.text())
            elif self.parts_dict[self.cb_targetValue3.text()] == i and self.cb_targetValue3.checkState():
                flag_add = True
                self.categories.append(self.cb_targetValue3.text())
            elif self.parts_dict[self.cb_targetValue4.text()] == i and self.cb_targetValue4.checkState():
                flag_add = True
                self.categories.append(self.cb_targetValue4.text())
            elif self.parts_dict[self.cb_targetValue5.text()] == i and self.cb_targetValue5.checkState():
                flag_add = True
                self.categories.append(self.cb_targetValue5.text())
            elif self.parts_dict[self.cb_targetValue6.text()] == i and self.cb_targetValue6.checkState():
                flag_add = True
                self.categories.append(self.cb_targetValue6.text())
            elif self.parts_dict[self.cb_targetValue7.text()] == i and self.cb_targetValue7.checkState():
                flag_add = True
                self.categories.append(self.cb_targetValue7.text())
            elif self.parts_dict[self.cb_targetValue8.text()] == i and self.cb_targetValue8.checkState():
                flag_add = True
                self.categories.append(self.cb_targetValue8.text())
            elif self.parts_dict[self.cb_targetValue9.text()] == i and self.cb_targetValue9.checkState():
                flag_add = True
                self.categories.append(self.cb_targetValue9.text())

            if flag_add:
                set1 << self.ctd.distanceList[0 + 3*i]
                set2 << self.ctd.distanceList[1 + 3*i]
                set3 << self.ctd.distanceList[2 + 3*i]
                self.set1_val = np.append(self.set1_val, [self.ctd.distanceList[0 + 3*i]])
                self.set2_val = np.append(self.set2_val, [self.ctd.distanceList[1 + 3*i]])
                self.set3_val = np.append(self.set3_val, [self.ctd.distanceList[2 + 3*i]])

        series = QHorizontalBarSeries()
        if self.cb_targetAxis1.checkState():
            series.append(set1)
        else:
            self.set1_val = np.zeros(len(self.categories))
        if self.cb_targetAxis2.checkState():
            series.append(set2)
        else:
            self.set2_val = np.zeros(len(self.categories))
        if self.cb_targetAxis3.checkState():
            series.append(set3)
        else:
            self.set3_val = np.zeros(len(self.categories))

        axisX = QValueAxis()
        axisX.applyNiceNumbers()
        axisY = QBarCategoryAxis()
        axisY.append(self.categories)

        chart = QChart()
        chart.setTitle("Timeseries Distance")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.addSeries(series)
        chart.setAxisX(axisX, series)
        chart.setAxisY(axisY)

        self.chartView.setChart(chart)
        self.chartView.setRenderHint(QPainter.Antialiasing)

        self.update_parts()

    def update_parts(self):
        set_max = [0, 0, 0]
        set_max_categories = [-1, -1, -1]
        for i in range(len(self.categories)):
            if set_max[0] < self.set1_val[i]:
                set_max[0] = self.set1_val[i]
                set_max_categories[0] = self.categories[i]
            if set_max[1] < self.set2_val[i]:
                set_max[1] = self.set2_val[i]
                set_max_categories[1] = self.categories[i]
            if set_max[2] < self.set3_val[i]:
                set_max[2] = self.set3_val[i]
                set_max_categories[2] = self.categories[i]

        self.viewParts.setSource(QUrl("./qml/qmlptviewer/main.qml"))
        self.init_parts()

        if len(self.categories) == 0:
            return -1
        set_max_num = -1
        set_max_no = -1
        for i in range(len(set_max)):
            if set_max_num < set_max[i]:
                set_max_num = set_max[i]
                set_max_no = i

        ### Merge XYZ
        self.viewParts.rootContext().setContextProperty(set_max_categories[set_max_no], "0.9,0.4,0.4,0.9")

        ### Eahc XYZ
        # self.viewParts.rootContext().setContextProperty(set_max_categories[0], "0,0,1,0.9")
        # self.viewParts.rootContext().setContextProperty(set_max_categories[1], "0,1,0,0.9")
        # self.viewParts.rootContext().setContextProperty(set_max_categories[2], "1,0,0,0.9")
        # if set_max_categories[0] == set_max_categories[1]:
        #     self.viewParts.rootContext().setContextProperty(set_max_categories[0], "0, 0.7, 0.7, 0.9")
        # if set_max_categories[1] == set_max_categories[2]:
        #     self.viewParts.rootContext().setContextProperty(set_max_categories[1], "0.7, 0.7, 0, 0.9")
        # if set_max_categories[0] == set_max_categories[2]:
        #     self.viewParts.rootContext().setContextProperty(set_max_categories[0], "0.7, 0, 0.7, 0.9")
        # if set_max_categories[0] == set_max_categories[1] and set_max_categories[1] == set_max_categories[2] :
        #     self.viewParts.rootContext().setContextProperty(set_max_categories[0], "0.7, 0.7, 0, 0.9")

    def init_parts(self):
        self.viewParts.rootContext().setContextProperty("HandRight", "0,0,0,0")
        self.viewParts.rootContext().setContextProperty("HandLeft", "0,0,0,0")
        self.viewParts.rootContext().setContextProperty("ElbowRight", "0,0,0,0")
        self.viewParts.rootContext().setContextProperty("ElbowLeft", "0,0,0,0")
        self.viewParts.rootContext().setContextProperty("Head", "0,0,0,0")

    def update_model_frame(self, mui):
        if self.textname == "":
            return -1
        if self.flag_readFile:
            self.setting_textname(self.textname)
            self.flag_readFile = False
        if self.cb_drawFigure.checkState():
            self.updateImage(mui)
            self.updateFigure(mui)

    def loop_update(self, mui, num):
        for i in range(num):
            self.thread_stop = False
            self.updateImage(mui)
            self.updateFigure(mui)
            if self.thread_stop_i > 0:
                self.thread_stop_i = -1
                break
        self.thread_stop = True

    def update_model_frame_last(self, mui):
        if self.textname == "":
            return -1

        ## 1
        import threading
        num = self.maxFrameNum - self.counter
        self.th_me = threading.Thread(target=self.loop_update, name="th_me", args=(mui,num,))
        self.th_me.start()

        ## 2
        self.update_chart()

    def updateImage(self, mui):
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

        if mui.skipDrawCounter():
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

