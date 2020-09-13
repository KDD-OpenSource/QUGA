"""
this class calculates the average mean L2 error between input and output of
autoencoders over all elements of the given testDataset
"""
import numpy as np
import pandas as pd
from .resultAE import resultAE
from ..utils import myUtils
from itertools import product
import os


class avgError(resultAE):
    def __init__(self, name='avgError'):
        super(avgError, self).__init__(name)
        self.algorithm = None
        self.data = None
        self.name = 'avgError'
        self.avgError = None
        self.result = None

    def calcResult(self, algorithm, trainDataset, testDataset):
        self.algorithm = algorithm
        self.testDataset = testDataset
        self.orig = np.array(self.testDataset.data)
        if self.testDataset.tsFlg:
            testDataset.timeseriesToPoints(
                windowLength=algorithm.architecture[0])
            self.recon = np.array(algorithm.predict(self.testDataset.data))
            self.avgError = pd.DataFrame(
                [np.square(np.subtract(self.recon, self.testDataset.data)).mean(axis=1).mean()])
            testDataset.pointsToTimeseries()
        else:
            self.recon = np.array(algorithm.predict(self.testDataset.data))
            self.avgError = pd.DataFrame(
                [np.square(np.subtract(self.recon, self.testDataset.data)).mean(axis=1).mean()])
        self.result = self.avgError

    def storeAEResult(
            self,
            folder,
            trainDataset,
            testDataset,
            algorithm,
            testName):
        cwd = os.getcwd()
        os.chdir(folder)
        self.result.to_csv(os.path.join(os.getcwd(), str(
            self.name) + '_' + str(self.testDataset.name) + '.csv'), header=False, index=False)
        os.chdir(cwd)
