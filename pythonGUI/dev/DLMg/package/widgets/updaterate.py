from PyQt4.QtGui import *
from PyQt4.QtCore import *


class UpdateRate(QWidget):
    def __init__(self, names):
        super(UpdateRate, self).__init__()

        self.hlayout = QHBoxLayout()

        self.lblTitles = []
        self.curRate = []
        for iname in names:
            ilbl = QLabel(iname)
            ilbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            icur = QLabel("")
            self.hlayout.addWidget(ilbl)
            self.hlayout.addWidget(icur)

            self.lblTitles.append(ilbl)
            self.curRate.append(icur)

        self.setLayout(self.hlayout)

    def setrates(self, rates):
        for iRate, iRateLabel in zip(rates, self.curRate):
            strval = "%03.1f" % iRate
            iRateLabel.setText(strval)
