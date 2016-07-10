'''
Created on 7 juin 2016

@author: saldenisov
'''
from PyQt5.Qt import QMainWindow
from PyQt5.QtGui import QCloseEvent

from utility import MainObserver
from utility import Meta
from views import Ui_MainWindow
from _functools import partial


class MainView(QMainWindow, MainObserver, metaclass=Meta):
    """
    """

    def __init__(self, in_controller, in_model, parent=None):
        """

        """
        super(QMainWindow, self).__init__(parent)
        self.controller = in_controller
        self.model = in_model

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model.add_observer(self)

        self.ui.actionHelp.triggered.connect(self.controller.help_clicked)
        self.ui.actionAuthor.triggered.connect(self.controller.author_clicked)
        self.ui.actionOpen.triggered.connect(self.controller.open_clicked)
        self.ui.actionQuit.triggered.connect(partial(self.controller.quit_clicked, QCloseEvent()))
        self.ui.button_empty.clicked.connect(self.controller.empty_clicked)
        self.ui.button_open.clicked.connect(self.controller.open_clicked)

    def loading(self):
        self.ui.button_open.click()

    def closeEvent(self, event):
        self.controller.quit_clicked(event)