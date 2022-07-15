from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class ConnectionArea(QGridLayout):
    def __init__(self, win_mode: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSpacing(14)
        self.font = QFont('Segoe UI', 11)
        self.win_mode = win_mode
        self.initConnectionArea()

    def initConnectionArea(self):
        self.quarob_name = QLabel('No Device')
        self.quarob_name.setFont(QFont('Segoe UI', 16, QFont.Bold))
        self.connect_btn = QPushButton('Connection')
        self.connect_btn.setFont(self.font)
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(
            ['Finetune mode', 'Control mode', 'Train mode'])
        self.mode_combo.setCurrentText(self.win_mode)
        self.mode_combo.setFont(self.font)

        self.addWidget(self.quarob_name, 0, 0, 1, 6)
        self.addWidget(self.connect_btn, 1, 0, 1, 3)
        self.addWidget(self.mode_combo, 1, 3, 1, 3)

    def connect_btn_connect(self, call_back_func):
        self.connect_btn.clicked.connect(call_back_func)

    def mode_combo_change_event_connect(self, call_back_func):
        self.mode_combo.currentTextChanged.connect(call_back_func)

    def get_window_mode(self):
        # print('get text: ',self.mode_combo.currentText())
        return self.mode_combo.currentText()
