'''
Created on 7 juin 2016

@author: saldenisov
'''
from PyQt5.Qt import QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem

from utility import TableObserver
from utility import Meta
from views import Ui_TableWindow


class TableView(QMainWindow, TableObserver, metaclass=Meta):
    """
    """

    def __init__(self, in_controller,
                 in_model,
                 in_name,
                 headers,
                 parent=None):
        """

        """
        super(QMainWindow, self).__init__(parent)
        self.controller = in_controller
        self.model = in_model

        self.ui = Ui_TableWindow()
        self.ui.setupUi(self, in_name, headers)

        self.model.add_observer(self)

        self.ui.button_load.clicked.connect(self.controller.load_clicked)
        self.ui.button_calc.clicked.connect(self.controller.calc_clicked)
        self.ui.button_graph.clicked.connect(self.controller.graph_clicked)
        self.ui.button_reabs.clicked.connect(self.controller.reabsorption_clicked)
        self.ui.table.keyPressed.connect(self.controller.key_pressed)
        self.ui.table.cellDoubleClicked.connect(self.controller.cell_doublecliked)
        self.ui.table.cellClicked.connect(self.controller.cell_clicked)
        self.ui.table.cellChanged.connect(self.controller.item_changed)

    def model_is_changed(self):
        self.ui.table.setRowCount(0)
        self.ui.table.setRowCount(550)
        data = self.model.data
        headers = self.controller.model.HeaderLabels
        for item in data.keys():
            column = headers.index(item)
            row = 0
            for i in data[item]:
                self.ui.table.setItem(row, column, QTableWidgetItem(str(i)))
                row += 1

    def QY_is_changed(self):
        self.ui.output_QY.setText("%.3f" % self.model.QY_corrected)

    def table_updated(self, column):
        column_s = self.model.HeaderLabels[column]
        data = self.model.data[column_s]
        row = 0
        for i in data:
            self.ui.table.setItem(row, column, QTableWidgetItem(str(i)))
            row += 1

    def datastatus_is_changed(self):
        if self.model.datastatus == 'full' or self.model.datastatus == 'partlyfull':
            self.ui.button_calc.setEnabled(True)
            self.ui.button_graph.setEnabled(True)
            #self.ui.button_filter_calc.setEnabled(True)
            self.ui.input_filter.setEnabled(True)
            self.ui.input_reab.setEnabled(True)
            if not self.model.datastatus == 'partlyfull':
                self.ui.button_reabs.setEnabled(True)

    def closeEvent(self, event):
        self.controller.quit_clicked(event)
