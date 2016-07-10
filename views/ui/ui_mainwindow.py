'''
Created on 7 juin 2016

@author: saldenisov
'''
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QVBoxLayout,
                             QHBoxLayout, QTreeView,
                             QFileSystemModel, QSplitter,
                             QListWidget, QGroupBox,
                             QPushButton)


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(50, 50, 200, 400)
        MainWindow.resize(250, 250)
        self.main_widget = QtWidgets.QWidget(MainWindow)
        self.main_widget.setObjectName("main_widget")
        MainWindow.setCentralWidget(self.main_widget)

        self.layout_main = QVBoxLayout(self.main_widget)
        self.layout_control = QVBoxLayout()

        self.groupbox_control = QGroupBox(self.main_widget)
        self.groupbox_control.setLayout(self.layout_control)

        self.button_open = QPushButton('Open')
        self.button_empty = QPushButton('Open Empty')

        self.layout_control.addWidget(self.button_open)
        self.layout_control.addWidget(self.button_empty)

        self.layout_main.addWidget(self.groupbox_control)


        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 22))
        self.menubar.setObjectName("menubar")
        self.menuMain = QtWidgets.QMenu(self.menubar)
        self.menuMain.setObjectName("menuMain")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionQuit.setShortcut('Ctrl+Q')
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionAuthor = QtWidgets.QAction(MainWindow)
        self.actionAuthor.setObjectName("actionAuthor")
        self.menuMain.addAction(self.actionOpen)
        self.menuMain.addAction(self.actionQuit)
        self.menuTools.addAction(self.actionSettings)
        self.menuAbout.addSeparator()
        self.menuAbout.addAction(self.actionHelp)
        self.menuAbout.addAction(self.actionAuthor)
        self.menubar.addAction(self.menuMain.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def retranslateUi(self, TableWindow):
        _translate = QtCore.QCoreApplication.translate
        TableWindow.setWindowTitle(_translate("TableWindow", "QY-Integrating sphere"))

        self.menuMain.setTitle(_translate("TableWindow", "Main"))
        self.menuTools.setTitle(_translate("TableWindow", "Tools"))
        self.menuAbout.setTitle(_translate("TableWindow", "About"))
        self.actionOpen.setText(_translate("TableWindow", "Open"))
        self.actionQuit.setText(_translate("TableWindow", "Quit"))
        self.actionSettings.setText(_translate("TableWindow", "Settings"))
        self.actionHelp.setText(_translate("TableWindow", "Help"))
        self.actionAuthor.setText(_translate("TableWindow", "Author"))
