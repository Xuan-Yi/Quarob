from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Components.Lines import QHLine
from Components.ScrollArea import ScrollArea

limbs = {
    'NN': 'No',
    'FL': 'Front-left',
    'FR': 'Front-right',
    'BL': 'Back-left',
    'BR': 'Back-right'
}


class FinetunePage(QWidget):
    def __init__(self, main_area, *args, **kwargs):
        super().__init__(*args, **kwargs)
        [self.connection_area, self.file_area] = main_area
        self.font = QFont('Segoe UI', 11)
        self.initUI()

    def initUI(self):
        self.showFullScreen()
        self.layout = QGridLayout()
        self.layout.setSpacing(12)
        # limb picker
        self.limb = 'NN'
        self.limb_picker = self.build_limb_peaker()
        self.layout.addItem(self.limb_picker, 0, 0, 64, 64)
        # control panel
        control_panel = self.build_panel()
        self.layout.addItem(control_panel, 0, 64, 64, 24)
        self.setLayout(self.layout)

    def build_limb_peaker(self):
        g_layout = QGridLayout()
        g_layout.setSpacing(14)
        g_layout.setContentsMargins(120, 30, 120, 30)

        img = QLabel()
        _oimg = QPixmap.fromImage(QImage('materials\look_down.png'))
        img.setPixmap(_oimg)
        img.setAlignment(Qt.AlignCenter)
        g_layout.addWidget(img, 0, 1, 6, 6)

        # buttons
        def Square_btn(text: str):
            css_style_normal = "color: white; background-color: red; border-radius: 16px; margin: 10px; font-weight: bold;"
            css_style_activated = "color: gray; background-color: pink; border-radius: 16px; margin: 10px; font-weight: bold;"
            btn = QPushButton(text)
            btn.setFont(QFont('Segoe UI', 16))
            btn.setFixedSize(QSize(80, 80))
            btn.setStyleSheet(css_style_normal)

            def choonse_limb():
                limb = text
                if self.limb == limb:
                    self.limb = 'NN'
                    btn.setStyleSheet(css_style_normal)
                else:
                    self.limb = limb
                    for _btn in [self.FL_btn, self.FR_btn, self.BL_btn, self.BR_btn]:
                        _btn.setStyleSheet(css_style_normal)
                    btn.setStyleSheet(css_style_activated)
                self.limb_part.setText(f'{limbs[self.limb]} limb is chosen.')

            btn.released.connect(choonse_limb)
            return btn

        self.FL_btn = Square_btn('FL')
        g_layout.addWidget(self.FL_btn, 1, 0, 1, 1)
        self.FR_btn = Square_btn('FR')
        g_layout.addWidget(self.FR_btn, 1, 7, 1, 1)
        self.BL_btn = Square_btn('BL')
        g_layout.addWidget(self.BL_btn, 4, 0, 1, 1)
        self.BR_btn = Square_btn('BR')
        g_layout.addWidget(self.BR_btn, 4, 7, 1, 1)

        return g_layout

    def build_panel(self):
        v_layout = QGridLayout()
        v_layout.setSpacing(14)
        # Part1
        splitter1 = QHLine()

        v_layout.addItem(self.connection_area, 0, 0, 1, 6)
        v_layout.addWidget(splitter1, 1, 0, 1, 6)

        # Part2
        self.limb_part = QLabel('No limb is chosen.')
        self.limb_part.setFont(QFont('Segoe UI', 13, QFont.Bold))

        def double_spin_set(text: str):
            h_layout = QGridLayout()
            h_layout.setSpacing(14)

            label = QLabel(text)
            label.setFont(self.font)
            spin = QDoubleSpinBox()
            spin.setFont(self.font)
            spin.setValue(0.0)

            h_layout.addWidget(label, 0, 0, 1, 3)
            h_layout.addWidget(spin, 0, 3, 1, 3)

            return h_layout

        c_spin = double_spin_set('Chest')
        s_spin = double_spin_set('Shoulder')
        e_spin = double_spin_set('Elbow')

        message_monitor = ScrollArea()
        message_monitor.setFont(self.font)
        # message_monitor.setMinimumSize(200, 200)

        locate_btn = QPushButton('Locate')
        locate_btn.setFont(self.font)
        set_offset_btn = QPushButton('Set Offset')
        set_offset_btn.setFont(self.font)
        splitter2 = QHLine()

        v_layout.addWidget(self.limb_part, 2, 0, 1, 6)
        v_layout.addItem(c_spin, 3, 0, 1, 6)
        v_layout.addItem(s_spin, 4, 0, 1, 6)
        v_layout.addItem(e_spin, 5, 0, 1, 6)
        v_layout.addWidget(message_monitor, 6, 0, 1, 6)
        v_layout.addWidget(locate_btn, 7, 0, 1, 3)
        v_layout.addWidget(set_offset_btn, 7, 3, 1, 3)
        v_layout.addWidget(splitter2, 8, 0, 1, 6)

        # Part3
        v_layout.addItem(self.file_area, 9, 0, 1, 6)

        return v_layout
