from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class ScrollArea(QScrollArea):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        font = QFont('Segoe UI', 11)
        self.scrollAreaWidgetContents =QWidget()
        self.setWidget(self.scrollAreaWidgetContents)
        self.setFont(font)
        