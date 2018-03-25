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
from streamer import CameraStreamer

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        g_verstion = 0.1
        self.setWindowTitle('Viewer ver.{0}'.format(g_verstion))
        self.init()

        self.ui = UI_MainWindow()
        self.ui.setupUi(self)
        self.controllerUI()
        self.setupInitUI()

    def init(self):
        self.cam = CameraStreamer()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Close Message', "Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    ### UI Controller
    def controllerUI(self):
        self.ui.btn_run.clicked.connect(self.mainUI_btn_run)
        self.ui.combobox_vURL.addItem("0")
        self.ui.combobox_vURL.addItem("http://10.232.163.38/mjpg/1/video.mjpg")
        self.ui.combobox_vURL.addItem("http://10.232.163.38/jpg/1/image.jpg")
        self.ui.combobox_vURL.addItem("http://10.232.168.41/-wvhttp-01-/GetOneShot")
        self.ui.combobox_vURL.currentTextChanged.connect(self.mainUI_combobox)
        self.ui.cb_resize.stateChanged.connect(self.resize_checkbox)
        self.ui.cb_imgproc.stateChanged.connect(self.img_proc_checkbox)
        self.ui.cb_data_mode.addItem("Video")
        self.ui.cb_data_mode.addItem("Frame")

    def setupInitUI(self):
        self.mainUI_combobox()

    ### UI Method
    def mainUI_combobox(self):
        self.ui.ledit_vURL.setText(self.ui.combobox_vURL.currentText())

    def resize_checkbox(self):
        self.cam.resize_on = self.ui.cb_resize.isChecked()

    def img_proc_checkbox(self):
        self.cam.img_proc_on = self.ui.cb_imgproc.isChecked()

    ### Main
    def mainUI_btn_run(self):
        if(self.ui.ledit_vURL.text().isdigit()):
            self.VIDEOURL = int(self.ui.ledit_vURL.text())
        else:
            self.VIDEOURL = self.ui.ledit_vURL.text()
        self.run()

    def run(self):
        self.cam.init()
        self.cam.set_size(self.ui.sb_width.value(), self.ui.sb_height.value())
        self.cam.set_sensor(self.VIDEOURL)
        self.cam.set_recoding_mode(self.ui.sb_recordingMode.value())

        if self.ui.cb_data_mode.currentText() == "Video":
            self.cam.videoCameraView()
        if self.ui.cb_data_mode.currentText() == "Frame":
            self.cam.frameCameraView()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())