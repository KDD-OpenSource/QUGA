"""
This class stores allows for storing AE results.
"""
from .result import result
import os
import matplotlib.pyplot as plt
import pandas as pd
import tikzplotlib as tikz

class resultAE(result):
    def __init__(self, name):
        self.name = name
        self.result = None
        pass

    def storeAEResult(
            self,
            folder,
            trainDataset,
            testDataset,
            algorithm,
            testName):
        cwd = os.getcwd()
        os.chdir(folder)
        if isinstance(self.result, plt.Figure):
            plt.savefig(os.path.join(os.getcwd(), str(self.name) + '.png'))
            tikz.save(
                os.path.join(
                    os.getcwd(), str(self.name) + '.tex'), encoding='utf-8')
            plt.close('all')
        elif isinstance(self.result, pd.DataFrame):
            self.result.to_csv(os.getcwd() + '/' +
                               str(self.name) + '.csv', header=False)
        else:
            print(
                "Your result is not in the appropriate format, hence it did not get saved")
        os.chdir(cwd)
