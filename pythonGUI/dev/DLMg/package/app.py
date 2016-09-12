from package.ui.windows import MainWindow
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import *


def run(argv):
    app = QApplication(argv)
    win = MainWindow()
    win.show()
    # start update timer
    timer = QTimer()
    timer.timeout.connect(win.updateAll)
    timer.start(100)

    app.exec_()
