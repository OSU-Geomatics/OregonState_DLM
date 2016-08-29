#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time
import serial

app = QtGui.QApplication([])

p = pg.plot()
p.setWindowTitle('live plot from serial')
curve = p.plot()

data = [0]
raw=serial.Serial("COM101",921600)
#raw.open()

def update():
    global curve, data
    line = raw.readline()
    rawdata = line.decode().split(',')
    if "A" in rawdata[0]:
         data.append(float(rawdata[3]))
    xdata = np.array(data, dtype='float64')
    curve.setData(xdata)
    app.processEvents()

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
