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
from mypackage.uidisplay import UI_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.setWindowTitle('Time Seriese Analysis ver.0.1')
        self.setGeometry(400, 100, 0, 0);
        self.setParameter()
        self.ui = UI_MainWindow()
        self.ui.setupUi(self)

        ### Key Acitivity
        self.keyfunc = KeyActivityTime()
        self.timeWindow = OperatingTimeWindow()
        self.timeWindow.show()

        ### Check Features
        self.featuresWindow = FeaturesWindow()

    def setParameter(self):
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

        ### Activity Parameter
        self.flagKeyActiveX = False
        self.flagKeyActiveY = False
        self.flagKeyActiveZ = False

    ### image
    def changeImageSize(self):
        self.lbl_image.setFixedSize(self.spb_imgWidth.value(), self.spb_imgHeight.value())
    def isDisplayImageInfomation(self):
        self.gb_imageInfo.setVisible(self.cb_imgDisplay.checkState())

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
        self.le_imgPath.setText(self.imageFolder)

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
        self.frameNumbSpb.setValue(self.sld_frameNum.value())
        if not self.runOn:
            self.update_plot_data()

    def refreshGraphSlider(self):
        self.sldv1.setValue(self.sldv1qsb.value())
        self.sldv2.setValue(self.sldv2qsb.value())
        self.sldh1.setValue(self.sldh1qsb.value())
        self.sldh2.setValue(self.sldh2qsb.value())
        self.pltnum_sld.setValue(self.pltnum_qsb.value())
        self.sld_frameNum.setMaximum(self.pltnum_qsb.value())
        self.sld_frameNum.setValue(self.frameNumbSpb.value())
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