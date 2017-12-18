from __future__ import with_statement

import numpy as np
import sys
from PyQt5 import QtCore, QtGui
import os
from opencv_test import opencv_test

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

class DesignerMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(DesignerMainWindow, self).__init__(parent)
        #self.setupUi(self)
        #QtCore.QObject.connect(self.file_button, QtCore.SIGNAL("clic＃ked()"), self.open_file)
        # executeボタンクリック時にexe_canny関数を実行
        #QtCore.QObject.connect(self.exec_button, QtCore.SIGNAL("clicked()"), self.exe_canny)

    def open_file(self):
        self.file = QFileDialog.getOpenFileName()
        if self.file:
            self.file_edit.setText(self.file[0])
            self.scene = QtGui.QGraphicsScene()
            pic_Item = QtGui.QGraphicsPixmapItem(QtGui.QPixmap(self.file[0]))
            __width = pic_Item.boundingRect().width()
            __height = pic_Item.boundingRect().height()
            __x = self.pic_View.x()
            __y = self.pic_View.y()
            self.pic_View.setGeometry(QtCore.QRect(__x, __y, __width, __height))

            __main_x = int(__x + __width + 20)
            __main_y = int(__y + __height + 50)
            self.resize(__main_x, __main_y)
            self.scene.addItem(pic_Item)
            self.pic_View.setScene(self.scene)
            return self.file


# exe_canny関数：opecvのcanny処理画像をQtのQPixmapに変換し描画
def exe_canny(self):
    # opencv_testファイルからクラスの読み込み
    cv_test = opencv_test()
    # ファイルを読み込んでRとBを交換
    pic, pic2 = cv_test.open_pic(self.file[0])
    # エッジ検出
    self.cv_img = cv_test.canny(pic2)
    # 画像の高さ、幅を読み込み
    height, width, dim = self.cv_img.shape
    # 全ピクセル数
    bytesPerLine = dim * width
    # Opencv（numpy）画像をQtのQImageに変換
    self.image = QtGui.QImage(self.cv_img.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
    # QImageをQPixmapに変換し、アイテムとして読み込む
    pic_Item = QtGui.QGraphicsPixmapItem(QtGui.QPixmap.fromImage(self.image))
    # 画像を描画
    self.scene.addItem(pic_Item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dmw = DesignerMainWindow()
    dmw.show()
    sys.exit(app.exec_())