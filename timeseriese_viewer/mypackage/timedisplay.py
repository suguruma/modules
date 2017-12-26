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
                               QDoubleSpinBox, QGroupBox, QSizePolicy
                             )
from PyQt5.QtQuickWidgets import QQuickWidget
from configparser import ConfigParser

class OperatingTimeWindow(QMainWindow):
    def setupUI(self, mui):
        self.initUI(mui)
        self.mainUI(mui)
        self.configUI(mui)
        self.timeUI()
        self.thresholdUI(mui)

    def initUI(self, mui):
        self.gb_config = QGroupBox()
        self.gb_oprTime = QGroupBox()
        mui.gb_setThreshold = QGroupBox()
        mui.gb_setThreshold.setVisible(False)

    def mainUI(self, mui):
        self.setWindowTitle('Operating Time Calclation')
        self.setGeometry(1350, 100, 0, 0);
        self.setMinimumWidth(350)
        main_frame = QWidget()
        vbox_main = QVBoxLayout()
        vbox_main.addWidget(self.gb_config)
        vbox_main.addWidget(self.gb_oprTime)
        vbox_main.addWidget(mui.gb_setThreshold)
        vbox_main.addStretch(1)
        main_frame.setLayout(vbox_main)
        self.setCentralWidget(main_frame)

    def configUI(self, mui):
        btn_readConfig = QPushButton('Read')
        btn_readConfig.clicked.connect(lambda : self.readConfig(mui))
        self.le_readConfig = QLineEdit()
        btn_saveConfig = QPushButton('Save')
        btn_saveConfig.clicked.connect(lambda : self.saveConfig(mui))
        self.le_saveConfig = QLineEdit()
        self.cb_DisplayThresholdUI = QCheckBox('Display Setting Threshold Form')
        self.cb_DisplayThresholdUI.setChecked(False)
        self.cb_DisplayThresholdUI.stateChanged.connect(lambda : self.displayThresholdWindow(mui))

        ### -1-
        hbox1 = QHBoxLayout()
        hbox1.addWidget(btn_readConfig)
        hbox1.addWidget(self.le_readConfig)
        ### -2-
        hbox2 = QHBoxLayout()
        hbox2.addWidget(btn_saveConfig)
        hbox2.addWidget(self.le_saveConfig)
        ### |-1-2-|
        vbox_gb_config = QVBoxLayout()
        vbox_gb_config.addLayout(hbox1)
        vbox_gb_config.addLayout(hbox2)
        vbox_gb_config.addWidget(self.cb_DisplayThresholdUI)

        self.gb_config.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.gb_config.setTitle("Config File")
        self.gb_config.setLayout(vbox_gb_config)

    def timeUI(self):
        ### Add Element
        stdOprTimeTextLabel = QLabel()
        stdOprTimeTextLabel.setText('Standard :')
        self.stdOprTimeSb = QDoubleSpinBox()
        self.stdOprTimeSb.setSingleStep(0.01)
        self.stdOprTimeSb.setSuffix(" [sec]")
        self.stdOprTimeSb.setValue(3.0)
        self.stdOprTimeSb.valueChanged.connect(self.calcDifferenceOperatingTime)
        calcOprTimeTextLabel = QLabel()
        calcOprTimeTextLabel.setText('Calculation :')
        self.calcOprTimeLabel = QLabel()
        self.calcOprTimeLabel.setText('0.000')
        extTimeLabel = QLabel()
        extTimeLabel.setText("[sec]")
        self.fpsSb = QSpinBox()
        self.fpsSb.setValue(30)
        self.fpsSb.setPrefix("fps: ")
        self.fpsSb.setRange(1, 150)
        differenceTimeTextLabel = QLabel()
        differenceTimeTextLabel.setText('Difference :')
        self.differenceTimeLabel = QLabel()
        self.differenceTimeLabel.setText('x.xxx')
        self.cb_saveOprTime = QCheckBox('Save:')
        self.le_filepath = QLineEdit()
        self.le_filepath.setText("CSV File")
        self.btn_save_fd = QPushButton('...')
        self.btn_save_fd.clicked.connect(self.setSaveTimeFilePath)
        self.btn_save_fd.setFixedWidth(30)

        ### -1-
        hbox1 = QHBoxLayout()
        hbox1.addWidget(stdOprTimeTextLabel)
        hbox1.addWidget(self.stdOprTimeSb)
        hbox1.addStretch(1)
        ### -2-
        hbox2 = QHBoxLayout()
        hbox2.addWidget(calcOprTimeTextLabel)
        hbox2.addWidget(self.calcOprTimeLabel)
        hbox2.addWidget(extTimeLabel)
        hbox2.addWidget(self.fpsSb)
        hbox2.addStretch(1)
        ### -3-
        hbox3 = QHBoxLayout()
        hbox3.addWidget(differenceTimeTextLabel)
        hbox3.addWidget(self.differenceTimeLabel)
        hbox3.addStretch(1)
        ### -4-
        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.cb_saveOprTime)
        hbox4.addWidget(self.le_filepath)
        hbox4.addWidget(self.btn_save_fd)

        ### |-1-2-3-|
        vbox_gb_oprTime = QVBoxLayout()
        vbox_gb_oprTime.addLayout(hbox1)
        vbox_gb_oprTime.addLayout(hbox2)
        vbox_gb_oprTime.addLayout(hbox3)
        vbox_gb_oprTime.addLayout(hbox4)

        self.gb_oprTime.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.gb_oprTime.setTitle("Operating Time")
        self.gb_oprTime.setLayout(vbox_gb_oprTime)

    def thresholdUI(self, mui):
        ### Add Element
        mui.cb_thX1_on =QCheckBox("X1")
        mui.cb_thX2_on =QCheckBox("X2")
        mui.cb_thY1_on =QCheckBox("Y1")
        mui.cb_thY2_on =QCheckBox("Y2")
        mui.cb_thZ1_on =QCheckBox("Z1")
        mui.cb_thZ2_on =QCheckBox("Z2")
        ## X
        mui.sld_thX1 = QSlider(Qt.Vertical)
        mui.sld_thX1.setRange(-50, 50)
        mui.sld_thX1.setValue(0)
        mui.sb_thX1 = QSpinBox()
        mui.sb_thX1.setRange(-50, 50)
        mui.sb_thX1.setValue(mui.sld_thX1.value())
        mui.sb_thX1.valueChanged.connect(mui.setSliderThresholdParameter)
        mui.sld_thX1.valueChanged.connect(mui.setSpinBoxGraphParameter)
        mui.sld_thX1.valueChanged.connect(mui.refreshGraphSlider)
        mui.sb_thX1Variance = QSpinBox()
        mui.sb_thX1Variance.setRange(0, 1000)
        mui.sb_thX1Variance.valueChanged.connect(mui.refreshGraphSpinBox)
        mui.sld_thX2 = QSlider(Qt.Vertical)
        mui.sld_thX2.setRange(-50, 50)
        mui.sld_thX2.setValue(0)
        mui.sb_thX2 = QSpinBox()
        mui.sb_thX2.setRange(-50, 50)
        mui.sb_thX2.setValue(mui.sld_thX1.value())
        mui.sb_thX2.valueChanged.connect(mui.setSliderThresholdParameter)
        mui.sld_thX2.valueChanged.connect(mui.setSpinBoxGraphParameter)
        mui.sld_thX2.valueChanged.connect(mui.refreshGraphSlider)
        mui.sb_thX2Variance = QSpinBox()
        mui.sb_thX2Variance.setRange(0, 1000)
        mui.sb_thX2Variance.valueChanged.connect(mui.refreshGraphSpinBox)
        ## Y
        mui.sld_thY1 = QSlider(Qt.Vertical)
        mui.sld_thY1.setRange(-50, 50)
        mui.sld_thY1.setValue(0)
        mui.sb_thY1 = QSpinBox()
        mui.sb_thY1.setRange(-50, 50)
        mui.sb_thY1.setValue(mui.sld_thY1.value())
        mui.sb_thY1.valueChanged.connect(mui.setSliderThresholdParameter)
        mui.sld_thY1.valueChanged.connect(mui.setSpinBoxGraphParameter)
        mui.sld_thY1.valueChanged.connect(mui.refreshGraphSlider)
        mui.sb_thY1Variance = QSpinBox()
        mui.sb_thY1Variance.setRange(0, 1000)
        mui.sb_thY1Variance.valueChanged.connect(mui.refreshGraphSpinBox)
        mui.sld_thY2 = QSlider(Qt.Vertical)
        mui.sld_thY2.setRange(-50, 50)
        mui.sld_thY2.setValue(0)
        mui.sb_thY2 = QSpinBox()
        mui.sb_thY2.setRange(-50, 50)
        mui.sb_thY2.setValue(mui.sld_thY1.value())
        mui.sb_thY2.valueChanged.connect(mui.setSliderThresholdParameter)
        mui.sld_thY2.valueChanged.connect(mui.setSpinBoxGraphParameter)
        mui.sld_thY2.valueChanged.connect(mui.refreshGraphSlider)
        mui.sb_thY2Variance = QSpinBox()
        mui.sb_thY2Variance.setRange(0, 1000)
        mui.sb_thY2Variance.valueChanged.connect(mui.refreshGraphSpinBox)
        ##Z
        mui.sld_thZ1 = QSlider(Qt.Vertical)
        mui.sld_thZ1.setRange(-50, 50)
        mui.sld_thZ1.setValue(0)
        mui.sb_thZ1 = QSpinBox()
        mui.sb_thZ1.setRange(-50, 50)
        mui.sb_thZ1.setValue(mui.sld_thZ1.value())
        mui.sb_thZ1.valueChanged.connect(mui.setSliderThresholdParameter)
        mui.sld_thZ1.valueChanged.connect(mui.setSpinBoxGraphParameter)
        mui.sld_thZ1.valueChanged.connect(mui.refreshGraphSlider)
        mui.sb_thZ1Variance = QSpinBox()
        mui.sb_thZ1Variance.setRange(0, 1000)
        mui.sb_thZ1Variance.valueChanged.connect(mui.refreshGraphSpinBox)
        mui.sld_thZ2 = QSlider(Qt.Vertical)
        mui.sld_thZ2.setRange(-50, 50)
        mui.sld_thZ2.setValue(0)
        mui.sb_thZ2 = QSpinBox()
        mui.sb_thZ2.setRange(-50, 50)
        mui.sb_thZ2.setValue(mui.sld_thZ2.value())
        mui.sb_thZ2.valueChanged.connect(mui.setSliderThresholdParameter)
        mui.sld_thZ2.valueChanged.connect(mui.setSpinBoxGraphParameter)
        mui.sld_thZ2.valueChanged.connect(mui.refreshGraphSlider)
        mui.sb_thZ2Variance = QSpinBox()
        mui.sb_thZ2Variance.setRange(0, 1000)
        mui.sb_thZ2Variance.valueChanged.connect(mui.refreshGraphSpinBox)

        #
        lbl_scaleX = QLabel('scale X:')
        lbl_scaleY = QLabel('scale Y:')
        lbl_scaleZ = QLabel('scale Z:')
        mui.sb_thX_scale = QDoubleSpinBox()
        mui.sb_thX_scale.setRange(0.01, 100)
        mui.sb_thX_scale.setValue(0.05)
        mui.sb_thX_scale.setSingleStep(0.01)
        mui.sb_thY_scale = QDoubleSpinBox()
        mui.sb_thY_scale.setRange(0.01, 100)
        mui.sb_thY_scale.setValue(0.05)
        mui.sb_thY_scale.setSingleStep(0.01)
        mui.sb_thZ_scale = QDoubleSpinBox()
        mui.sb_thZ_scale.setRange(0.01, 100)
        mui.sb_thZ_scale.setValue(0.05)
        mui.sb_thZ_scale.setSingleStep(0.01)

        ### -1-
        hbox1 = QHBoxLayout()
        hbox1.addWidget(lbl_scaleX)
        hbox1.addWidget(mui.sb_thX_scale)
        hbox1.addWidget(lbl_scaleY)
        hbox1.addWidget(mui.sb_thY_scale)
        hbox1.addWidget(lbl_scaleZ)
        hbox1.addWidget(mui.sb_thZ_scale)

        ### |1|
        vbox1 = QVBoxLayout()
        vbox1.addWidget(mui.cb_thX1_on)
        vbox1.addWidget(mui.sb_thX1)
        vbox1.addWidget(mui.sld_thX1)
        vbox1.addWidget(mui.sb_thX1Variance)
        vbox1_2 = QVBoxLayout()
        vbox1_2.addWidget(mui.cb_thX2_on)
        vbox1_2.addWidget(mui.sb_thX2)
        vbox1_2.addWidget(mui.sld_thX2)
        vbox1_2.addWidget(mui.sb_thX2Variance)
        ### |2|
        vbox2 = QVBoxLayout()
        vbox2.addWidget(mui.cb_thY1_on)
        vbox2.addWidget(mui.sb_thY1)
        vbox2.addWidget(mui.sld_thY1)
        vbox2.addWidget(mui.sb_thY1Variance)
        vbox2_2 = QVBoxLayout()
        vbox2_2.addWidget(mui.cb_thY2_on)
        vbox2_2.addWidget(mui.sb_thY2)
        vbox2_2.addWidget(mui.sld_thY2)
        vbox2_2.addWidget(mui.sb_thY2Variance)
        ### |3|
        vbox3 = QVBoxLayout()
        vbox3.addWidget(mui.cb_thZ1_on)
        vbox3.addWidget(mui.sb_thZ1)
        vbox3.addWidget(mui.sld_thZ1)
        vbox3.addWidget(mui.sb_thZ1Variance)
        vbox3_2 = QVBoxLayout()
        vbox3_2.addWidget(mui.cb_thZ2_on)
        vbox3_2.addWidget(mui.sb_thZ2)
        vbox3_2.addWidget(mui.sld_thZ2)
        vbox3_2.addWidget(mui.sb_thZ2Variance)
        ### -2|1|2|3|-
        hbox2 = QHBoxLayout()
        hbox2.addLayout(vbox1)
        hbox2.addLayout(vbox1_2)
        hbox2.addLayout(vbox2)
        hbox2.addLayout(vbox2_2)
        hbox2.addLayout(vbox3)
        hbox2.addLayout(vbox3_2)

        ### |-1-2-|
        vbox_gb_setThreshold = QVBoxLayout()
        vbox_gb_setThreshold.addLayout(hbox1)
        vbox_gb_setThreshold.addLayout(hbox2)

        mui.gb_setThreshold.setMinimumHeight(500)
        mui.gb_setThreshold.setVisible(self.cb_DisplayThresholdUI.isVisible())
        mui.gb_setThreshold.setTitle("Setting Threshold")
        mui.gb_setThreshold.setLayout(vbox_gb_setThreshold)

    def readConfig(self, mui):
        filename = QFileDialog.getOpenFileName(self, 'Open file', '.')
        self.le_readConfig.setText(filename[0])
        if self.le_readConfig.text() == "":
            return -1

        config = ConfigParser()
        config.read(self.le_readConfig.text())

        ## set parameter
        self.stdOprTimeSb.setValue(float(config['timeUI']['StandartOperationTime']))
        self.fpsSb.setValue(int(config['timeUI']['FPS']))
        self.cb_saveOprTime.setChecked("True" == (config['timeUI']['SaveOperationTime']))
        self.le_filepath.setText(config['timeUI']['SaveFilename'])
        mui.cb_thX1_on.setChecked("True" == (config['thresholdUI']['UseThreshold_X1']))
        mui.cb_thX2_on.setChecked("True" == (config['thresholdUI']['UseThreshold_X2']))
        mui.cb_thY1_on.setChecked("True" == (config['thresholdUI']['UseThreshold_Y1']))
        mui.cb_thY2_on.setChecked("True" == (config['thresholdUI']['UseThreshold_Y2']))
        mui.cb_thZ1_on.setChecked("True" == (config['thresholdUI']['UseThreshold_Z1']))
        mui.cb_thZ2_on.setChecked("True" == (config['thresholdUI']['UseThreshold_Z2']))
        mui.sb_thX_scale.setValue(float(config['thresholdUI']['Threshold_ScaleX']))
        mui.sb_thY_scale.setValue(float(config['thresholdUI']['Threshold_ScaleY']))
        mui.sb_thZ_scale.setValue(float(config['thresholdUI']['Threshold_ScaleZ']))
        mui.sb_thX1.setValue(int(config['thresholdUI']['Threshold_ValueX1']))
        mui.sb_thX2.setValue(int(config['thresholdUI']['Threshold_ValueX2']))
        mui.sb_thY1.setValue(int(config['thresholdUI']['Threshold_ValueY1']))
        mui.sb_thY2.setValue(int(config['thresholdUI']['Threshold_ValueY2']))
        mui.sb_thZ1.setValue(int(config['thresholdUI']['Threshold_ValueZ1']))
        mui.sb_thZ2.setValue(int(config['thresholdUI']['Threshold_ValueZ2']))
        mui.sb_thX1Variance.setValue(int(config['thresholdUI']['Threshold_VarianceX1']))
        mui.sb_thX2Variance.setValue(int(config['thresholdUI']['Threshold_VarianceX2']))
        mui.sb_thY1Variance.setValue(int(config['thresholdUI']['Threshold_VarianceY1']))
        mui.sb_thY2Variance.setValue(int(config['thresholdUI']['Threshold_VarianceY2']))
        mui.sb_thZ1Variance.setValue(int(config['thresholdUI']['Threshold_VarianceZ1']))
        mui.sb_thZ2Variance.setValue(int(config['thresholdUI']['Threshold_VarianceZ2']))
        mui.combo.setCurrentText(config['figureUI']['TargetSkeltonParts'])

    def saveConfig(self, mui):
        filename = QFileDialog.getSaveFileName(self, 'Save File', '.')
        self.le_saveConfig.setText(filename[0])
        if self.le_saveConfig.text() == "":
            return -1

        config = ConfigParser()
        config.optionxform = str
        config.add_section('timeUI')
        config.add_section('thresholdUI')
        config.add_section('figureUI')
        config.add_section('mainUI')
        config.set('timeUI', 'StandartOperationTime', str(self.stdOprTimeSb.value()))
        config.set('timeUI', 'FPS', str(self.fpsSb.value()))
        config.set('timeUI', 'SaveOperationTime', str(self.cb_saveOprTime.checkState()))
        config.set('timeUI', 'SaveFilename', str(self.le_filepath.text()))
        config.set('thresholdUI', 'UseThreshold_X1', self.bool2string(mui.cb_thX1_on.checkState()))
        config.set('thresholdUI', 'UseThreshold_X2', self.bool2string(mui.cb_thX2_on.checkState()))
        config.set('thresholdUI', 'UseThreshold_Y1', self.bool2string(mui.cb_thY1_on.checkState()))
        config.set('thresholdUI', 'UseThreshold_Y2', self.bool2string(mui.cb_thY2_on.checkState()))
        config.set('thresholdUI', 'UseThreshold_Z1', self.bool2string(mui.cb_thZ1_on.checkState()))
        config.set('thresholdUI', 'UseThreshold_Z2', self.bool2string(mui.cb_thZ2_on.checkState()))
        config.set('thresholdUI', 'Threshold_ScaleX', str(mui.sb_thX_scale.value()))
        config.set('thresholdUI', 'Threshold_ScaleY', str(mui.sb_thY_scale.value()))
        config.set('thresholdUI', 'Threshold_ScaleZ', str(mui.sb_thZ_scale.value()))
        config.set('thresholdUI', 'Threshold_ValueX1', str(mui.sb_thX1.value()))
        config.set('thresholdUI', 'Threshold_ValueX2', str(mui.sb_thX2.value()))
        config.set('thresholdUI', 'Threshold_ValueY1', str(mui.sb_thY1.value()))
        config.set('thresholdUI', 'Threshold_ValueY2', str(mui.sb_thY2.value()))
        config.set('thresholdUI', 'Threshold_ValueZ1', str(mui.sb_thZ1.value()))
        config.set('thresholdUI', 'Threshold_ValueZ2', str(mui.sb_thZ2.value()))
        config.set('thresholdUI', 'Threshold_VarianceX1', str(mui.sb_thX1Variance.value()))
        config.set('thresholdUI', 'Threshold_VarianceX2', str(mui.sb_thX2Variance.value()))
        config.set('thresholdUI', 'Threshold_VarianceY1', str(mui.sb_thY1Variance.value()))
        config.set('thresholdUI', 'Threshold_VarianceY2', str(mui.sb_thY2Variance.value()))
        config.set('thresholdUI', 'Threshold_VarianceZ1', str(mui.sb_thZ1Variance.value()))
        config.set('thresholdUI', 'Threshold_VarianceZ2', str(mui.sb_thZ2Variance.value()))
        config.set('figureUI', 'TargetSkeltonParts', str(mui.combo.currentText()))
        config.write(open(self.le_saveConfig.text(), 'w'))

    def getCalclationTime(self, mui):
        self.calcDifferenceOperatingTime()
        if self.cb_saveOprTime.checkState():
            self.writeText(mui)

    def calcDifferenceOperatingTime(self):
        time = self.stdOprTimeSb.value() - float(self.calcOprTimeLabel.text())
        self.differenceTimeLabel.setText("{0:.2f}[sec]".format(time))

    def writeText(self, mui):
        import csv
        import os.path
        writeItemname = True
        if os.path.isfile( self.le_filepath.text() ):
            writeItemname = False
        with open(self.le_filepath.text(), 'a', newline="") as f:
            writer = csv.writer(f)
            if writeItemname:
                writer.writerow(['Filename', 'FPS', 'Calclation Time', 'Setting Time'])
            writer.writerow([mui.fnameQle.text(), self.fpsSb.value(), float(self.calcOprTimeLabel.text()), self.stdOprTimeSb.value()])

    def setSaveTimeFilePath(self):
        filename = QFileDialog.getSaveFileName(self, 'Save File', '.')
        self.le_filepath.setText(filename[0])

    def bool2string(self, bool_val):
        if bool_val:
            return 'True'
        else:
            return 'False'

    def displayThresholdWindow(self, mui):
        mui.gb_setThreshold.setVisible(self.cb_DisplayThresholdUI.isChecked())
