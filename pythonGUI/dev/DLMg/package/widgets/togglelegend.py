from PyQt4.QtGui import *
from PyQt4.QtCore import *
import pyqtgraph as pg


class LegendWidget(QWidget):
    def __init__(self, entries):
        super(LegendWidget, self).__init__()
        self.layout = QVBoxLayout()

        self.checkboxes = []
        self.colorpicker = []

        # Add Legend Title
        self.legendtitle = QLabel()
        self.legendtitle.setText('Legend')
        self.legendtitle.setAlignment(Qt.AlignCenter)
        self.legendtitle.setFont(self.boldfont(16))
        self.layout.addWidget(self.legendtitle)

        for entry in entries:
            icheckbox = QCheckBox()
            icheckbox.setText(entry)
            icolorbutton = pg.ColorButton()
            icolorbutton.setFixedWidth(50)
            self.checkboxes.append(icheckbox)
            self.colorpicker.append(icolorbutton)

        for icheckbox, icolorpicker in zip(self.checkboxes, self.colorpicker):
            iLayout = QHBoxLayout()
            iLayout.addWidget(icheckbox)
            iLayout.addWidget(icolorpicker)
            self.layout.addLayout(iLayout)

        self.setLayout(self.layout)

    def boldfont(self, fontsize):
        return QFont("Times", fontsize, QFont.Bold)
