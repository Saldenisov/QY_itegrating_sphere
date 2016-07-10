'''
Created on 8 juin 2016

@author: saldenisov
'''
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget,
                             QSplitter,
                             QGroupBox,
                             QPushButton,
                             QVBoxLayout,
                             QHBoxLayout,
                             QGridLayout,
                             QTableWidget,
                             QLineEdit,
                             QCheckBox)
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt

class MyTable(QTableWidget):
    keyPressed = QtCore.pyqtSignal(str)

    def keyPressEvent(self, event):
        super(MyTable, self).keyPressEvent(event)
        if event.key() == Qt.Key_V and event.modifiers() == Qt.ControlModifier:
            self.keyPressed.emit('Ctrl-V')
        if event.key() == Qt.Key_C and event.modifiers() == Qt.ControlModifier:
            self.keyPressed.emit('Ctrl-C')
        if event.key() == Qt.Key_D and event.modifiers() == Qt.ControlModifier:
            self.keyPressed.emit('Ctrl-D')
        if event.key() == Qt.Key_Delete:
            self.keyPressed.emit('Delete')
        else:
            self.keyPressed.emit('Any')


class Ui_TableWindow(object):
    def setupUi(self, TableWindow, name, headers):
        TableWindow.setObjectName("TableWindow: " + name)
        TableWindow.resize(1240, 800)
        self.main_widget = QWidget(TableWindow)
        self.main_widget.setObjectName("table_window")

        layout_main = QGridLayout(self.main_widget)
        layout_table = QVBoxLayout()
        layout_controls = QHBoxLayout()

        self.table = MyTable(self.main_widget)
        self.table.setRowCount(550)
        self.table.setColumnCount(len(headers))
        HeaderLabels = headers
        self.table.setHorizontalHeaderLabels(HeaderLabels)
        [self.table.setColumnWidth(i,90) for i in range(10)]


        groupbox_table = QGroupBox(self.main_widget)
        groupbox_table.setLayout(layout_table)
        layout_table.addWidget(self.table)

        self.button_load = QPushButton('Load')
        self.button_calc = QPushButton('Calculate')
        self.button_graph = QPushButton('Graph')
        self.check_correct = QCheckBox('Correct')
        self.check_background = QCheckBox('Background')
        self.button_reabs = QPushButton('Reabsorption')
        self.input_reab= QLineEdit()
        self.input_reab.setFixedWidth(40)
        self.input_reab.setText('1.0')
        self.button_filter_calc = QPushButton('Filter calculate')
        self.input_filter = QLineEdit()
        self.input_filter.setFixedWidth(60)
        self.input_filter.setText('0.00538')
        self.output_QY = QLineEdit()
        self.output_QY.setFixedWidth(60)

        status = False
        self.button_calc.setEnabled(status)
        self.button_graph.setEnabled(status)
        self.button_filter_calc.setEnabled(status)
        self.button_reabs.setEnabled(status)
        self.input_filter.setEnabled(status)
        self.input_reab.setEnabled(status)

        groubox_controls = QGroupBox(self.main_widget)
        groubox_controls.setLayout(layout_controls)
        layout_controls.addWidget(self.button_load)
        layout_controls.addWidget(self.button_calc)
        layout_controls.addWidget(self.check_correct)
        layout_controls.addWidget(self.check_background)
        layout_controls.addWidget(self.button_graph)
        layout_controls.addWidget(self.button_reabs)
        layout_controls.addWidget(self.input_reab)
        layout_controls.addWidget(self.button_filter_calc)
        layout_controls.addWidget(self.input_filter)
        layout_controls.addWidget(self.output_QY)

        layout_main.addWidget(groupbox_table)
        layout_main.addWidget(groubox_controls)

        self.main_widget.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.main_widget.setWindowTitle("TableWindow")

        self.main_widget.setFocus()
        TableWindow.setCentralWidget(self.main_widget)

        self.retranslateUi(TableWindow, name)

    def retranslateUi(self, TableWindow, name):
        _translate = QtCore.QCoreApplication.translate
        TableWindow.setWindowTitle(_translate("TableWindow", "Table (raw data): " + name))
