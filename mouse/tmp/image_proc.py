from __future__ import with_statement

import sys
from PyQt5.QtCore import (QObject, Qt, QUrl, QTimer, QModelIndex, QPoint, QRect, QEvent )
from PyQt5.QtGui import (QStandardItemModel, QStandardItem, QPixmap, QKeySequence, QImage, QCursor, 
                                QPainter, QBrush, QColor
                            )
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
                               QPushButton, QComboBox, QCheckBox, QLabel, QSpinBox, QLineEdit, QListView,
                               QLCDNumber, QSlider, QTableWidget, QTableWidgetItem, QAction, QFileDialog,
                               QMessageBox, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView,
                               QMenu, QGraphicsItem, QGraphicsEllipseItem
                            )
import numpy as np
import cv2

class opencv_test:
	#初期化
	def __init__(self, file, parent = None):
		self.file = file
	#ファイルを読み込み、BGRをRGBに変換する関数
	def open_pic(self,file):
		pic = cv2.imread(file)
		pic_color = cv2.cvtColor(pic,cv2.COLOR_BGR2RGB)
		return pic,pic_color
	#Canny処理してエッジ検出した後に、元の画像と重ねる関数
	def canny(self,pic):
		img =cv2.cvtColor(pic,cv2.COLOR_BGR2GRAY)
		edges = cv2.Canny(img,100,200)
		edges2 = np.zeros_like(pic)
		for i in (0,1,2):
			edges2[:,:,i] = edges
		add = cv2.addWeighted(pic,1,edges2,0.4,0)
		return add

#http://tatabox.hatenablog.com/entry/2014/09/16/194456
class DesignerMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(DesignerMainWindow, self).__init__(parent)
        
        mainframe = QWidget()
        grid = QGridLayout()

        btn = QPushButton("Open File")
        btn.clicked.connect(self.open_file)
        grid.addWidget(btn, 0, 0)

        self.file_edit = QLineEdit()
        grid.addWidget(self.file_edit, 1, 0)

        self.pic_View = QGraphicsView()
        grid.addWidget(self.pic_View, 2, 0)

        btn2 = QPushButton("EXE")
        btn2.clicked.connect(self.exe_canny)
        grid.addWidget(btn2, 3, 0)

        #grid.addWidget(self.gb_display_frame, 0, 1)
        mainframe.setLayout(grid)
        self.setCentralWidget(mainframe)

        pic_view = self.pic_View

        pic_view.setContextMenuPolicy(Qt.CustomContextMenu)
        pic_view.customContextMenuRequested.connect(self.contextMenue)
        
        self.pic_View.installEventFilter(self)

    def contextMenue(self, event):
        menu = QMenu()
        menu.addAction('canny',self.exe_canny)
        menu.addAction('test1',self.exe_canny)
        menu.addAction('test2',self.exe_canny)
        menu.exec_(QCursor.pos())

    def eventFilter(self, source, event):
        if (event.type() == QEvent.MouseButtonPress and source is self.pic_View):
            if event.button() == Qt.RightButton:
                pass
                #self.scene.clear()
                #self.scene.removeItem(self.scene.focusItem)
            else:
                pos = event.pos()
                msgbox = QMessageBox(self)
                msgbox.setText('mouse position: (%d, %d)' % (pos.x(), pos.y()))
                #ret = msgbox.exec_()
                print(pos.x(), pos.y())

                h_sbar_val = self.pic_View.horizontalScrollBar().value()
                v_sbar_val = self.pic_View.verticalScrollBar().value()

                radius = 5
                item = QGraphicsEllipseItem(pos.x()-radius+h_sbar_val, pos.y()-radius+v_sbar_val, radius*2, radius*2)
                item.setBrush(QBrush(QColor("lime")))
                item.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable | 
                                QGraphicsItem.ItemIsFocusable)

                self.scene.addItem(item)
                for i in range(1, len(self.scene.items(0))):
                    print(len(self.scene.items(0)))
                    print(self.scene.items(0)[i].rect())
                    print(self.scene.items(0)[i].scenePos())

        return QWidget.eventFilter(self, source, event)

    def open_file(self):
        self.file = QFileDialog.getOpenFileName()
        if self.file:
            self.file_edit.setText(self.file[0])
            self.scene = QGraphicsScene()
            pic_Item = QGraphicsPixmapItem(QPixmap(self.file[0]))
            __width = pic_Item.boundingRect().width()
            __height = pic_Item.boundingRect().height()
            __x = self.pic_View.x()
            __y = self.pic_View.y()
            self.pic_View.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            #self.pic_View.setGeometry(QRect(__x, __y, __width, __height))

            __main_x = int(__x + __width + 20)
            __main_y = int(__y + __height + 20)
            self.resize(__main_x, __main_y)
            self.scene.addItem(pic_Item)

            self.pic_View.setScene(self.scene)

        return self.file

    # exe_canny関数：opecvのcanny処理画像をQtのQPixmapに変換し描画
    def exe_canny(self):
        cv_test = opencv_test(self.file[0]) # opencv_testファイルからクラスの読み込み
        pic, pic2 = cv_test.open_pic(self.file[0]) # ファイルを読み込んでRとBを交換
        self.cv_img = cv_test.canny(pic2) # エッジ検出

        height, width, dim = self.cv_img.shape # 画像の高さ、幅を読み込み
        bytesPerLine = dim * width # 全ピクセル数
        self.image = QImage(self.cv_img.data, width, height, bytesPerLine, QImage.Format_RGB888) # Opencv（numpy）画像をQtのQImageに変換
        pic_Item = QGraphicsPixmapItem(QPixmap.fromImage(self.image)) # QImageをQPixmapに変換し、アイテムとして読み込む

        self.scene = QGraphicsScene()
        self.scene.addItem(pic_Item) # 画像を描画
        self.pic_View.setScene(self.scene)

    def resizeEvent(self, e):
        #print("resize="+str(e.oldSize().height()) +"_"+str(e.oldSize().width())
        # +":"+str(e.size().height()) +"_"+str(e.size().width()))

        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dmw = DesignerMainWindow()
    dmw.show()
    sys.exit(app.exec_())