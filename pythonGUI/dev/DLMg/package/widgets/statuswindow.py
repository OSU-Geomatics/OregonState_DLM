from PyQt4.QtGui import *
from PyQt4.QtCore import *


class StatusWindow(QWidget):
    def __init__(self):
        super(StatusWindow, self).__init__()
        self.statusBox = QPlainTextEdit()
        self.statusBox.setReadOnly(True)

        self.layout = QVBoxLayout()

        self.statustitle = QLabel()
        self.statustitle.setText('Status')
        self.statustitle.setAlignment(Qt.AlignCenter)
        self.statustitle.setFont(self.boldfont(16))
        self.layout.addWidget(self.statustitle)
        self.layout.addWidget(self.statusBox)
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

    def addstatus(self, status):
        self.statusBox.appendPlainText(status)

    def boldfont(self, fontsize):
        return QFont("Times", fontsize, QFont.Bold)