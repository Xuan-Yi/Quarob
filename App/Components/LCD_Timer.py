from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from anyio import current_time


class LCD_Timer(QGridLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font = QFont("Modern", 14)
        self.initTimer()

    def initTimer(self):
        label = QLabel("Timer: ")
        label.setFont(QFont('Segoe UI', 11))
        self.addWidget(label, 0, 0, 1, 2)
        # LCD Display
        self.LCD = QLCDNumber()
        self.LCD.setDigitCount(10)
        self.LCD.setStyleSheet("border: transparent;")
        self.LCD.setMode(QLCDNumber.Dec)
        self.setValue(0)
        self.addWidget(self.LCD, 0, 2, 1, 6)
        # timer

        self.time = QTimer()
        self.time.setInterval(1000)
        self.active = False

        return self.layout

    def setValue(self, second: int):
        sec = int(second % 60)
        min = int((second/60) % 60)
        hr = int((second/3600) % 24)
        day = int((second/86400) % 10)
        self.LCD.display(f'{day}:{hr}:{min}:{sec}')

    def refresh(self):
        current_time = QDateTime.currentSecsSinceEpoch()
        interval = current_time-self.init_time  # sec
        self.setValue(interval)

    def start_timer(self):
        if not self.active:
            self.init_time = QDateTime.currentSecsSinceEpoch()
            self.active = True
            self.time.timeout.connect(self.refresh)
            self.time.start()

    def end_timer(self):
        if self.active:
            self.init_time = QDateTime.currentSecsSinceEpoch()
            self.time.stop()

    def clear_timer(self):
        if self.active:
            self.end_timer()
            self.setValue(0)
            self.active = False
