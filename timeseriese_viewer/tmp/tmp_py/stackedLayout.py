# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 19:03:06 2017

@author: Terada
"""
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
                               QDoubleSpinBox, QGroupBox, QSizePolicy, QMessageBox, QDialog, QStackedLayout
                              )

class MyLayoutDialog(QDialog):
        def __init__(self, parent=None):
                super(MyLayoutDialog, self).__init__(parent)
                self.setWindowTitle("My Layout Dialog")
                
                # ページとして並べるウィジェットを作成
                labelA = QLabel("Label A")
                labelB = QLabel("Label B")
                labelC = QLabel("Label C")
                
                # ページ切り替え用コンボボックス
                combo = QComboBox()
                combo.addItem('Page A')
                combo.addItem('Page B')
                combo.addItem('Page C')

                # ページを追加していく
                layout = QStackedLayout()
                layout.addWidget(labelA)
                layout.addWidget(labelB)
                layout.addWidget(labelC)

                # コンボボックスの切り替えでページを切り替えるようシグナルとスロットを接続
                combo.currentIndexChanged.connect(layout.setCurrentIndex)

                #  ページ切り替え用コンボボックスとスタックレイアウトを垂直方向に並べる
                vLayout = QVBoxLayout()
                vLayout.addWidget(combo)
                vLayout.addLayout(layout)
                self.setLayout(vLayout)

if __name__ == '__main__':
        app = QApplication(sys.argv)
        ui = MyLayoutDialog()
        ui.show()
        app.exec_()