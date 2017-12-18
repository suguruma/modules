#!/usr/bin/env python
import sys
import numpy as np
from collections import deque
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import (Qt, QUrl, QTimer)
from PyQt5.QtGui import (QStandardItemModel, QStandardItem, QPainter, QImage, QPixmap, QColor)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
                               QPushButton, QComboBox, QCheckBox, QLabel, QSpinBox, QLineEdit, QListView,
                               QLCDNumber, QSlider, QTableWidget, QTableWidgetItem, QAction, QFileDialog)
from PyQt5.QtQuickWidgets import QQuickWidget

class Sample(QMainWindow):
    def __init__(self, parent = None):
        super(Sample, self).__init__(parent)


    def paintEvent(self,event):
        painter = QPainter()
        painter.begin(self)
        #painter.setPen(QColor('#FFFFFF'))
        #painter.setBrush(Qt.white)
        #painter.drawRect(event.rect())

        image = QImage('./lena.png')
        x = (self.width() - image.width()) / 2
        y = (self.height() - image.height()) / 2

        painter.drawImage(x,y,image)
        painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sample = Sample()
    sample.show()
    sys.exit(app.exec_())