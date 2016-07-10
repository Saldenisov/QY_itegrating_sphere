'''
Created on 7 juin 2016

@author: saldenisov
'''
'''
Created on 7 oct. 2015

@author: saldenisov
'''

from configobj import ConfigObj
from validate import Validator


class Configuration(object):
    """
    Creates main configuration
    """

    def __init__(self, path='C:\\Users\\saldenisov\\Dropbox\\Python\\QY\\Settings\\'):

        __configspec = ConfigObj(path + 'configspec.ini', encoding='UTF8',
                                 list_values=False, _inspec=True)

        self.__config = ConfigObj(
            path + 'config_main.ini', configspec=__configspec)

        val = Validator()

        if self.config.validate(val) == False:
            raise ValueError(
                'Configuration file is corrupted. Check in settings config_main.ini and configspec.ini.')

    @property
    def config(self):
        return self.__config
