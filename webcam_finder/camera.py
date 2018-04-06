#!/usr/bin/env python
from PyQt5.QtCore import QByteArray
from PyQt5.QtMultimedia import QCamera
from PyQt5.QtMultimediaWidgets import QCameraViewfinder

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QAction, QActionGroup, QApplication, QMainWindow, QMessageBox

class Ui_Camera(object):
    def setupUi(self, Camera):
        Camera.setObjectName("Camera")
        self.centralwidget = QtWidgets.QWidget(Camera)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_main = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_main.setObjectName("gridLayout_main")

        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.viewfinderPage = QtWidgets.QWidget()
        self.viewfinderPage.setObjectName("viewfinderPage")
        self.gridLayout_sub = QtWidgets.QGridLayout(self.viewfinderPage)
        self.gridLayout_sub.setObjectName("gridLayout_sub")
        self.viewfinder = QCameraViewfinder(self.viewfinderPage)
        self.viewfinder.setObjectName("viewfinder")
        self.gridLayout_sub.addWidget(self.viewfinder, 0, 0)
        self.stackedWidget.addWidget(self.viewfinderPage)
        self.gridLayout_main.addWidget(self.stackedWidget, 0, 0)

        Camera.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Camera)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuDevices = QtWidgets.QMenu(self.menubar)
        self.menuDevices.setObjectName("menuDevices")
        Camera.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Camera)
        self.statusbar.setObjectName("statusbar")
        Camera.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(Camera)
        self.actionExit.setObjectName("actionExit")
        self.actionStartCamera = QtWidgets.QAction(Camera)
        self.actionStartCamera.setObjectName("actionStartCamera")
        self.actionStopCamera = QtWidgets.QAction(Camera)
        self.actionStopCamera.setObjectName("actionStopCamera")
        self.menuFile.addAction(self.actionStartCamera)
        self.menuFile.addAction(self.actionStopCamera)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDevices.menuAction())

        self.retranslateUi(Camera)
        self.stackedWidget.setCurrentIndex(0)
        self.actionStartCamera.triggered.connect(Camera.startCamera)
        self.actionStopCamera.triggered.connect(Camera.stopCamera)
        QtCore.QMetaObject.connectSlotsByName(Camera)

    def retranslateUi(self, Camera):
        _translate = QtCore.QCoreApplication.translate
        Camera.setWindowTitle(_translate("Camera", "Camera"))
        self.menuFile.setTitle(_translate("Camera", "File"))
        self.menuDevices.setTitle(_translate("Camera", "Devices"))
        self.actionExit.setText(_translate("Camera", "Exit"))
        self.actionStartCamera.setText(_translate("Camera", "Start Camera"))
        self.actionStopCamera.setText(_translate("Camera", "Stop Camera"))

class Camera(QMainWindow):

    def __init__(self, parent=None):
        super(Camera, self).__init__(parent)

        self.ui = Ui_Camera()
        self.camera = None
        self.imageCapture = None
        self.isCapturingImage = False
        self.applicationExiting = False
        self.ui.setupUi(self)

        cameraDevice = QByteArray()
        videoDevicesGroup = QActionGroup(self)
        videoDevicesGroup.setExclusive(True)

        for deviceName in QCamera.availableDevices():
            description = QCamera.deviceDescription(deviceName)
            videoDeviceAction = QAction(description, videoDevicesGroup)
            videoDeviceAction.setCheckable(True)
            videoDeviceAction.setData(deviceName)

            if cameraDevice.isEmpty():
                cameraDevice = deviceName
                videoDeviceAction.setChecked(True)
            self.ui.menuDevices.addAction(videoDeviceAction)

        videoDevicesGroup.triggered.connect(self.updateCameraDevice)
        self.setCamera(cameraDevice)

    def setCamera(self, cameraDevice):
        if cameraDevice.isEmpty():
            self.camera = QCamera()
        else:
            self.camera = QCamera(cameraDevice)

        self.camera.stateChanged.connect(self.updateCameraState)
        self.camera.error.connect(self.displayCameraError)
        self.camera.setViewfinder(self.ui.viewfinder)
        self.updateCameraState(self.camera.state())
        self.camera.start()

    def startCamera(self):
        self.camera.start()

    def stopCamera(self):
        self.camera.stop()

    def updateCameraState(self, state):
        if state == QCamera.ActiveState:
            self.ui.actionStartCamera.setEnabled(False)
            self.ui.actionStopCamera.setEnabled(True)
        elif state in (QCamera.UnloadedState, QCamera.LoadedState):
            self.ui.actionStartCamera.setEnabled(True)
            self.ui.actionStopCamera.setEnabled(False)

    def displayCameraError(self):
        QMessageBox.warning(self, "Camera error", self.camera.errorString())

    def updateCameraDevice(self, action):
        self.setCamera(action.data())

    def closeEvent(self, event):
        if self.isCapturingImage:
            self.setEnabled(False)
            self.applicationExiting = True
            event.ignore()
        else:
            event.accept()

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    camera = Camera()
    camera.show()
    sys.exit(app.exec_())