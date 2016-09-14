from PyQt4.QtGui import *
from PyQt4.QtCore import *


class SaveData(QWidget):
    def __init__(self):
        super(SaveData, self).__init__()

        self.layout = QVBoxLayout()

        # title of widget
        self.title = QLabel()
        self.title.setText('Save Data')
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(self.boldfont(16))
        self.layout.addWidget(self.title)

        # file select
        self.layout_middle = QHBoxLayout()
        self.checkBox = QCheckBox()
        self.checkBox.setText("File Name")
        self.checkBox.stateChanged.connect(self.updateStatus)
        self.lineEdit = QLineEdit()
        self.filebtn = QPushButton("...")
        self.filebtn.clicked.connect(self.selectFile)
        self.layout_middle.addWidget(self.checkBox)
        self.layout_middle.addWidget(self.lineEdit)
        self.layout_middle.addWidget(self.filebtn)
        self.layout.addLayout(self.layout_middle)

        # start and stop buttons
        self.startbutton = QPushButton('Start')
        self.startbutton.clicked.connect(self.startAction)
        self.stopbutton = QPushButton('Stop')
        self.stopbutton.clicked.connect(self.stopAction)
        self.savebutton = QPushButton('Save')

        self.layout_bottom = QHBoxLayout()
        self.layout_bottom.addWidget(self.startbutton)
        self.layout_bottom.addWidget(self.stopbutton)
        self.layout_bottom.addWidget(self.savebutton)
        self.layout.addLayout(self.layout_bottom)

        # add flags for reading/saving data
        self.doreaddata = [False]
        self.dowritedata = [False]

        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        self.updateStatus()

    def selectFile(self):
        dlg = QFileDialog()
        self.lineEdit.setText(dlg.getSaveFileName(dlg, "Select Output File", None, "Text Files (*.txt)"))

    def boldfont(self, fontsize):
        return QFont("Times", fontsize, QFont.Bold)

    def updateStatus(self):
        if self.checkBox.isChecked():
            self.filebtn.setEnabled(True)
            self.lineEdit.setEnabled(True)
            self.savebutton.setEnabled(True)
        else:
            self.filebtn.setEnabled(False)
            self.lineEdit.setEnabled(False)
            self.savebutton.setEnabled(False)
            self.lineEdit.setText("")

    def startAction(self):
        self.startbutton.setEnabled(False)
        self.stopbutton.setEnabled(True)
        self.savebutton.setEnabled(False)
        self.doreaddata[0] = True
        if self.checkBox.isEnabled():
            self.dowritedata[0] = True
        else:
            self.doreaddata[0] = False

    def stopAction(self):
        self.stopbutton.setEnabled(False)
        self.startbutton.setEnabled(True)
        if self.checkBox.isChecked():
            self.savebutton.setEnabled(True)

        self.doreaddata[0] = False
        self.dowritedata[0] = False
        self.startbutton.setText("Restart")
