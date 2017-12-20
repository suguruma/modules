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
                               QDoubleSpinBox
                             )
from PyQt5.QtQuickWidgets import QQuickWidget


class OperatingTimeWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Operating Time')
        #self.resize(160,240)
        sub_frame = QWidget()

        oprTimeTextLabel = QLabel()
        oprTimeTextLabel.setText('--- Operating Time ---')

        ## h1 line
        stdOprTimeTextLabel = QLabel()
        stdOprTimeTextLabel.setText('Standard :')
        self.stdOprTimeSb = QDoubleSpinBox()
        self.stdOprTimeSb.setSingleStep(0.01)
        self.stdOprTimeSb.setSuffix(" [sec]")
        self.stdOprTimeSb.setValue(3.0)
        self.stdOprTimeSb.valueChanged.connect(self.calcDifferenceOperatingTime)

        ## h2 line
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

        ## h3 line
        differenceTimeTextLabel = QLabel()
        differenceTimeTextLabel.setText('Difference :')
        self.differenceTimeLabel = QLabel()
        self.differenceTimeLabel.setText('x.xxx')

        hbox1 = QHBoxLayout()
        hbox1.addWidget(stdOprTimeTextLabel)
        hbox1.addWidget(self.stdOprTimeSb)
        hbox1.addStretch(1)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(calcOprTimeTextLabel)
        hbox2.addWidget(self.calcOprTimeLabel)
        hbox2.addWidget(extTimeLabel)
        hbox2.addStretch(1)
        hbox2.addWidget(self.fpsSb)
        hbox3 = QHBoxLayout()
        hbox3.addWidget(differenceTimeTextLabel)
        hbox3.addWidget(self.differenceTimeLabel)
        hbox3.addStretch(1)
        vbox1 = QVBoxLayout()
        vbox1.addWidget(oprTimeTextLabel)
        vbox1.addLayout(hbox1)
        vbox1.addLayout(hbox2)
        vbox1.addLayout(hbox3)
        sub_frame.setLayout(vbox1)
        self.setCentralWidget(sub_frame)

    def calcDifferenceOperatingTime(self):
        time = self.stdOprTimeSb.value() - float(self.calcOprTimeLabel.text())
        self.differenceTimeLabel.setText("{0:.2f}[sec]".format(time))
