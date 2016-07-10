'''
Created on 8 juin 2016

@author: saldenisov
'''

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import numpy as np

from views import TableView
from utility import MyException, WrongSelection

import logging
module_logger = logging.getLogger(__name__)


class TableController():
    """
    Class TableController is a controller
    which coordinates work between
    TableView and MainModel
    """

    def __init__(self, in_model, mainmodel, name):
        """
        """
        self.doubleclicked = False
        self.clicked = False
        self.keypressed = False
        self.name = name
        self.logger = logging.getLogger("MAIN." + __name__)
        self.model = in_model
        self.mainmodel = mainmodel
        self.graphnumber = 0

        self.view = TableView(self,
                              in_model=self.model,
                              in_name=name,
                              headers=self.model.HeaderLabels)
        self.view.show()

    def load_clicked(self):
        self.mainmodel.loading()
        self.mainmodel.delete_table(tablename=self.name)

    def calc_clicked(self):
        try:
            filter_ = float(self.view.ui.input_filter.text())
            reabsorption_ = float(self.view.ui.input_reab.text())
            check_correct_ = self.view.ui.check_correct.isChecked()
            check_background_ = self.view.ui.check_background.isChecked()
            self.model.calc_QY(filter=filter_,
                               reabsorption=reabsorption_,
                               check_correct=check_correct_,
                               check_background=check_background_)
        except (MyException, ValueError) as e:
            self.logger.info('problems with filter or reabsorption values')
            self.logger.error(str(e))

    def graph_clicked(self):
        ranges = self.view.ui.table.selectedRanges()
        if ranges:
            try:
                columns = []
                for range_ in ranges:
                    leftcolumn= range_.leftColumn()
                    rightcolumn= range_.rightColumn()
                    headers = self.model.HeaderLabels
                    columns.extend(headers[leftcolumn:rightcolumn+1])

                self.model.draw_graphs(columns)
            except:
                self.logger.error('Error in during graph building')

        else:
            self.logger.info('Nothing is selected for creating a graph')

    def cell_doublecliked(self):
        self.doubleclicked = True

    def cell_clicked(self):
        self.clicked = True

    def item_changed(self):
        """
        Function invokes when table item is changed
        """
        if (self.doubleclicked or self.clicked) and self.keypressed:
            self.doubleclicked = False
            self.clicked = False
            self.keypressed = False
            item = self.view.ui.table.selectedItems()[0]
            row = item.row()
            column = item.column()
            value = self.view.ui.table.currentItem().text()
            if not self.model.update_data(row, column, value):
                key = self.model.HeaderLabels[column]
                old_value = self.model.data[key][row]
                self.view.ui.table.setItem(row, column, QTableWidgetItem("%.3f" % old_value))

    def reabsorption_clicked(self):
        """
        Reabsorption button event handler function
        """
        ranges = self.view.ui.table.selectedRanges()
        self.logger.info('Reabsorption calculation started')
        if ranges:
            try:
                columns = []
                for range_ in ranges:
                    leftcolumn = range_.leftColumn()
                    rightcolumn = range_.rightColumn()
                    headers = self.model.HeaderLabels
                    columns.extend(headers[leftcolumn:rightcolumn+1])

                columns_mustbe = ['Xe', 'Ec', 'Ed']
                if len(columns) > 3 or len(columns) < 3 or not all(i in columns_mustbe for i in columns):
                    raise WrongSelection('Wrong selection for reabsorption calculation')
                else:
                    self.model.draw_reabsorption(columns, float(self.view.ui.input_reab.text()))
            except WrongSelection as e:
                self.logger.info('No reabsorption calculation could be accomplished')
                self.logger.error(str(e))

        else:
            self.logger.info('Nothing is selected for creating a graph')

    def filter_calculate_clicked(self):
        """
        Filter button event handler function
        """
        pass

    def key_pressed(self, event):
        """
        Table's key pressed event handler
        """
        if event == 'Any':
            self.keypressed = True
        if event == 'Ctrl-V':
            self.keypressed = False
            self.model.set_data_clipboard(self.view.ui.table.currentColumn())
        if event == 'Ctrl-C':
            self.keypressed = False
            indexes = self.view.ui.table.selectionModel().selectedColumns()
            columns = [index.column() for index in indexes]
            self.model.get_data_clipboard(columns)
        if event == 'Ctrl-D':
            self.keypressed = False
            self.model.delete_data()
        if event == 'Delete':
            indexes = self.view.ui.table.selectionModel().selectedColumns()
            columns = [index.column() for index in indexes]
            self.keypressed = False
            if columns:
                self.model.delete_data(columns)

    def quit_clicked(self, event):
        if not self.model.developing:
            reply = QMessageBox.question(self.view, 'Message',
                                         "Are you sure to quit?",
                                         QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
