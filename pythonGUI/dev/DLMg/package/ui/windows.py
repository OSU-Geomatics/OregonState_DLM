from PyQt4.QtGui import *
from PyQt4.QtCore import *
from package.widgets.togglelegend import LegendWidget
from package.widgets.plotsettings import PlotSettings
from package.widgets.statuswindow import StatusWindow
from package.widgets.savedata import SaveData
from package.widgets.updaterate import UpdateRate
from package.widgets.myplotwidget import MyPlotWidget
from package.sensors.finddlmports import dlmfindcomports
from package.sensors.acceldata import acceldata4

import pyqtgraph as pg
import time

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Desktop Learning Module")
        self.setWindowIcon(QIcon('img/logo.ico'))
        self.setGeometry(300, 300, 1200, 800)

        # create layouts/widgets containing layouts for size constraints
        self.frame_main = QWidget()
        self.layout_main = QHBoxLayout()
        self.layout_left = QVBoxLayout()
        self.layout_right = QVBoxLayout()
        self.layout_bottom = QHBoxLayout()
        self.widget_left = QWidget()
        self.widget_bottom = QWidget()

        # define widget parameters
        legendEntries = ('Ax', 'Ay', 'Az', 'Atot',
                         'Bx', 'By', 'Bz', 'Btot',
                         'Cx', 'Cy', 'Cz', 'Ctot',
                         'Dx', 'Dy', 'Dz', 'Dtot')
        settingsEntries = ('Scrolling dt',
                           'maxY axis',
                           'minY axis',
                           'Line Thickness',
                           )
        updateNames = ("A(Hz):", "B(Hz):", "C(Hz):", "D(Hz):", "fps:")

        # create widgets
        self.widget_legend = LegendWidget(legendEntries)
        self.widget_settings = PlotSettings(settingsEntries)
        self.widget_plot = MyPlotWidget()
        self.widget_updateRate = UpdateRate(updateNames)
        self.widget_status = StatusWindow()
        self.widget_savedata = SaveData()

        # build ui
        self.build_ui()

        # load default values
        self.load_defaults()

        # initialize data class
        self.com1, self.com2 = self.testcomports()
        self.data = acceldata4(self.com1, self.com2)

        # add data pointers to plot widget
        self.set_plotData()

        # start data threads
        self.data.startReaderThread(self.com1, self.widget_savedata.doreaddata)
        self.data.startReaderThread(self.com2, self.widget_savedata.doreaddata)

        # start update timer
        timer = QTimer()
        timer.timeout.connect(self.updateAll)
        timer.start(0)

    def testcomports(self):
        # connect to COM ports
        com1, com2, issuccess = dlmfindcomports()
        if issuccess:
            self.addStatus('Connected to ' + com1)
            self.addStatus('Connected to ' + com2)
            # initialize data array
        else:
            self.addStatus('Unsuccessful COM port detection')
        return [com1, com2]

    def set_plotData(self):
        p = []
        for i in range(0,15):
            p[i] =self.widget_plot.plot()

    def load_defaults(self):
        # legend
        self.widget_legend.checkboxes[3].setChecked(True)
        self.widget_legend.colorpicker[3].setColor((255, 0, 0))

        self.widget_legend.checkboxes[7].setChecked(True)
        self.widget_legend.colorpicker[7].setColor((0, 255, 0))

        self.widget_legend.checkboxes[11].setChecked(True)
        self.widget_legend.colorpicker[11].setColor((0, 0, 255))

        self.widget_legend.checkboxes[15].setChecked(True)
        self.widget_legend.colorpicker[15].setColor((255, 255, 0))

        # Add legend Color
        self.widget_legend.setAutoFillBackground(True)
        p = self.widget_legend.palette()
        p.setColor(self.widget_legend.backgroundRole(), Qt.lightGray)
        self.widget_legend.setPalette(p)

        # plot settings
        isTrue = (True, True, True, True)
        defaultValue = (10, 8, 0, 0)
        defaultMin = (1, -10, -10, 1)
        defaultMax = (1000, 10, 10, 10)

        for i in range(0,4):
            self.widget_settings.checkboxes[i].setChecked(isTrue[i])
            self.widget_settings.textinput[i].setValue(defaultValue[i])
            self.widget_settings.textinput[i].setMinimum(defaultMin[i])
            self.widget_settings.textinput[i].setMaximum(defaultMax[i])

        # update rate
        self.widget_updateRate.setrates((0, 0, 0, 0, 0))

        # status
        self.widget_status.addstatus('GUI initialized')

        # save data
        self.widget_savedata.checkBox.setChecked(False)
        self.widget_savedata.stopbutton.setEnabled(False)

    def build_ui(self):
        # make cosmetic lines
        vline1 = QFrame(self.frame_main)
        vline2 = QFrame(self.frame_main)
        hline1 = QFrame(self.frame_main)
        hline2 = QFrame(self.frame_main)
        vline1.setFrameStyle(QFrame.VLine | QFrame.Raised)
        vline2.setFrameStyle(QFrame.VLine | QFrame.Raised)
        hline1.setFrameStyle(QFrame.HLine | QFrame.Raised)
        hline2.setFrameStyle(QFrame.HLine | QFrame.Raised)

        # Build layouts
        self.setCentralWidget(self.frame_main)
        self.frame_main.setLayout(self.layout_main)
        self.layout_main.addWidget(self.widget_left)
        self.layout_main.addWidget(vline1)
        self.layout_main.addLayout(self.layout_right)
        self.widget_left.setLayout(self.layout_left)
        self.layout_left.addWidget(self.widget_legend)
        self.layout_left.addWidget(hline1)
        self.layout_left.addWidget(self.widget_settings)
        self.layout_right.addWidget(self.widget_plot)
        self.layout_right.addWidget(hline2)
        self.layout_right.addWidget(self.widget_updateRate)
        self.layout_right.addWidget(self.widget_bottom)
        self.widget_bottom.setLayout(self.layout_bottom)
        self.layout_bottom.addWidget(self.widget_status)
        self.layout_right.addWidget(vline2)
        self.layout_bottom.addWidget(self.widget_savedata)

        # Size Left and Bottom Layouts
        self.widget_left.setFixedWidth(200)
        self.widget_bottom.setFixedHeight(175)

        # Set Widget Names

    def updateAll(self):
        print("??")
        self.update()
        self.widget_legend.update()
        self.widget_settings.update()
        self.widget_plot.update()
        self.widget_updateRate.update()
        self.widget_status.update()
        self.widget_savedata.update()
        print("A")

    def addStatus(self, status):
        self.widget_status.addstatus(status)