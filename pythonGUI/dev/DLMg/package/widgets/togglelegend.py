from PyQt4.QtGui import *
from PyQt4.QtCore import *
import pyqtgraph as pg


class LegendWidget(QWidget):
    def __init__(self, entries):
        super(LegendWidget, self).__init__()
        self.layout = QVBoxLayout()

        self.checkboxes = []
        self.colorpicker = []
        self.isPlotting = []

        # Add Legend Title
        self.legendtitle = QLabel()
        self.legendtitle.setText('Legend')
        self.legendtitle.setAlignment(Qt.AlignCenter)
        self.legendtitle.setFont(self.boldfont(16))
        self.layout.addWidget(self.legendtitle)

        for entry in entries:
            icheckbox = QCheckBox()
            icheckbox.setText(entry)
            icheckbox.stateChanged.connect(self.changeState)

            icheckbox.setFixedSize(icheckbox.minimumSizeHint())
            icolorbutton = pg.ColorButton()
            icolorbutton.setFixedWidth(50)

            self.checkboxes.append(icheckbox)
            self.colorpicker.append(icolorbutton)
            self.isPlotting.append(False)

        for icheckbox, icolorpicker in zip(self.checkboxes, self.colorpicker):
            iLayout = QHBoxLayout()
            iLayout.addWidget(icheckbox)

            hline1 = QFrame()
            hline1.setFrameStyle(QFrame.HLine | QFrame.Raised)
            iLayout.addWidget(hline1)

            iLayout.addWidget(icolorpicker)
            self.layout.addLayout(iLayout)

        self.setLayout(self.layout)

        self.changeState()

    def boldfont(self, fontsize):
        return QFont("Times", fontsize, QFont.Bold)

    def changeState(self):
        for icheckbox, icolorpicker in zip(self.checkboxes, self.colorpicker):
            if icheckbox.isChecked():
                icolorpicker.setEnabled(True)
            else:
                icolorpicker.setEnabled(False)

        for i in range(0,len(self.checkboxes)):
            if self.checkboxes[i].isChecked():
                self.isPlotting[i] = True
            else:
                self.isPlotting[i] = False
