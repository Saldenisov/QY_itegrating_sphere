'''
Created on 28 août 2016

@author: saldenisov
'''

import sqlite3
import sys
import json
import numpy as np

import logging
module_logger = logging.getLogger(__name__)


class DB_helper:
    '''
    classdocs
    '''

    def __init__(self, db_path):
        self.logger = logging.getLogger("MAIN." + __name__)

        try:
            db = sqlite3.connect(db_path)

            self.cursor = db.cursor()

            self.logger.info('Successfully connected to DB')

        except (sqlite3.Error) as e:
            self.logger.error(e)
            raise e