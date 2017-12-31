import sys
import numpy as np
from collections import deque
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import (Qt, QUrl, QTimer)
from PyQt5.QtGui import (QStandardItemModel, QStandardItem)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
                               QPushButton, QComboBox, QCheckBox, QLabel, QSpinBox, QLineEdit, QListView,
                               QLCDNumber, QSlider, QTableWidget, QTableWidgetItem, QAction, QFileDialog)
from PyQt5.QtQuickWidgets import QQuickWidget

class QMLWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.initUI()

    def initUI(self):
        container = QWidget()
        #container.setMinimumSize(200, 200);
        #container.setMaximumSize(200, 200);
        container.setFocusPolicy(Qt.TabFocus)
        self.view = QQuickWidget()
        self.view.setSource(QUrl("./qml/qmlptviewer/main.qml"))
        self.combo = QComboBox(self)
        self.combo.addItem("qmlptviewer")
        self.combo.addItem("qmlcharttest")
        self.combo.addItem("qmlcustomlegend")
        self.combo.addItem("qmlaxes")
        self.combo.addItem("qmlpolarchart")
        self.combo.addItem("qmlcustominput")
        self.combo.addItem("qmlscatter")
        self.combo.addItem("qmlspectrogram")
        self.combo.currentTextChanged.connect(self.setComboBoxText)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.combo)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.view)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        container.setLayout(vbox)
        self.setCentralWidget(container)

    def setComboBoxText(self):
        self.view.setSource(QUrl("./qml/{0}/main.qml".format(self.combo.currentText())))
