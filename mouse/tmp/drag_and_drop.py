#encoding:utf-8
import sys
from collections import deque
from PyQt5.QtCore import (Qt, QUrl, QTimer, QModelIndex, QPoint)
from PyQt5.QtGui import (QStandardItemModel, QStandardItem, QPixmap, QKeySequence)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
                               QPushButton, QComboBox, QCheckBox, QLabel, QSpinBox, QLineEdit, QListView,
                               QLCDNumber, QSlider, QTableWidget, QTableWidgetItem, QAction, QFileDialog,
                               QMessageBox
                              )
##http://w3log.hatenablog.com/entry/2012/03/14/092146

class Example(QWidget):
    def __init__(self, parent=None):
        super(Example, self).__init__(parent)
        self.setAcceptDrops(True)
        self.resize(150, 150)
        self.setWindowTitle("D&D")
        lineEdit(self)
        self.show()

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        print("\n".join(u.toLocalFile() for u in e.mimeData().urls()))

    def moveEvent(self,e):
        print("move="+str(e.oldPos().x())
            +"_"+str(e.oldPos().y())
            +":"+str(e.pos().x())
            +"_"+str(e.pos().y()))

    def resizeEvent(self,e):
        print("resize="+str(e.oldSize().height())
            +"_"+str(e.oldSize().width())
            +":"+str(e.size().height())
            +"_"+str(e.size().width()))

    def showEvent(self,e):
        print("show:"+str(e.spontaneous()))

    def wheelEvent(self,e):
        print("wheel="+str(e.delta()/8)
            +"_"+str(e.orientation())
            +":"+str(e.x())
            +"_"+str(e.y()))

    def mouseMoveEvent(self,e):
        print("mouseMove="+bin(int(e.buttons())))


class lineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(lineEdit, self).__init__(parent)
        self.move(30,30)

    def keyPressEvent(self,e):
        super(lineEdit,self).keyPressEvent(e)
        print("text="+e.text()
            +",count="+str(e.count())
            +",key="+hex(e.key())
            +",Modifiers="+hex(int(e.modifiers()))
            +",nativeVK="+str(e.nativeVirtualKey())
            +",nativeScanCode="+str(e.nativeScanCode())
            +",nativeModifiers="+bin(e.nativeModifiers())
            +",isAutoRepeat="+str(e.isAutoRepeat())
            +",matches="+str(e.matches(QKeySequence.Copy))
              )


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()