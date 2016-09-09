from PyQt4.QtGui import *
from PyQt4.QtCore import *
from package.widgets.togglelegend import LegendWidget
from package.widgets.plotsettings import PlotSettings
from package.widgets.statuswindow import StatusWindow
from package.widgets.savedata import SaveData

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
        # create widgets
        self.widget_legend = LegendWidget(legendEntries)
        self.widget_settings = PlotSettings(settingsEntries)
        self.widget_plot = pg.PlotWidget()
        self.widget_status = StatusWindow()
        self.widget_savedata = SaveData()

        # create title for layouts

        # build ui
        self.build_ui()

        # make connections
        self.widget_status.addstatus('test')
        self.widget_status.addstatus('test2')
        self.widget_status.addstatus('test3')
        self.widget_status.addstatus('test4')

        # load default values

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
        self.layout_right.addWidget(self.widget_bottom)
        self.widget_bottom.setLayout(self.layout_bottom)
        self.layout_bottom.addWidget(self.widget_status)
        self.layout_right.addWidget(vline2)
        self.layout_bottom.addWidget(self.widget_savedata)

        # Size Left and Bottom Layouts
        self.widget_left.setFixedWidth(200)
        self.widget_bottom.setFixedHeight(200)

        # Add Color
        self.widget_legend.setAutoFillBackground(True)
        p = self.widget_legend.palette()
        p.setColor(self.widget_legend.backgroundRole(), Qt.gray)
        self.widget_legend.setPalette(p)
        # Set Widget Names
