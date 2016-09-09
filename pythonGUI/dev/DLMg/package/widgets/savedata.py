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
        self.lineEdit = QLineEdit()
        self.filebtn = QPushButton("...")
        self.filebtn.clicked.connect(self.selectFile)
        self.layout_middle.addWidget(self.checkBox)
        self.layout_middle.addWidget(self.lineEdit)
        self.layout_middle.addWidget(self.filebtn)
        self.layout.addLayout(self.layout_middle)

        # start and stop buttons
        self.startbutton = QPushButton('Start')
        self.stopbutton = QPushButton('Start')
        self.layout_bottom = QHBoxLayout()
        self.layout_bottom.addWidget(self.startbutton)
        self.layout_bottom.addWidget(self.stopbutton)
        self.layout.addLayout(self.layout_bottom)

        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

    def selectFile(self):

        self.lineEdit.setText(QFileDialog.getSaveFileName(self, "Select Output File", None, "Text Files (*.txt)"))

    def boldfont(self, fontsize):
        return QFont("Times", fontsize, QFont.Bold)