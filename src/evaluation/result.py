"""
this class ensures that calcResult is implemented
"""
import abc

class result(metaclass=abc.ABCMeta):
    def __init__(self, name):
        self.name = name
        pass

    @abc.abstractmethod
    def calcResult():
        pass
