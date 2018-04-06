import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Widget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.px = None
        self.py = None
        self.points = []
        self.psets = []

    def mousePressEvent(self, event):
        self.points.append(event.pos())
        self.update()

    def mouseMoveEvent(self, event):
        self.points.append(event.pos())
        self.update()

    def mouseReleaseEvent(self, event):
        self.pressed = False
        self.psets.append(self.points)
        self.points = []
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.white)
        painter.drawRect(self.rect())

        painter.setPen(Qt.black)

        # draw historical points
        for points in self.psets:
            painter.drawPolyline(*points)
        print(len(self.psets))

        # draw current points
        print(self.points)
        if self.points:
            painter.drawPolyline(*self.points)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    w.raise_()
    sys.exit(app.exec_())