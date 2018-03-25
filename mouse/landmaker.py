import sys
from PyQt5.QtCore import (Qt, QEvent)
from PyQt5.QtGui import (QPixmap, QImage, QCursor, QBrush, QColor, QPalette)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
                             QPushButton, QComboBox, QCheckBox, QLabel, QSpinBox, QLineEdit, QFileDialog,
                             QGraphicsPixmapItem, QGraphicsScene, QGraphicsView,
                             QMenu, QGraphicsItem, QGraphicsEllipseItem, QColorDialog,
                             QGroupBox, QSizePolicy
                             )

from mypackage.opencv_ip import ImageProcessing
from mypackage.landmark_detection import PredictLandmark
from mypackage.table_parts import Model, View

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Landmarker ver.2.0")
        self.setAcceptDrops(True)

        self.init()
        self.imageMenu()
        self.imageProcessingMenu()
        self.drawImageMenu()
        self.labelMenu()
        self.landmarkMenu()
        self.labelDataMenu()

        mainframe = QWidget()
        grid = QGridLayout()
        grid.addWidget(self.grbox_imageMenu, 0, 0)
        grid.addWidget(self.grbox_IP, 1, 0)
        grid.addWidget(self.picView, 2, 0)
        vbox = QVBoxLayout()
        vbox.addWidget(self.grbox_labelMenu)
        vbox.addWidget(self.grbox_landmark)
        vbox.addWidget(self.grbox_labelDataMenu)
        grid.addLayout(vbox, 0, 1, 3, 1)
        mainframe.setLayout(grid)
        self.setCentralWidget(mainframe)

    def init(self):
        self.ptColor = QColor("lime")
        self.openFileFlags = False
        self.ipModule = ImageProcessing()
        self.src_img = ""
        self.dst_img = ""
    # ui function
    def imageMenu(self):
        btn_open = QPushButton("Open File")
        btn_open.clicked.connect(self.openFile)
        self.file_edit = QLineEdit()
        self.label_imgWidth = QLabel("(width)")
        self.label_imgHeihgt = QLabel("(height)")
        self.sb_maxImgWidth = QSpinBox()
        self.sb_maxImgWidth.setMaximum(3840)
        self.sb_maxImgWidth.setValue(1080)
        self.sb_maxImgHeihgt = QSpinBox()
        self.sb_maxImgHeihgt.setMaximum(2160)
        self.sb_maxImgHeihgt.setValue(720)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(btn_open)
        hbox1.addWidget(self.file_edit)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel("Image Size:"))
        hbox2.addWidget(self.label_imgWidth)
        hbox2.addWidget(QLabel("x"))
        hbox2.addWidget(self.label_imgHeihgt)
        hbox2.addStretch(0)
        hbox2.addWidget(QLabel("Max Window:"))
        hbox2.addWidget(self.sb_maxImgWidth)
        hbox2.addWidget(QLabel("x"))
        hbox2.addWidget(self.sb_maxImgHeihgt)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        self.grbox_imageMenu = QGroupBox("Image Menu")
        self.grbox_imageMenu.setLayout(vbox)
    # ui function
    def imageProcessingMenu(self):
        btn_ipRun = QPushButton("Run")
        btn_ipRun.clicked.connect(self.selectImageProcessing)
        self.cmb_IP = QComboBox()
        IPs = ["Grayscale", "Flip(Horizon)", "Translation","Sobel(X)","Sobel(Y)", "Laplacian", "Canny"]
        for IP in IPs:
            self.cmb_IP.addItem(IP)
        self.cb_keepImage = QCheckBox("Keep")
        self.cb_keepImage.stateChanged.connect(self.keepImage)
        btn_saveImage = QPushButton("Save")
        btn_saveImage.clicked.connect(self.saveImage)
        btn_initImage = QPushButton("Clear")
        btn_initImage.clicked.connect(self.clearItems)
        hbox = QHBoxLayout()
        hbox.addWidget(self.cmb_IP)
        hbox.addWidget(btn_ipRun)
        hbox.addWidget(self.cb_keepImage)
        hbox.addWidget(btn_saveImage)
        hbox.addWidget(btn_initImage)
        hbox.addStretch(0)
        self.grbox_IP = QGroupBox("Image Processing")
        self.grbox_IP.setLayout(hbox)
    # ui function
    def drawImageMenu(self):
        self.picView = QGraphicsView()
        self.picView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.picView.customContextMenuRequested.connect(self.contextMenue)
        self.picView.installEventFilter(self)
    # ui function
    def labelMenu(self):
        self.cmb_ID = QComboBox()
        values = ["0:None","1:RightEye","2:LeftEye", "3:Nose"]
        for value in values:
            self.cmb_ID.addItem(value)
        self.sb_radius = QSpinBox()
        self.sb_radius.setValue(5)
        btn_color = QPushButton("Color")
        btn_color.clicked.connect(self.selectColor)
        self.label_color = QLabel("●")
        pal = self.label_color.palette()
        pal.setColor(QPalette.Foreground, self.ptColor)
        self.label_color.setPalette(pal)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("ID:"))
        hbox1.addWidget(self.cmb_ID)
        hbox1.addStretch(0)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel("Point:"))
        hbox2.addWidget(self.label_color)
        hbox2.addWidget(btn_color)
        hbox2.addWidget(QLabel("Size"))
        hbox2.addWidget(self.sb_radius)
        hbox2.addStretch(0)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        self.grbox_labelMenu = QGroupBox("Label Menu")
        self.grbox_labelMenu.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.grbox_labelMenu.setLayout(vbox)
    # ui function
    def landmarkMenu(self):
        self.sb_inputWidth = QSpinBox()
        self.sb_inputWidth.setMaximum(1080)
        self.sb_inputWidth.setValue(90)
        # self.sb_inputWidth.setEnabled(False)
        self.sb_inputHeight = QSpinBox()
        self.sb_inputHeight.setMaximum(720)
        self.sb_inputHeight.setValue(100)
        # self.sb_inputHeight.setEnabled(False)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("Input Size:"))
        hbox1.addWidget(self.sb_inputWidth)
        hbox1.addWidget(QLabel("x"))
        hbox1.addWidget(self.sb_inputHeight)
        hbox1.addStretch(0)
        btn_modelPath = QPushButton("Model Path")
        btn_modelPath.clicked.connect(self.selectModelPath)
        self.le_modelPath = QLineEdit()
        self.le_modelPath.setText("model/mdl_ep1000")
        hbox2 = QHBoxLayout()
        hbox2.addWidget(btn_modelPath)
        hbox2.addWidget(self.le_modelPath)
        btn_landmark = QPushButton("Run")
        btn_landmark.clicked.connect(self.detectLandmarks)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(btn_landmark)
        self.grbox_landmark = QGroupBox("Landmark Detection")
        self.grbox_landmark.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.grbox_landmark.setLayout(vbox)
    # ui function
    def labelDataMenu(self):
        btn_load = QPushButton("Load")
        btn_load.clicked.connect(self.loadFile)
        btn_save = QPushButton("Save")
        btn_save.clicked.connect(self.saveFile)
        self.tableView = View(self)
        self.model = Model(self)
        self.model.setHeaders(['No.', 'ID', 'POS(X)', 'POS(Y)'])
        self.tableView.setModel(self.model)
        self.tableView.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.tableView.setMaximumWidth(215)
        self.tableView.setColumnWidth(0, 20) # have to load the tableview before setting size
        self.tableView.setColumnWidth(1, 20)
        self.tableView.setColumnWidth(2, 50)
        self.tableView.setColumnWidth(3, 50)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(btn_load)
        hbox1.addWidget(btn_save)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addWidget(self.tableView)
        self.grbox_labelDataMenu = QGroupBox("Label Data")
        self.grbox_labelDataMenu.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.grbox_labelDataMenu.setLayout(vbox)

    # event function
    def contextMenue(self, event):
        if self.openFileFlags:
            menu = QMenu()
            menu.addAction('Remove Selected Items', self.removeItems)
            menu.addAction('Clear Items', self.clearItems)
            menu.exec_(QCursor.pos())
    # event function
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    # event function
    def dropEvent(self, event):
        self.file = ["".join(u.toLocalFile() for u in event.mimeData().urls()),""]
        self.readImage()
    # event function
    def eventFilter(self, source, event):
        # event MouseButtonPress
        if (event.type() == QEvent.MouseButtonPress and source is self.picView):
            if event.button() == Qt.RightButton:
                pass
            else:
                pos = event.pos()
                h_sbar_val = self.picView.horizontalScrollBar().value()
                v_sbar_val = self.picView.verticalScrollBar().value()

                item = QGraphicsEllipseItem(pos.x() - self.sb_radius.value() + h_sbar_val,
                                            pos.y() - self.sb_radius.value() + v_sbar_val,
                                            self.sb_radius.value() * 2, self.sb_radius.value() * 2)
                item.setBrush(QBrush(self.ptColor))
                item.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
                item.setData(0, self.cmb_ID.currentText().split(':')[0])

                self.scene.addItem(item)
                self.updateItems()

        # event Leave
        if (event.type() == QEvent.Leave and source is self.picView):
            self.updateItems()

        return QWidget.eventFilter(self, source, event)

    # button function
    def removeItems(self):
        items = self.scene.selectedItems()
        for item in items:
            self.scene.removeItem(item)
        self.updateItems()
    # button function
    def clearItems(self):
        self.scene.clear()
        self.model.itemsClear()
        pic_Item = QGraphicsPixmapItem(QPixmap(self.file[0]))
        self.scene.addItem(pic_Item)
        self.src_img = self.dst_img = ""

    # button function
    def openFile(self):
        fileFilter = 'Image Files (*.png *.jpg *.bmp)'
        self.file = QFileDialog.getOpenFileName(self, 'Open file', '', fileFilter)
        self.readImage()

    # function
    def updateItems(self):
        if self.openFileFlags:
            self.model.itemsClear()
            for i in range(len(self.scene.items(0))):
                if self.scene.items(0)[i].type() == QGraphicsEllipseItem().type():
                    a = self.scene.items(0)[i].rect().x()
                    b = self.scene.items(0)[i].rect().y()
                    c = self.scene.items(0)[i].scenePos().x()
                    d = self.scene.items(0)[i].scenePos().y()
                    id = self.scene.items(0)[i].data(0)

                    self.model.addRow(i, id, a + c + self.sb_radius.value(), b + d + self.sb_radius.value())
                    self.scene.items(0)[i].setToolTip("No.{0}".format(i))
            self.tableView.scrollToBottom()

    def readImage(self):
        if not self.file[0] == "":
            self.file_edit.setText(self.file[0])
            self.scene = QGraphicsScene()
            pic_Item = QGraphicsPixmapItem(QPixmap(self.file[0]))
            self.scene.addItem(pic_Item)
            self.picView.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            self.picView.setScene(self.scene)

            self.openFileFlags = True
            imgWidth = int(pic_Item.boundingRect().width())
            imgHeight = int(pic_Item.boundingRect().height())
            self.label_imgWidth.setText(str(imgWidth))
            self.label_imgHeihgt.setText(str(imgHeight))
            self.resizeWindow(imgWidth, imgHeight)

            self.cb_keepImage.setChecked(False)
            self.src_img = self.dst_img = ""

    def resizeWindow(self, _imgWidth, _imgHeight):
        winWidth = _imgWidth
        winHeight = _imgHeight
        if self.sb_maxImgWidth.value() < _imgWidth:
            winWidth = self.sb_maxImgWidth.value()
        if self.sb_maxImgWidth.value() < _imgHeight:
            winHeight = self.sb_maxImgWidth.value()

        pos = self.picView.pos()
        menuWidth = self.grbox_labelDataMenu.width()
        offset = [17, 11]
        self.resize(pos.x() + winWidth + menuWidth + offset[0], pos.y() + winHeight + offset[1])

    # button function
    def loadFile(self):
        import csv
        fileFilter = 'CSV Files (*.csv);;Text Files (*.txt)'
        file = QFileDialog.getOpenFileName(self, 'Load File', '', fileFilter)
        if not file[0] == "":
            with open(file[0], 'r') as f:
                reader = csv.reader(f)
                header = next(reader) #header pass
                for row in reader:
                    item = QGraphicsEllipseItem(int(float(row[2]))-self.sb_radius.value(), int(float(row[3]))-self.sb_radius.value(), self.sb_radius.value() * 2, self.sb_radius.value() * 2)
                    item.setBrush(QBrush(self.ptColor))
                    item.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
                    item.setData(0, int(float(row[1])))
                    self.scene.addItem(item)
                self.updateItems()

    # button function
    def saveFile(self):
        import csv
        fileFilter = 'CSV Files (*.csv);;Text Files (*.txt)'
        file = QFileDialog.getSaveFileName(self, 'Save File', '', fileFilter)
        if not file[0] == "":
            with open(file[0], 'w', newline="") as f:
                writer = csv.writer(f)
                writer.writerow(self.model.headers)
                for item in self.model.items:
                    writer.writerow(item)

    # button function
    def selectColor(self):
        self.ptColor = QColorDialog.getColor()
        
        pal = self.label_color.palette()
        pal.setColor(QPalette.Foreground, self.ptColor)
        self.label_color.setPalette(pal)

    # button function
    def selectImageProcessing(self):
        if self.openFileFlags:
            self.openImage()
            if self.cmb_IP.currentText() == "Grayscale":
                self.dst_img = self.ipModule.grayscale(self.src_img)
            elif self.cmb_IP.currentText() == "Flip(Horizon)":
                self.dst_img = self.ipModule.flip(self.src_img)
            elif self.cmb_IP.currentText() == "Translation":
                self.dst_img = self.ipModule.translation(self.src_img)
            elif self.cmb_IP.currentText() == "Sobel(X)":
                self.dst_img = self.ipModule.sobelX(self.src_img)
            elif self.cmb_IP.currentText() == "Sobel(Y)":
                self.dst_img = self.ipModule.sobelY(self.src_img)
            elif self.cmb_IP.currentText() == "Laplacian":
                self.dst_img = self.ipModule.laplacian(self.src_img)
            elif self.cmb_IP.currentText() == "Canny":
                self.dst_img = self.ipModule.canny(self.src_img)

            self.setProcessedImage(self.dst_img)

    def openImage(self):
        if not self.cb_keepImage.isChecked() or len(self.src_img) == 0:
            _, self.src_img = self.ipModule.open_img(self.file[0])
            self.dst_img = self.src_img

    def keepImage(self):
        if self.openFileFlags and len(self.src_img) > 0:
            if self.cb_keepImage.isChecked():
                self.src_img = self.dst_img

    def saveImage(self):
        if self.openFileFlags and len(self.src_img) > 0:
            fileFilter = 'JPEG Files (*.jpg);;PNG File (*.png);;BMP File (*.bmp)'
            file = QFileDialog.getSaveFileName(self, 'Save File', '', fileFilter)
            if not file[0] == "":
                self.ipModule.save_img(file[0], self.dst_img)

    def setProcessedImage(self, _img):
        if len(_img.shape) == 3:
            height, width, dim = _img.shape
            bytesPerLine = dim * width
            qimg = QImage(_img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        if len(_img.shape) == 2:
            height, width = _img.shape
            bytesPerLine = width
            qimg = QImage(_img.data, width, height, bytesPerLine, QImage.Format_Grayscale8)

        pic_Item = QGraphicsPixmapItem(QPixmap.fromImage(qimg))
        self.scene = QGraphicsScene()
        self.scene.addItem(pic_Item)
        self.picView.setScene(self.scene)
        self.keepImage()
    # button function
    def selectModelPath(self):
        path = QFileDialog.getExistingDirectory(self, 'Select Model Directory')
        self.le_modelPath.setText(path)
    # button function
    def detectLandmarks(self):
        if self.openFileFlags:
            self.cb_keepImage.setChecked(True)
            self.openImage()
            # exe
            lm_module = PredictLandmark()
            lm_module.setImageSize(self.sb_inputWidth.value(), self.sb_inputHeight.value())
            lm_module.setModel(self.le_modelPath.text())
            lm_module.calcImageRatio(int(self.label_imgWidth.text()), int(self.label_imgHeihgt.text()))
            posX, posY = lm_module.getLandmarkPos(self.dst_img)
            # registration
            for x, y in zip(posX, posY):
                item = QGraphicsEllipseItem(int(float(x)) - self.sb_radius.value(),
                                            int(float(y)) - self.sb_radius.value(),
                                            self.sb_radius.value() * 2, self.sb_radius.value() * 2)
                item.setBrush(QBrush(self.ptColor))
                item.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
                item.setData(0, int(float(0)))
                self.scene.addItem(item)
            self.updateItems()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dmw = MainWindow()
    dmw.show()
    sys.exit(app.exec_())