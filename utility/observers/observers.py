from abc import ABCMeta, abstractmethod


class MainObserver(metaclass=ABCMeta):
    """
    Abstract superclass for observers
    """
    @abstractmethod
    def loading(self):
        pass


class TableObserver(metaclass=ABCMeta):
    """
    Abstract superclass for observers
    """
    @abstractmethod
    def model_is_changed(self):
        pass
    
    @abstractmethod
    def table_updated(self, column):
        pass

    @abstractmethod
    def QY_is_changed(self):
        pass

    @abstractmethod
    def datastatus_is_changed(self):
        pass
