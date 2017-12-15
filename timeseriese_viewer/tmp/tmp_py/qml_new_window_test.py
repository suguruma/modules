#!/usr/bin/env python
import sys
import numpy as np
from collections import deque

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt, QUrl, QTimer, QObject)
from PyQt5.QtGui import (QStandardItemModel, QStandardItem, QGuiApplication)
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QGridLayout, QVBoxLayout, QHBoxLayout, QListView,
                             QLabel, QLineEdit, QPushButton)
from PyQt5.QtWidgets import (QMainWindow, QWidget, QLCDNumber, QSlider, QListWidget, QCheckBox,
                             QTableWidget, QTableWidgetItem, QAction, QComboBox, QSpinBox, QFileDialog)
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQuickWidgets import QQuickWidget
from PyQt5.QtQml import QQmlApplicationEngine

class QMLMainWindow(QQmlApplicationEngine):
    def __init__(self, parent=None):
        QQmlApplicationEngine.__init__(self, parent)
        self.initUI()

    def initUI(self):
        self.load(QUrl("test.qml"))
        #self.rootObjects()[0]

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    form = QMLMainWindow()
    sys.exit(app.exec_())

