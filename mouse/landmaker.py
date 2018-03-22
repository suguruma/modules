from __future__ import with_statement

import sys
from PyQt5.QtCore import (QObject, Qt, QUrl, QTimer, QModelIndex, QPoint, QRect, QEvent,
                            QAbstractItemModel
                            )
from PyQt5.QtGui import (QStandardItemModel, QStandardItem, QPixmap, QKeySequence, QImage, QCursor, 
                            QPainter, QBrush, QColor
                            )
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
                                QPushButton, QComboBox, QCheckBox, QLabel, QSpinBox, QLineEdit, QListView,
                                QLCDNumber, QSlider, QTableWidget, QTableWidgetItem, QAction, QFileDialog,
                                QMessageBox, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView,
                                QMenu, QGraphicsItem, QGraphicsEllipseItem, QTreeView, QAbstractItemView,
                                QStyledItemDelegate, QGroupBox, QRadioButton
                                )
import numpy as np
import cv2

class Model(QAbstractItemModel):
    headers = 'トッピング', 'うどん/そば', '温/冷', 'POS'
    def __init__(self, parent=None):
        super(Model, self).__init__(parent)
        self.items = [
            ['たぬき','そば','温'],
            ['きつね','うどん','温'],
            ['月見','うどん','冷'],
            ['天ぷら','そば','温'],
            ]

    def index(self, row, column, parent=QModelIndex()):
        return self.createIndex(row, column, None)

    def parent(self, child):
        return QModelIndex()

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            try:
                return self.items[index.row()][index.column()]
            except:
                return
        return

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return
        if orientation == Qt.Horizontal:
            return self.headers[section]

    def addRow(self, topping, menkind, hotcold, tmp = 1):
        self.beginInsertRows(QModelIndex(), len(self.items), 1)
        self.items.append([topping, menkind, hotcold, tmp])
        self.endInsertRows()

    def removeRows(self, rowIndexes):
        for row in sorted(rowIndexes, reverse=True):
            self.beginRemoveRows(QModelIndex(), row, row + 1)
            del self.items[row]
            self.endRemoveRows()

    def flags(self, index):
        return super(Model, self).flags(index) | Qt.ItemIsEditable

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            self.items[index.row()][index.column()] = value
            return True
        return False


class View(QTreeView):
    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        self.setItemsExpandable(False)
        self.setIndentation(0)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def drawBranches(self, painter, rect, index):
        return


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

class InputWidget(QWidget):
    toppings = 'きつね', 'たぬき', '天ぷら', '月見', '肉', 'カレー'
    noodles = 'うどん', 'そば'
    hotcold = '温', '冷'
    columns = toppings, noodles, hotcold

    def __init__(self, parent=None):
        super(InputWidget, self).__init__(parent)
        layout = QVBoxLayout()

        self.toppingInput = InputWidget.comboBox(InputWidget.toppings)
        layout.addWidget(self.toppingInput)

        grpbox, self.noodles = InputWidget.radioButtons(InputWidget.noodles)
        layout.addWidget(grpbox)

        grpbox, self.hotcold = InputWidget.radioButtons(InputWidget.hotcold)
        layout.addWidget(grpbox)

        self.addButton = QPushButton('確定')
        layout.addWidget(self.addButton)

        layout.addStretch()

        self.setLayout(layout)

    @staticmethod
    def comboBox(values):
        comboBox = QComboBox()
        for value in values:
            comboBox.addItem(value)
        return comboBox

    @staticmethod
    def radioButtons(values):
        grpbox = QGroupBox()
        layout = QHBoxLayout()
        buttons = []
        for value in values:
            rb = QRadioButton(value)
            layout.addWidget(rb)
            buttons.append(rb)
        buttons[0].setChecked(True)
        grpbox.setLayout(layout)
        return grpbox, buttons

    def values(self):
        topping = self.toppingInput.currentText()

        udonsoba = '?'
        for btn in self.noodles:
            if btn.isChecked():
                udonsoba = btn.text()
                break

        hotcold = '?'
        for btn in self.hotcold:
            if btn.isChecked():
                hotcold = btn.text()
                break

        return topping, udonsoba, hotcold

class Delegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(Delegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        editor = InputWidget.comboBox(InputWidget.columns[index.column()])
        editor.setParent(parent)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole)
        editor.setCurrentIndex(editor.findText(value))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText())

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

        ####
        self.view = View(self)
        self.model = Model(self)
        self.view.setModel(self.model)
        self.view.setItemDelegate(Delegate())
        grid.addWidget(self.view, 0, 1, 4, 1)

        self.inputWidget = InputWidget()
        self.inputWidget.addButton.clicked.connect(self.addItem)
        grid.addWidget(self.inputWidget, 0, 2, 4, 1)


        mainframe.setLayout(grid)
        self.setCentralWidget(mainframe)

        pic_view = self.pic_View

        pic_view.setContextMenuPolicy(Qt.CustomContextMenu)
        pic_view.customContextMenuRequested.connect(self.contextMenue)
        
        self.pic_View.installEventFilter(self)

    ####
    def addItem(self):
        self.model.addRow(*self.inputWidget.values())

    def selectedRows(self):
        rows = []
        for index in self.view.selectedIndexes():
            if index.column() == 0:
                rows.append(index.row())
        return rows

    def removeItems(self):
        self.model.removeRows(self.selectedRows())

    #-

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

                a = item.rect().x()
                b = item.rect().y()
                c = 0
                d = 0
                self.model.addRow(a,b,c,d)

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

            #__main_x = int(__x + __width + 20)
            #__main_y = int(__y + __height + 20)
            #self.resize(__main_x, __main_y)
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