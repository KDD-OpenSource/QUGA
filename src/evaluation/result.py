import abc
'''I think this class really makes no sense. What do I encapsulate here for? What are shared properties of 'results' that are worth sharing? (Not existing currently) '''


"""
NOTE THAT IF YOU COMPARE TEST AND TRAIN DATA THEY NEED TO HAVE THE SAME STRUCTURE
Note that if only one dataset is needed for the plot we use the test_data per default
"""


class result(metaclass=abc.ABCMeta):
    def __init__(self, name):
        self.name = name
        pass

    # the method 'get_result' has the purpose to return the result obtained to
    # the 'execute_experiment' function and thus be able to save it
    @abc.abstractmethod
    def calcResult():
        pass

    def getCollResults(self):
        if 'collResults' in self.__dir__():
            return self.collResults
        else:
            return None
