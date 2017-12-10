import sys

import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class BarPlot():
    def __init__(self, parent=None):
        
        # Create the mpl Figure and FigCanvas objects.
        # 5x4 inches, 100 dots-per-inch
        self.dpi = 100
        self.fig = Figure((5,4), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)    #pass a figure to the canvas
        self.canvas.setParent(parent)
        
        self.axes = self.fig.add_subplot(111)
        
        self.data = [1,2,3,1,2,3]


    def on_draw(self):
        """
        redraw the figure
        """
        self.axes.clear()
        self.axes.grid()

        x = range(len(self.data))
        self.axes.bar(left=x, height=self.data, width=0.3, align='center', alpha=0.44, picker=5)
        self.canvas.draw()

class AppForm(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.creat_main_window()
        self.barplot.on_draw()

    def creat_main_window(self):
        self.main_frame = QWidget()
        self.barplot = BarPlot(self.main_frame)

        #set layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.barplot.canvas)    #add canvs to the layout

        self.main_frame.setLayout(vbox)

        #set widget
        self.setCentralWidget(self.main_frame)
        
def main(args):
    app = QApplication(args)
    form = AppForm()
    form.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main(sys.argv)
