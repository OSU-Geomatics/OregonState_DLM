from PyQt4.QtGui import *
from PyQt4.QtCore import *
import pyqtgraph as pg

class MyPlotWidget(pg.PlotWidget):
    def __init__(self):
        super(MyPlotWidget, self).__init__()
        self.plotItem.setLabel('left','Acceleration','g')
        self.plotItem.setLabel('bottom', 'Time', 's')
        self.plotItem.setTitle('DLM Accelerations')

    def updateSettings(self):
        print("test")