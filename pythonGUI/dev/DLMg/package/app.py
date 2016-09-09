from package.ui.windows import MainWindow
from PyQt4.QtGui import QApplication


def run(argv):
    app = QApplication(argv)
    win = MainWindow()
    win.show()
    app.exec_()
