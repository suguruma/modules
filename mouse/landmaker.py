import sys
from PyQt5.QtCore import (Qt, QEvent)
from PyQt5.QtGui import (QPixmap, QImage, QCursor, QBrush, QColor, QPalette)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
                             QPushButton, QComboBox, QCheckBox, QLabel, QSpinBox, QLineEdit, QFileDialog,
                             QGraphicsPixmapItem, QGraphicsScene, QGraphicsView,
                             QMenu, QGraphicsItem, QGraphicsEllipseItem, QColorDialog,
                             QGroupBox, QSizePolicy
                             )

from mypackage.ui_mainform import UIMainWindow
from mypackage.opencv_ip import ImageProcessing
from mypackage.landmark_detection import PredictLandmark

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Landmarker ver.2.1")
        self.setAcceptDrops(True)

        self.init()
        self.ui = UIMainWindow(self)
        self.ipModule = ImageProcessing()

        mainframe = QWidget()
        grid = QGridLayout()
        grid.addWidget(self.ui.grbox_imageMenu, 0, 0)
        grid.addWidget(self.ui.grbox_IP, 1, 0)
        grid.addWidget(self.ui.picView, 2, 0)
        vbox = QVBoxLayout()
        vbox.addWidget(self.ui.grbox_labelMenu)
        vbox.addWidget(self.ui.grbox_landmark)
        vbox.addWidget(self.ui.grbox_labelDataMenu)
        grid.addLayout(vbox, 0, 1, 3, 1)
        mainframe.setLayout(grid)
        self.setCentralWidget(mainframe)

    def init(self):
        self.ptColor = QColor("lime")
        self.openFileFlags = False
        self.src_img = ""
        self.dst_img = ""

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
        if (event.type() == QEvent.MouseButtonPress and source is self.ui.picView):
            if event.button() == Qt.RightButton:
                pass
            else:
                pos = event.pos()
                h_sbar_val = self.ui.picView.horizontalScrollBar().value()
                v_sbar_val = self.ui.picView.verticalScrollBar().value()

                item = QGraphicsEllipseItem(pos.x() - self.ui.sb_radius.value() + h_sbar_val,
                                            pos.y() - self.ui.sb_radius.value() + v_sbar_val,
                                            self.ui.sb_radius.value() * 2, self.ui.sb_radius.value() * 2)
                item.setBrush(QBrush(self.ptColor))
                item.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
                item.setData(0, self.ui.cmb_ID.currentText().split(':')[0])

                self.scene.addItem(item)
                self.updateItems()

        # event Leave
        if (event.type() == QEvent.Leave and source is self.ui.picView):
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
        self.ui.model.itemsClear()
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
            self.ui.model.itemsClear()
            for i in range(len(self.scene.items(0))):
                if self.scene.items(0)[i].type() == QGraphicsEllipseItem().type():
                    a = self.scene.items(0)[i].rect().x()
                    b = self.scene.items(0)[i].rect().y()
                    c = self.scene.items(0)[i].scenePos().x()
                    d = self.scene.items(0)[i].scenePos().y()
                    id = self.scene.items(0)[i].data(0)

                    self.ui.model.addRow(i, id, a + c + self.ui.sb_radius.value(), b + d + self.ui.sb_radius.value())
                    self.scene.items(0)[i].setToolTip("No.{0}".format(i))
            self.ui.tableView.scrollToBottom()

    def readImage(self):
        if not self.file[0] == "":
            self.ui.file_edit.setText(self.file[0])
            self.scene = QGraphicsScene()

            pic_Item = QGraphicsPixmapItem(QPixmap(self.file[0]))
            self.scene.addItem(pic_Item)
            self.ui.picView.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            self.ui.picView.setScene(self.scene)

            self.openFileFlags = True
            imgWidth = int(pic_Item.boundingRect().width())
            imgHeight = int(pic_Item.boundingRect().height())
            self.ui.label_imgWidth.setText(str(imgWidth))
            self.ui.label_imgHeihgt.setText(str(imgHeight))
            self.resizeWindow(imgWidth, imgHeight)

            self.ui.cb_keepImage.setChecked(False)
            self.src_img = self.dst_img = ""

    def resizeWindow(self, _imgWidth, _imgHeight):
        winWidth = _imgWidth
        winHeight = _imgHeight
        if self.ui.sb_maxImgWidth.value() < _imgWidth:
            winWidth = self.sb_maxImgWidth.value()
        if self.ui.sb_maxImgWidth.value() < _imgHeight:
            winHeight = self.sb_maxImgWidth.value()

        pos = self.ui.picView.pos()
        menuWidth = self.ui.grbox_labelDataMenu.width()
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
        
        pal = self.ui.label_color.palette()
        pal.setColor(QPalette.Foreground, self.ptColor)
        self.ui.label_color.setPalette(pal)

    # button function
    def selectImageProcessing(self):
        if self.openFileFlags:
            self.openImage()
            if self.ui.cmb_IP.currentText() == "Grayscale":
                self.dst_img = self.ipModule.grayscale(self.src_img)
            elif self.ui.cmb_IP.currentText() == "Flip(Horizon)":
                self.dst_img = self.ipModule.flip(self.src_img)
            elif self.ui.cmb_IP.currentText() == "Translation":
                self.dst_img = self.ipModule.translation(self.src_img)
            elif self.ui.cmb_IP.currentText() == "Sobel(X)":
                self.dst_img = self.ipModule.sobelX(self.src_img)
            elif self.ui.cmb_IP.currentText() == "Sobel(Y)":
                self.dst_img = self.ipModule.sobelY(self.src_img)
            elif self.ui.cmb_IP.currentText() == "Laplacian":
                self.dst_img = self.ipModule.laplacian(self.src_img)
            elif self.ui.cmb_IP.currentText() == "Canny":
                self.dst_img = self.ipModule.canny(self.src_img)

            self.setProcessedImage(self.dst_img)

    def openImage(self):
        if not self.ui.cb_keepImage.isChecked() or len(self.src_img) == 0:
            _, self.src_img = self.ipModule.open_img(self.file[0])
            self.dst_img = self.src_img

    def keepImage(self):
        if self.openFileFlags and len(self.src_img) > 0:
            if self.ui.cb_keepImage.isChecked():
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
        self.ui.picView.setScene(self.scene)
        self.keepImage()
    # button function
    def selectModelPath(self):
        path = QFileDialog.getExistingDirectory(self, 'Select Model Directory')
        self.ui.le_modelPath.setText(path)
    # button function
    def detectLandmarks(self):
        if self.openFileFlags:
            self.ui.cb_keepImage.setChecked(True)
            self.openImage()
            # exe
            lm_module = PredictLandmark()
            lm_module.setImageSize(self.ui.sb_inputWidth.value(), self.ui.sb_inputHeight.value())
            lm_module.setModel(self.ui.le_modelPath.text())
            lm_module.calcImageRatio(int(self.ui.label_imgWidth.text()), int(self.ui.label_imgHeihgt.text()))
            posX, posY = lm_module.getLandmarkPos(self.dst_img)
            # registration
            for x, y in zip(posX, posY):
                item = QGraphicsEllipseItem(int(float(x)) - self.ui.sb_radius.value(),
                                            int(float(y)) - self.ui.sb_radius.value(),
                                            self.ui.sb_radius.value() * 2, self.ui.sb_radius.value() * 2)
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