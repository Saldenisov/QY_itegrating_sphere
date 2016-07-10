'''
Created on 7 juin 2016

@author: saldenisov
'''

from views import MainView
from models import QYModel
from utility import MyException
from controllers.tablecontroller import TableController
from PyQt5.QtWidgets import (QMessageBox,
                             QApplication,
                             QFileDialog)


import logging
module_logger = logging.getLogger(__name__)


class MainController():
    """
    Class MainController is a controller
    which coordinates work between
    MainView and MainModel
    """

    def __init__(self, in_model):
        """
        """
        self.logger = logging.getLogger("MAIN." + __name__)
        self.model = in_model

        self.view = MainView(self, in_model=self.model)
        self.view.show()

        if self.model.developing:
            self.open_clicked()

    def help_clicked(self):
        QMessageBox.information(self.view,
                                'Help',
                                """For any help contact:\n
                                Dr. Sergey A. Denisov\n
                                saldenisov@gmail.com""")

    def author_clicked(self):
        QMessageBox.information(self.view,
                                'Author information',
                                """Author: Dr. Sergey A. Denisov\n
                                e-mail: saldenisov@gmail.com\n
                                telephone: +33625252159""")

    def quit_clicked(self, event):
        if not self.model.developing:
            reply = QMessageBox.question(self.view, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.logger.info('Closing')
                self.model.kill_observes()
                QApplication.quit()
            else:
                event.ignore()
        else:
            self.logger.info('Closing')
            self.model.remove_tables()
            QApplication.quit()

    def open_clicked(self):
        try:
            if self.model.developing:
                file_name = 'C:\\Users\\saldenisov\\Dropbox\\Python\\QY\\test-excel.xlsx'
            else:
                file_name = QFileDialog.getOpenFileName(self.view,
                                                   'Open file', '')[0]
                if not file_name:
                    raise MyException('FileNotFoundError')
                self.logger.info('Loading file:' + str(file_name))

            modeltable = QYModel(app_folder=self.model.app_folder,
                                 developing=self.model.developing)

            tablecontroller = TableController(in_model=modeltable,
                                              mainmodel=self.model,
                                              name=file_name)
            tablecontroller.model.set_data(file_name)
            datastatus = tablecontroller.model.check_datastatus()
            tablecontroller.model.set_datastatus(datastatus)
            self.model.add_table(table=tablecontroller, name=file_name)
        except (MyException, FileNotFoundError) as e:
            self.empty_clicked()
            self.logger.info('Could not load file')
            self.logger.error(str(e))




    def empty_clicked(self):
        try:
            modeltable = QYModel(app_folder=self.model.app_folder,
                                 developing=self.model.developing)
            name = 'Empty' + str(self.model.emptyfiles)
            self.model.emptyfiles += 1
            tablecontroller = TableController(in_model=modeltable,
                                              mainmodel=self.model,
                                              name=name)
            self.model.add_table(table=tablecontroller, name=name)
        except MyException as e:
            self.logger.info('Could not open empty table')
            self.logger.error(str(e))
