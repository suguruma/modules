import sys
import numpy as np
from collections import deque
from PyQt5.QtCore import (Qt, QUrl, QTimer, QModelIndex, QPoint)
from PyQt5.QtGui import (QStandardItemModel, QStandardItem, QPixmap)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
                               QPushButton, QComboBox, QCheckBox, QLabel, QSpinBox, QLineEdit, QListView,
                               QLCDNumber, QSlider, QTableWidget, QTableWidgetItem, QAction, QFileDialog,
                               QMessageBox
                              )

from image_viewer_ui import UI_MainWindow
from streamer import ImageProcessing
from streamer import CameraStreamer

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        g_verstion = 0.1
        self.setWindowTitle('Viewer ver.{0}'.format(g_verstion))
        self.ui = UI_MainWindow()
        self.ui.setupUi(self)
        self.init()

    def init(self):
        self.VIDEODATA = 0

        self.cam = CameraStreamer()
        self.cam.init()

        # self.cam.set_recoding_mode(0) # 0(movie) or 1(frame)

        # self.cam.videoCameraView()
        # self.cam.frameCameraView()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Close Message', "Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def main(args):
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main(sys.argv)