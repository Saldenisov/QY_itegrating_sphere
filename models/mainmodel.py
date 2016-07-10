'''
Created on 7 juin 2016

@author: saldenisov
'''
from collections import OrderedDict

import logging
module_logger = logging.getLogger(__name__)


class MainModel:
    """
    Class MainModel is upper level data model
    """

    def __init__(self, app_folder, developing=False):
        self.logger = logging.getLogger("MAIN." + __name__)
        self.app_folder = app_folder
        self.observers = []
        self.tables = OrderedDict()
        self.developing = developing
        self.normalfiles = 1
        self.emptyfiles = 1

    def add_table(self, table, name):
        self.tables[name] = table

    def delete_table(self, tablename):
        self.tables[tablename].view.close()
        del self.tables[tablename]

    def remove_tables(self):
        for key in self.tables.keys():
            self.tables[key].view.close()
            del self.tables[key]

    def add_observer(self, inObserver):
        self.observers.append(inObserver)

    def remove_observer(self, inObserver):
        self.observers.remove(inObserver)

    def loading(self):
        self.notify_observers()

    def notify_observers(self):
        for x in self.observers:
            x.loading()
