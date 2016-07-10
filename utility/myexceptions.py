'''
Created on 9 juin 2016

@author: saldenisov
'''

class MyException(Exception):
    pass


class WrongArraySizes(MyException):
    def __init__(self):
        MyException.__init__(self, "Wrong array sizes were passed")


class IsnanInput(TypeError):
    def __init__(self):
        MyException.__init__(self, "clipboard contains non digits")

class WrongSelection(MyException):
    def __init__(self, text):
        MyException.__init__(self, text)
