#!/usr/bin/env python
import sys
import numpy as np
from collections import deque
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import (Qt, QUrl, QTimer)
from PyQt5.QtGui import (QStandardItemModel, QStandardItem, QPainter, QImage, QPixmap)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
                               QPushButton, QComboBox, QCheckBox, QLabel, QSpinBox, QLineEdit, QListView,
                               QLCDNumber, QSlider, QTableWidget, QTableWidgetItem, QAction, QFileDialog)
from PyQt5.QtQuickWidgets import QQuickWidget

#from PyQt5.QtGui import QGuiApplication
#from PyQt5.QtCore import (QLineF, QPointF, QRectF)
#from PyQt5.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsItem, QListWidget)
#from PyQt5.QtQuick import QQuickView
#from PyQt5.QtQml import QQmlApplicationEngine

from mypackage.plotdisplay_test import MainPlotWindow
from mypackage.qmldisplay_test import QMLWindow
from mypackage.subdisplay_test import SubWindow

def create_QPixmap(image):
  qimage = QImage(image.data, image.shape[1], image.shape[0], image.shape[1] * 4, QImage.Format_ARGB32_Premultiplied)
  pixmap = QPixmap.fromImage(image)
  return pixmap

class ImageWidget(QWidget):
  def __init__(self, image):
    super(ImageWidget, self).__init__()
    self.image = image

  def paintEvent(self, event):
    painter = QPainter(self)
    if self.image is None:
      painter.setPen(Qt.black)
      painter.setBrush(Qt.black)
      painter.drawRect(0, 0, self.width(), self.height())
      return
    pixmap = create_QPixmap(self.image)
    painter.drawPixmap(0, 0, self.image.shape[1], self.image.shape[0], pixmap)

  def set_image(self, image):
    self.image = image
    self.update()

def main(args):
    app = QApplication(sys.argv)
    mainWindow = ImageWidget()

    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main(sys.argv)
