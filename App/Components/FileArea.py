from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class FileArea(QGridLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font = QFont('Segoe UI', 11)
        self.initFileArea()

    def initFileArea(self):
        self.setSpacing(14)

        filename_label = QLabel('File: ')
        filename_label.setFont(QFont('Segoe UI', 11, QFont.Bold))
        self.file_name = QLabel('')
        self.file_name.setFont(self.font)
        load_from_quarob_btn = QPushButton('Load from Quarob')
        load_from_quarob_btn.setFont(self.font)
        load_to_quarob_btn = QPushButton('Load to Quarob')
        load_to_quarob_btn.setFont(self.font)

        self.addWidget(filename_label, 0, 0, 1, 1)
        self.addWidget(self.file_name, 0, 1, 1, 5)
        self.addWidget(load_from_quarob_btn, 1, 0, 1, 6)
        self.addWidget(load_to_quarob_btn, 2, 0, 1, 6)
