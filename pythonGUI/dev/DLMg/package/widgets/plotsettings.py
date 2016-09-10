from PyQt4.QtGui import *
from PyQt4.QtCore import *

class PlotSettings(QWidget):
    def __init__(self, entries):
        super(PlotSettings, self).__init__()
        self.layout = QVBoxLayout()

        self.checkboxes = []
        self.textinput = []

        # Add Legend Title
        self.settingstitle = QLabel()
        self.settingstitle.setText('Plot Settings')
        self.settingstitle.setAlignment(Qt.AlignCenter)
        self.settingstitle.setFont(self.boldfont(16))
        self.layout.addWidget(self.settingstitle)

        for entry in entries:
            icheckbox = QCheckBox()
            icheckbox.setText(entry)
            icheckbox.stateChanged.connect(self.changeState)

            itextinput = QSpinBox()
            itextinput.setFixedWidth(50)
            self.checkboxes.append(icheckbox)
            self.textinput.append(itextinput)

        for icheckbox, itextinput in zip(self.checkboxes, self.textinput):
            iLayout = QHBoxLayout()
            iLayout.addWidget(icheckbox)
            iLayout.addWidget(itextinput)
            self.layout.addLayout(iLayout)

        self.layout.setAlignment(Qt.AlignTop)

        self.setLayout(self.layout)

        self.changeState()

    def boldfont(self, fontsize):
        return QFont("Times", fontsize, QFont.Bold)

    def changeState(self):
        for icheckbox, itextinput in zip(self.checkboxes, self.textinput):
            if icheckbox.isChecked():
                itextinput.setEnabled(True)
            else:
                itextinput.setEnabled(False)