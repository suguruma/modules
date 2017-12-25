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
        self.setGeometry(1350, 100, 0, 0);
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
        mui.cb_thX1_on =QCheckBox("X1")
        mui.cb_thX2_on =QCheckBox("X2")
        mui.cb_thY1_on =QCheckBox("Y1")
        mui.cb_thY2_on =QCheckBox("Y2")
        mui.cb_thZ1_on =QCheckBox("Z1")
        mui.cb_thZ2_on =QCheckBox("Z2")
        ## X
        mui.sld_thX1 = QSlider(Qt.Vertical)
        mui.sld_thX1.setRange(-50, 50)
        mui.sld_thX1.setValue(0)
        mui.sb_thX1 = QSpinBox()
        mui.sb_thX1.setRange(-50, 50)
        mui.sb_thX1.setValue(mui.sld_thX1.value())
        mui.sld_thX1.valueChanged.connect(mui.setGraphParameter)
        mui.sld_thX1.valueChanged.connect(mui.refreshGraphSlider)
        mui.sb_thX1Variance = QSpinBox()
        mui.sb_thX1Variance.setRange(0, 1000)
        mui.sb_thX1Variance.valueChanged.connect(mui.refreshGraphSpinBox)
        mui.sld_thX2 = QSlider(Qt.Vertical)
        mui.sld_thX2.setRange(-50, 50)
        mui.sld_thX2.setValue(0)
        mui.sb_thX2 = QSpinBox()
        mui.sb_thX2.setRange(-50, 50)
        mui.sb_thX2.setValue(mui.sld_thX1.value())
        mui.sld_thX2.valueChanged.connect(mui.setGraphParameter)
        mui.sld_thX2.valueChanged.connect(mui.refreshGraphSlider)
        mui.sb_thX2Variance = QSpinBox()
        mui.sb_thX2Variance.setRange(0, 1000)
        mui.sb_thX2Variance.valueChanged.connect(mui.refreshGraphSpinBox)
        ## Y
        mui.sld_thY1 = QSlider(Qt.Vertical)
        mui.sld_thY1.setRange(-50, 50)
        mui.sld_thY1.setValue(0)
        mui.sb_thY1 = QSpinBox()
        mui.sb_thY1.setRange(-50, 50)
        mui.sb_thY1.setValue(mui.sld_thY1.value())
        mui.sld_thY1.valueChanged.connect(mui.setGraphParameter)
        mui.sld_thY1.valueChanged.connect(mui.refreshGraphSlider)
        mui.sb_thY1Variance = QSpinBox()
        mui.sb_thY1Variance.setRange(0, 1000)
        mui.sb_thY1Variance.valueChanged.connect(mui.refreshGraphSpinBox)
        mui.sld_thY2 = QSlider(Qt.Vertical)
        mui.sld_thY2.setRange(-50, 50)
        mui.sld_thY2.setValue(0)
        mui.sb_thY2 = QSpinBox()
        mui.sb_thY2.setRange(-50, 50)
        mui.sb_thY2.setValue(mui.sld_thY1.value())
        mui.sld_thY2.valueChanged.connect(mui.setGraphParameter)
        mui.sld_thY2.valueChanged.connect(mui.refreshGraphSlider)
        mui.sb_thY2Variance = QSpinBox()
        mui.sb_thY2Variance.setRange(0, 1000)
        mui.sb_thY2Variance.valueChanged.connect(mui.refreshGraphSpinBox)
        ##Z
        mui.sld_thZ1 = QSlider(Qt.Vertical)
        mui.sld_thZ1.setRange(-50, 50)
        mui.sld_thZ1.setValue(0)
        mui.sb_thZ1 = QSpinBox()
        mui.sb_thZ1.setRange(-50, 50)
        mui.sb_thZ1.setValue(mui.sld_thZ1.value())
        mui.sld_thZ1.valueChanged.connect(mui.setGraphParameter)
        mui.sld_thZ1.valueChanged.connect(mui.refreshGraphSlider)
        mui.sb_thZ1Variance = QSpinBox()
        mui.sb_thZ1Variance.setRange(0, 1000)
        mui.sb_thZ1Variance.valueChanged.connect(mui.refreshGraphSpinBox)
        mui.sld_thZ2 = QSlider(Qt.Vertical)
        mui.sld_thZ2.setRange(-50, 50)
        mui.sld_thZ2.setValue(0)
        mui.sb_thZ2 = QSpinBox()
        mui.sb_thZ2.setRange(-50, 50)
        mui.sb_thZ2.setValue(mui.sld_thZ2.value())
        mui.sld_thZ2.valueChanged.connect(mui.setGraphParameter)
        mui.sld_thZ2.valueChanged.connect(mui.refreshGraphSlider)
        mui.sb_thZ2Variance = QSpinBox()
        mui.sb_thZ2Variance.setRange(0, 1000)
        mui.sb_thZ2Variance.valueChanged.connect(mui.refreshGraphSpinBox)

        #
        lbl_scaleX = QLabel('scale X:')
        lbl_scaleY = QLabel('scale Y:')
        lbl_scaleZ = QLabel('scale Z:')
        mui.sb_thX_scale = QDoubleSpinBox()
        mui.sb_thX_scale.setRange(0.01, 100)
        mui.sb_thX_scale.setValue(0.05)
        mui.sb_thX_scale.setSingleStep(0.01)
        mui.sb_thY_scale = QDoubleSpinBox()
        mui.sb_thY_scale.setRange(0.01, 100)
        mui.sb_thY_scale.setValue(0.05)
        mui.sb_thY_scale.setSingleStep(0.01)
        mui.sb_thZ_scale = QDoubleSpinBox()
        mui.sb_thZ_scale.setRange(0.01, 100)
        mui.sb_thZ_scale.setValue(0.05)
        mui.sb_thZ_scale.setSingleStep(0.01)

        ### -1-
        hbox1 = QHBoxLayout()
        hbox1.addWidget(lbl_scaleX)
        hbox1.addWidget(mui.sb_thX_scale)
        hbox1.addWidget(lbl_scaleY)
        hbox1.addWidget(mui.sb_thY_scale)
        hbox1.addWidget(lbl_scaleZ)
        hbox1.addWidget(mui.sb_thZ_scale)

        ### |1|
        vbox1 = QVBoxLayout()
        vbox1.addWidget(mui.cb_thX1_on)
        vbox1.addWidget(mui.sb_thX1)
        vbox1.addWidget(mui.sld_thX1)
        vbox1.addWidget(mui.sb_thX1Variance)
        vbox1_2 = QVBoxLayout()
        vbox1_2.addWidget(mui.cb_thX2_on)
        vbox1_2.addWidget(mui.sb_thX2)
        vbox1_2.addWidget(mui.sld_thX2)
        vbox1_2.addWidget(mui.sb_thX2Variance)
        ### |2|
        vbox2 = QVBoxLayout()
        vbox2.addWidget(mui.cb_thY1_on)
        vbox2.addWidget(mui.sb_thY1)
        vbox2.addWidget(mui.sld_thY1)
        vbox2.addWidget(mui.sb_thY1Variance)
        vbox2_2 = QVBoxLayout()
        vbox2_2.addWidget(mui.cb_thY2_on)
        vbox2_2.addWidget(mui.sb_thY2)
        vbox2_2.addWidget(mui.sld_thY2)
        vbox2_2.addWidget(mui.sb_thY2Variance)
        ### |3|
        vbox3 = QVBoxLayout()
        vbox3.addWidget(mui.cb_thZ1_on)
        vbox3.addWidget(mui.sb_thZ1)
        vbox3.addWidget(mui.sld_thZ1)
        vbox3.addWidget(mui.sb_thZ1Variance)
        vbox3_2 = QVBoxLayout()
        vbox3_2.addWidget(mui.cb_thZ2_on)
        vbox3_2.addWidget(mui.sb_thZ2)
        vbox3_2.addWidget(mui.sld_thZ2)
        vbox3_2.addWidget(mui.sb_thZ2Variance)
        ### -2|1|2|3|-
        hbox2 = QHBoxLayout()
        hbox2.addLayout(vbox1)
        hbox2.addLayout(vbox1_2)
        hbox2.addLayout(vbox2)
        hbox2.addLayout(vbox2_2)
        hbox2.addLayout(vbox3)
        hbox2.addLayout(vbox3_2)

        ### |-1-2-|
        vbox_gb_setThreshold = QVBoxLayout()
        vbox_gb_setThreshold.addLayout(hbox1)
        vbox_gb_setThreshold.addLayout(hbox2)

        mui.gb_setThreshold.setMinimumHeight(500)
        mui.gb_setThreshold.setVisible(True)
        mui.gb_setThreshold.setTitle("Setting Threshold")
        mui.gb_setThreshold.setLayout(vbox_gb_setThreshold)

    def calcDifferenceOperatingTime(self):
        time = self.stdOprTimeSb.value() - float(self.calcOprTimeLabel.text())
        self.differenceTimeLabel.setText("{0:.2f}[sec]".format(time))
