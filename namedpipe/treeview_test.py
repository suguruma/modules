#!/usr/bin/env python
import sys
import os
import numpy as np
from collections import deque

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt, QTimer)
from PyQt5.QtGui import (QStandardItemModel, QStandardItem)
from PyQt5.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QGridLayout, QVBoxLayout, QHBoxLayout, QSizePolicy,
                             QLabel, QLineEdit, QPushButton)
from PyQt5.QtWidgets import (QAbstractItemView, QWidget,  QListView, QListWidget,QTreeView, QFileSystemModel,
                             QTableWidget, QTableWidgetItem, QAction, QComboBox, QSpinBox, QFileDialog)


class MyTreeView(QTreeView):
    def __init__(self,parent=None):
        super(MyTreeView,self).__init__(parent)
        model = QFileSystemModel()
        model.setRootPath('')
        self.setModel(model)
        self.setRootIndex(model.index(os.path.expanduser('~')))

def main():
    app = QApplication(sys.argv)

    view = MyTreeView()
    view.show()

    app.exec_()

class MyListWidget(QListWidget):
    def __init__(self,parent=None):
        super(MyListWidget,self).__init__(parent)
        self.addItem('first row')
        self.addItem('second row')


def main1():
    app = QApplication(sys.argv)

    view = MyListWidget()
    view.show()

    app.exec_()


class MyListWidget2(QListWidget):
    def __init__(self,parent=None):
        super(MyListWidget2,self).__init__(parent)
        self.model = QStandardItemModel(self)
        self.view = QListView(self)
        self.view.setModel(self.model)
        self.model.appendRow(QStandardItem('first row2'))
        self.model.appendRow(QStandardItem('second row2'))

def main2():
    app = QApplication(sys.argv)

    view = MyListWidget2()
    view.show()

    app.exec_()

class MyListWidget3(QListWidget):
    def __init__(self, parent=None):
        super(MyListWidget3, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)

    def dragEnterEvent(self, event):
        print("dragE")

    def dragMoveEvent(self, event):
        print("dragM")

    def dropEvent(self, event):
        print("dropE")

def main3():
    app = QApplication(sys.argv)

    view = MyListWidget3()
    view.show()

    app.exec_()

if __name__ == '__main__':
    main3()