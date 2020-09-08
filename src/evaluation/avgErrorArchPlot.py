import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .resultAE import resultAE
from .avgError import avgError
from ..utils import myUtils
from itertools import product


class avgErrorAEParamPlot(resultAE):
    """This class plots the reconstructed vs the original plot"""

    def __init__(self, AEParam, name='avgErrorAEParamPlot'):
        super(avgErrorAEParamPlot, self).__init__(name)
        self.name = 'avgErrorAEParamPlot'
        self.collResults = pd.DataFrame(
            columns=[
                'algorithm',
                'trainDataset',
                'testDataset',
                'avgError'])
        self.maxError = None
        self.result = None
        self.figures = None
        self.AEParam = AEParam

    def calcResult(self, algorithm, trainDataset, testDataset):
        avgErrorTmp = avgError()
        avgErrorTmp.calcResult(algorithm, trainDataset, testDataset)
        avgErrorNumber = avgErrorTmp.result.values.flatten()
        resultToAppend = pd.DataFrame(
            columns=[
                'algorithm',
                'trainDataset',
                'testDataset',
                'avgError'],
            data=[
                [
                    algorithm,
                    trainDataset,
                    testDataset,
                    avgErrorNumber]])
        self.collResults = self.collResults.append(resultToAppend)

    def storeAEResult(
            self,
            folder,
            trainDataset,
            testDataset,
            algorithm,
            testName):
        pass

    def calcCollectedAEResults(self):
        self.figures = []
        for testDataset, trainDataset in product(
                self.collResults['testDataset'].unique(), self.collResults['trainDataset'].unique()):
            maxError = self.calcMaxError()
            self.figures.append(
                {
                    'figure': self.calcCollectedAEResult(
                        testDataset,
                        trainDataset,
                        maxError),
                    'trainDataset': trainDataset,
                    'testDataset': testDataset})

    def calcCollectedAEResult(self, testDataset, trainDataset, maxError):
        tmpDataFrame = self.collResults[(self.collResults['testDataset'] == testDataset) & (
            self.collResults['trainDataset'] == trainDataset)]
        AEParams = sorted([x[self.AEParam] for x in tmpDataFrame['algorithm']])
        y_pos = np.arange(len(AEParams))
        avgErrors = tmpDataFrame['avgError'].values.tolist()
        fig = plt.figure(figsize=(20, 10))
        plt.plot(y_pos, avgErrors, marker='.')
        axes = plt.gca()
        axes.set_ylim([0, 1.1 * maxError])
        plt.xticks(y_pos, AEParams, rotation=90)
        return fig

    def storeCollectedAEResults(self, runFolder):
        for figureDict in self.figures:
            self.storeCollectedAEResult(runFolder, figureDict)

    def storeCollectedAEResult(self, folder, figureDict):
        plt.figure(figureDict['figure'].number)
        trainDatasetName = figureDict['trainDataset'].name
        testDatasetName = figureDict['testDataset'].name
        # figureDict['figure'].suptitle(f'Train-Dataset: {trainDatasetName}, \n
        # Test-Dataset: {testDatasetName}')
        plt.savefig(folder +
                    '//' +
                    'avgErrors_' +
                    str(figureDict['trainDataset'].obj_id)[:4] +
                    '_' +
                    str(figureDict['testDataset'].obj_id)[:4] +
                    '.png')
        # plt.close('all')

    def calcMaxError(self):
        print('in avgError: {}'.format(self.collResults))
        print('in avgError: {}'.format(self.collResults['avgError']))
        maxError = self.collResults['avgError'].max()
        return maxError

    # I want the plot function to plot over all autoencoders with different
    # architectures (that is we group by everything except by architecture)
