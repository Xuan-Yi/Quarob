import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Components.ConnectionArea import ConnectionArea
from Components.FileArea import FileArea

from Containers.controlPage import ControlPage
from Containers.trainPage import TrainPage
from Containers.finetunePage import FinetunePage

windows = {
    'Finetune mode': 'finetune',
    'Control mode': 'control',
    'Train mode': 'train'
}


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        # self.window_mode presented in combobox denotion
        self.window_mode = 'Finetune mode'
        # Do NOT use showFullScreen(), or entire screen would be occupied.
        self.showMaximized()   # full screen
        self.setWindowIcon(QIcon('materials\icon.png'))
        self.setWindowTitle("Quarob App")
        self.menubar()
        # central widget
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.refresh_main_widget()

    def menubar(self):
        menubar = self.menuBar()
        # Filemenu
        filemenu = menubar.addMenu('File')

        actionNew = QAction('New', self)
        actionNew.setShortcut('Ctrl+N')
        actionOpen = QAction('Open', self)
        actionOpen.setShortcut('Ctrl+O')
        filemenu.addActions([actionNew, actionOpen])
        filemenu.addSeparator()

        filemenu.addSeparator()

        actionSave = QAction('Save', self)
        actionSave.setShortcut('Ctrl+S')
        actionSave_As = QAction('Save As', self)
        filemenu.addActions([actionSave, actionSave_As])

        filemenu.addSeparator()

        actionQuit = QAction('Quit', self)
        actionQuit.setShortcut('Ctrl+Q')
        filemenu.addActions([actionQuit])

    def refresh_main_widget(self):
        # connection area
        self.connectionArea = ConnectionArea(self.window_mode)
        self.fileArea = FileArea()
        self.connectionArea.mode_combo_change_event_connect(self.change_mode)
        # change central widget
        main_areas = [self.connectionArea, self.fileArea]

        win_mode = windows[self.window_mode]

        if win_mode == 'control':
            page = ControlPage(main_areas)
        elif win_mode == 'train':
            page = TrainPage(main_areas)
        elif win_mode == 'finetune':
            page = FinetunePage(main_areas)
        else:
            print('Something went wrong.')
        self.central_widget.addWidget(page)
        self.central_widget.setCurrentWidget(page)

    def change_mode(self):
        self.window_mode = self.connectionArea.get_window_mode()
        self.refresh_main_widget()


if __name__ == '__main__':
    app = QApplication(sys.argv)    # 系統視窗程式
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())   # 偵測視窗關閉後結束程式
