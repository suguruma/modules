import sys
import numpy as np
from collections import deque
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import (Qt, QUrl, QTimer)
from PyQt5.QtGui import (QStandardItemModel, QStandardItem)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
                               QPushButton, QComboBox, QCheckBox, QLabel, QSpinBox, QLineEdit, QListView,
                               QLCDNumber, QSlider, QTableWidget, QTableWidgetItem, QAction, QFileDialog,
                               QDoubleSpinBox, QGroupBox, QSizePolicy
                             )
from PyQt5.QtQuickWidgets import QQuickWidget

class OperatingTimeWindow(QMainWindow):
    def setupUI(self, mui):
        #QMainWindow.__init__(self, parent)
        self.initUI(mui)
        self.mainUI(mui)
        self.timeUI()
        self.thresholdUI(mui)

    def initUI(self, mui):
        self.gb_oprTime = QGroupBox()
        mui.gb_setThreshold = QGroupBox()
        mui.gb_setThreshold.setVisible(False)

    def mainUI(self, mui):
        self.setWindowTitle('Operating Time')
        self.setGeometry(1300, 400, 0, 0);
        main_frame = QWidget()
        vbox_main = QVBoxLayout()
        vbox_main.addWidget(self.gb_oprTime)
        vbox_main.addWidget(mui.gb_setThreshold)
        main_frame.setLayout(vbox_main)
        self.setCentralWidget(main_frame)

    def timeUI(self):
        ### Add Element
        stdOprTimeTextLabel = QLabel()
        stdOprTimeTextLabel.setText('Standard :')
        self.stdOprTimeSb = QDoubleSpinBox()
        self.stdOprTimeSb.setSingleStep(0.01)
        self.stdOprTimeSb.setSuffix(" [sec]")
        self.stdOprTimeSb.setValue(3.0)
        self.stdOprTimeSb.valueChanged.connect(self.calcDifferenceOperatingTime)
        calcOprTimeTextLabel = QLabel()
        calcOprTimeTextLabel.setText('Calculation :')
        self.calcOprTimeLabel = QLabel()
        self.calcOprTimeLabel.setText('x.xxx')
        extTimeLabel = QLabel()
        extTimeLabel.setText("[sec]")
        self.fpsSb = QSpinBox()
        self.fpsSb.setValue(30)
        self.fpsSb.setPrefix("fps: ")
        self.fpsSb.setRange(1, 150)
        differenceTimeTextLabel = QLabel()
        differenceTimeTextLabel.setText('Difference :')
        self.differenceTimeLabel = QLabel()
        self.differenceTimeLabel.setText('x.xxx')

        ### -1-
        hbox1 = QHBoxLayout()
        hbox1.addWidget(stdOprTimeTextLabel)
        hbox1.addWidget(self.stdOprTimeSb)
        hbox1.addStretch(1)
        ### -2-
        hbox2 = QHBoxLayout()
        hbox2.addWidget(calcOprTimeTextLabel)
        hbox2.addWidget(self.calcOprTimeLabel)
        hbox2.addWidget(extTimeLabel)
        hbox2.addWidget(self.fpsSb)
        hbox2.addStretch(1)
        ### -3-
        hbox3 = QHBoxLayout()
        hbox3.addWidget(differenceTimeTextLabel)
        hbox3.addWidget(self.differenceTimeLabel)
        hbox3.addStretch(1)
        ### |-1-2-3-|
        vbox_gb_oprTime = QVBoxLayout()
        vbox_gb_oprTime.addLayout(hbox1)
        vbox_gb_oprTime.addLayout(hbox2)
        vbox_gb_oprTime.addLayout(hbox3)

        self.gb_oprTime.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gb_oprTime.setTitle("Operating Time")
        self.gb_oprTime.setLayout(vbox_gb_oprTime)

    def thresholdUI(self, mui):
        ### Add Element
        mui.th_sldv_baseX_qsb = QSpinBox()
        mui.th_sldv_baseX_qsb.setRange(1, 1000)
        mui.th_sldv_baseX_qsb.setValue(20)
        mui.th_sldv_baseY_qsb = QSpinBox()
        mui.th_sldv_baseY_qsb.setRange(1, 1000)
        mui.th_sldv_baseY_qsb.setValue(20)
        mui.th_sldv_baseZ_qsb = QSpinBox()
        mui.th_sldv_baseZ_qsb.setRange(1, 1000)
        mui.th_sldv_baseZ_qsb.setValue(20)

        mui.th_sldvX = QSlider(Qt.Vertical)
        mui.th_sldvX.setRange(-50, 50)
        mui.th_sldvX.setValue(0)
        mui.th_sldvXqsb = QSpinBox()
        mui.th_sldvXqsb.setRange(-50, 50)
        mui.th_sldvXqsb.setValue(mui.th_sldvX.value())
        mui.th_sldvX.valueChanged.connect(mui.setGraphParameter)
        mui.th_sldvX.valueChanged.connect(mui.refreshGraphSlider)

        mui.th_sldvY = QSlider(Qt.Vertical)
        mui.th_sldvY.setRange(-50, 50)
        mui.th_sldvY.setValue(0)
        mui.th_sldvYqsb = QSpinBox()
        mui.th_sldvYqsb.setRange(-50, 50)
        mui.th_sldvYqsb.setValue(mui.th_sldvY.value())
        mui.th_sldvY.valueChanged.connect(mui.setGraphParameter)
        mui.th_sldvY.valueChanged.connect(mui.refreshGraphSlider)

        mui.th_sldvZ = QSlider(Qt.Vertical)
        mui.th_sldvZ.setRange(-50, 50)
        mui.th_sldvZ.setValue(0)
        mui.th_sldvZqsb = QSpinBox()
        mui.th_sldvZqsb.setRange(-50, 50)
        mui.th_sldvZqsb.setValue(mui.th_sldvZ.value())
        mui.th_sldvZ.valueChanged.connect(mui.setGraphParameter)
        mui.th_sldvZ.valueChanged.connect(mui.refreshGraphSlider)


        ###
        mui.th_varianceXqsb = QSpinBox()
        mui.th_varianceXqsb.setRange(0, 1000)
        mui.th_varianceXqsb.valueChanged.connect(mui.refreshGraphSpinBox)
        mui.th_varianceYqsb = QSpinBox()
        mui.th_varianceYqsb.setRange(0, 1000)
        mui.th_varianceYqsb.valueChanged.connect(mui.refreshGraphSpinBox)
        mui.th_varianceZqsb = QSpinBox()
        mui.th_varianceZqsb.setRange(0, 1000)
        mui.th_varianceZqsb.valueChanged.connect(mui.refreshGraphSpinBox)

        ### |1|
        vbox1 = QVBoxLayout()
        vbox1.addWidget(mui.th_sldvXqsb)
        vbox1.addWidget(mui.th_sldvX)
        vbox1.addWidget(mui.th_sldv_baseX_qsb)
        vbox1.addWidget(mui.th_varianceXqsb)
        ### |2|
        vbox2 = QVBoxLayout()
        vbox2.addWidget(mui.th_sldvYqsb)
        vbox2.addWidget(mui.th_sldvY)
        vbox2.addWidget(mui.th_sldv_baseY_qsb)
        vbox2.addWidget(mui.th_varianceYqsb)
        ### |3|
        vbox3 = QVBoxLayout()
        vbox3.addWidget(mui.th_sldvZqsb)
        vbox3.addWidget(mui.th_sldvZ)
        vbox3.addWidget(mui.th_sldv_baseZ_qsb)
        vbox3.addWidget(mui.th_varianceZqsb)
        ### -|1|2|3|-
        hbox_gb_setThreshold = QHBoxLayout()
        hbox_gb_setThreshold.addLayout(vbox1)
        hbox_gb_setThreshold.addLayout(vbox2)
        hbox_gb_setThreshold.addLayout(vbox3)

        mui.gb_setThreshold.setMinimumHeight(500)
        mui.gb_setThreshold.setVisible(True)
        mui.gb_setThreshold.setTitle("Setting Threshold")
        mui.gb_setThreshold.setLayout(hbox_gb_setThreshold)

    def calcDifferenceOperatingTime(self):
        time = self.stdOprTimeSb.value() - float(self.calcOprTimeLabel.text())
        self.differenceTimeLabel.setText("{0:.2f}[sec]".format(time))
