from PyQt4.QtGui import *
from PyQt4.QtCore import *
import pyqtgraph as pg


class MyPlotWidget(pg.PlotWidget):
    def __init__(self, nplots):
        super(MyPlotWidget, self).__init__(enableMenu=False)
        self.plotItem.setLabel('left','Acceleration','g')
        self.plotItem.setLabel('bottom', 'Time', 's')
        self.plotItem.setTitle('DLM Accelerations')

        p = self.plotItem.plot()

        self.plot_handles = []
        for i in range(0,nplots):
            self.plot_handles.append(self.plotItem.plot())

    def setPlotLineSettings(self, colors, width):
        for i, iplot_handle in zip(range(0, len(self.plot_handles)), self.plot_handles):
            iplot_handle.curve.setPen(color=colors[i], width=width)

    def plotData(self, i, x, y):
        self.plot_handles[i].curve.setData(x, y)
