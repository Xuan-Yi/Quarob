from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Components.Lines import QHLine
from Components.OpenGLWidget import OpenGLWidget


class ControlPage(QWidget):
    def __init__(self, main_area, *args, **kwargs):
        super().__init__(*args, **kwargs)
        [self.connection_area, self.file_area] = main_area
        self.font = QFont('Segoe UI', 11)
        self.initUI()

    def initUI(self):
        self.showFullScreen()
        self.layout = QGridLayout()
        self.layout.setSpacing(12)
        # monitor
        self.monitor = OpenGLWidget('3D')
        self.layout.addWidget(self.monitor, 0, 0, 64, 64)
        # control panel
        control_panel = self.build_panel()
        self.layout.addItem(control_panel, 0, 64, 64, 24)
        self.setLayout(self.layout)

    def build_panel(self):
        v_layout = QGridLayout()
        v_layout.setSpacing(14)
        # Part1
        splitter1 = QHLine()

        v_layout.addItem(self.connection_area, 0, 0, 1, 6)
        v_layout.addWidget(splitter1, 1, 0, 1, 6)

        # Part2
        perpective_label = QLabel('Perspective: ')
        perpective_label.setFont(self.font)
        self.LD_rbtn = QRadioButton('Look Down')
        self.LD_rbtn.setChecked(False)  # default Perspective = '3D'
        self.LD_rbtn.toggled.connect(self.LD_rbtn_on_toggle)
        self.LD_rbtn.setFont(self.font)
        self._3D_rbtn = QRadioButton('3D')
        self._3D_rbtn.setChecked(True)  # default Perspective = '3D'
        self._3D_rbtn.toggled.connect(self._3D_rbtn_on_toggle)
        self._3D_rbtn.setFont(self.font)
        self.sub_monitor = OpenGLWidget('Look Down')
        stand_btn = QPushButton('Stand up')
        stand_btn.setFont(self.font)
        sit_down_btn = QPushButton('Sit Down')
        sit_down_btn.setFont(self.font)
        splitter2 = QHLine()

        v_layout.addWidget(perpective_label, 2, 0, 1, 2)
        v_layout.addWidget(self.LD_rbtn, 2, 2, 1, 2)
        v_layout.addWidget(self._3D_rbtn, 2, 4, 1, 2)
        v_layout.addWidget(self.sub_monitor, 3, 0, 6, 6)
        v_layout.addWidget(stand_btn, 9, 0, 1, 3)
        v_layout.addWidget(sit_down_btn, 9, 3, 1, 3)
        v_layout.addWidget(splitter2, 10, 0, 1, 6)

        # Part3
        v_layout.addItem(self.file_area, 11, 0, 1, 6)

        return v_layout

    def LD_rbtn_on_toggle(self):
        if self.LD_rbtn.isChecked():
            self.monitor.setPerspective('Look Down')
            self.sub_monitor.setPerspective('3D')
            self._3D_rbtn.setChecked(False)

    def _3D_rbtn_on_toggle(self):
        if self._3D_rbtn.isChecked():
            self.monitor.setPerspective('3D')
            self.sub_monitor.setPerspective('Look Down')
            self.LD_rbtn.setChecked(False)
