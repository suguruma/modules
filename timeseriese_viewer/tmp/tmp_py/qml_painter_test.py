# -*- coding: utf-8 -*-

from os.path import join,dirname
import json

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView
from PyQt5.QtCore import * #QUrl, QTimer

class QtPainter(QQuickView):
    def __init__(self, parent=None):

        QQuickView.__init__(self)
        self.setParent(parent)
        self.value = ""

        json_init = json.dumps(
            {'OnRightHand': 0, 'ColorRightHand': 0,
             'OnLeftHand': 0, 'ColorLeftHand': 0,
             'OnRightArm': 0, 'ColorRightArm': 0,
             'OnLeftArm': 0, 'ColorLeftArm': 0,
             'OnHead': 0, 'ColorHead': 0},
            sort_keys=True, indent=4, separators=(',', ': ')
        )
        self.AnalyzeJsonFile(json_init)
        self.UpdateFigure()

    def AnalyzeJsonFile(self, json_strings):
        try:
            json_data = json.loads(json_strings) # json.loads(msg.payload.decode('utf-8'))
            key_list = json_data.keys()
            for k in key_list:
                if '' == k:
                    print("Empty message is sent")
                elif 'OnRightHand' == k:
                    self.OnRightHand = json_data[k]
                elif 'ColorRightHand' == k:
                    self.ColorRightHand = json_data[k]
                elif 'OnLeftHand' == k:
                    self.OnLeftHand = json_data[k]
                elif 'ColorLeftHand' == k:
                    self.ColorLeftHand = json_data[k]
                elif 'OnRightArm' == k:
                    self.OnRightArm = json_data[k]
                elif 'ColorRightArm' == k:
                    self.ColorRightArm = json_data[k]
                elif 'OnLeftArm' == k:
                    self.OnLeftArm = json_data[k]
                elif 'ColorLeftArm' == k:
                    self.ColorLeftArm = json_data[k]
                elif 'OnHead' == k:
                    self.OnHead = json_data[k]
                elif 'ColorHead' == k:
                    self.ColorHead = json_data[k]
                else:
                    print("Nonregistered key is sent : {0}".format(k))
        except:
            print("Sent file is not correct")

    def UpdateFigure(self):

        url = QUrl.fromLocalFile("PointingViewer.qml")

        #url = QUrl(join(dirname(__file__), 'PointingViewer.qml'))
        self.setSource(url)
        self.rootContext().setContextProperty("OnRightHand", self.OnRightHand);
        self.rootContext().setContextProperty("ColorRightHand", self.ColorRightHand);
        self.rootContext().setContextProperty("OnLeftHand", self.OnLeftHand);
        self.rootContext().setContextProperty("ColorLeftHand", self.ColorLeftHand);
        self.rootContext().setContextProperty("OnRightArm",  self.OnRightArm);
        self.rootContext().setContextProperty("ColorRightArm", self.ColorRightArm);
        self.rootContext().setContextProperty("OnLeftArm", self.OnLeftArm);
        self.rootContext().setContextProperty("ColorLeftArm", self.ColorLeftArm );
        self.rootContext().setContextProperty("OnHead", self.OnHead);
        self.rootContext().setContextProperty("ColorHead", self.ColorHead);


if __name__ == '__main__':
    '''
    import sys

    ### GUI
    app = QGuiApplication(sys.argv)
    view = QQuickView()
    view.engine().quit.connect(app.quit)

    ### Viewer
    QtPainterWindow = QtPainter()
    QtPainterWindow.show()

    ### Exit
    view.rootContext().setContextProperty("subfunc", QtPainterWindow);
    sys.exit(app.exec_())
    '''
    import sys
    app = QApplication(sys.argv)

    view = QQuickView()
    view.setSource(QUrl('PointingViewer.qml'))
    view.show()

    sys.exit(app.exec_())
