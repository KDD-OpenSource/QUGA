"""
This file implements the 'latentSpaceSMTPlot' class, which is a result that plots one advers. attack in parallel coordinates. I.e. it gets the solution from an smt-solver and visualizes them next to each other.
"""
from .resultSMT import resultSMT
from ..utils.myUtils import solutionsToPoints
import matplotlib.pyplot as plt
import time
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import os
from sklearn.metrics.pairwise import euclidean_distances
# from ..utils.myUtils import saveSmtSolutions


class latentSpaceSMTPlot(resultSMT):
    def __init__(self, name='latentSpaceSMTPlot', accuracy=0.1):
        super(latentSpaceSMTPlot, self).__init__(name)
        self.result = None
        self.smtSolutions = None
        self.accuracy = accuracy

    def calcResult(self, algorithm, trainDataset, smt):
        if 'adversAttack' in smt.abstractConstr:
            smt.addAEConstr(algorithm)
            # maxAdversAttack = smt.getMaxAdversAttack(startValue = smt.abstractConstr['adversAttack']['severity'], accuracy = self.accuracy)
            maxAdversAttack = smt.getMaxAdversAttack(
                startValue=smt.abstractConstr['adversAttack']['severity'],
                accuracy=self.accuracy,
                algorithm=algorithm,
                trainDataset=trainDataset)
            self.result = maxAdversAttack['severity']
            self.smtSolutions = maxAdversAttack['smtModel']
            trainLatentPoints = self.getTrainLatentPoints(
                trainDataset, algorithm)
            maxAdversLatentPoint = self.getMaxAdversLatentPoint(algorithm)
            fig = self.getResultFig(trainLatentPoints, maxAdversLatentPoint)
            self.result = fig

    def getTrainLatentPoints(self, trainDataset, algorithm):
        if trainDataset.tsFlg:
            trainDataset.timeseriesToPoints(algorithm.architecture[0])
            trainLatentPoints = algorithm.getLatentSpace(trainDataset.data)
            trainDataset.pointsToTimeseries()
        else:
            trainLatentPoints = algorithm.getLatentSpace(trainDataset)
        return trainLatentPoints

    def getMaxAdversLatentPoint(self, algorithm):
        maxAdversAttackPoint = solutionsToPoints(self.smtSolutions, ['x_0'])
        maxAdversAttackPointDF = pd.DataFrame(maxAdversAttackPoint[0])
        return algorithm.getLatentSpace(maxAdversAttackPointDF)

    def getResultFig(self, trainLatentPoints, maxAdversLatentPoint):
        fig = plt.figure(figsize=(30, 20))
        ax = fig.add_subplot(1, 1, 1)
        for index in np.random.choice(trainLatentPoints.index, 30):
            trainLatentPoints.iloc[index].plot(color='blue')
        for index in maxAdversLatentPoint.index:
            maxAdversLatentPoint.iloc[index].plot(color='red')

        minDistToAdversLatent = euclidean_distances(
            trainLatentPoints, maxAdversLatentPoint).min()
        distInTrainLatentPoints = euclidean_distances(
            trainLatentPoints, trainLatentPoints)
        distInTrainLatentPoints[distInTrainLatentPoints == 0] = 10
        distInTrainLatentPointsMinRows = distInTrainLatentPoints.min(axis=0)
        maxMinDistInTrainLatentPoints = distInTrainLatentPointsMinRows.max()
        if maxMinDistInTrainLatentPoints != 0:
            distRatio = minDistToAdversLatent / maxMinDistInTrainLatentPoints

        fig.suptitle(
            'The minimum distance of any Datapoint to the maxAdversLatentPoint is {}. The max-min distance within the trainDatasetLatentPoints is {}. Their ratio is {}'.format(
                minDistToAdversLatent,
                maxMinDistInTrainLatentPoints,
                distRatio))
        return fig

    def storeSMTResult(self, tmpFolderSmt):
        if self.result is not None:
            self.saveSmtSolutions(tmpFolderSmt)
            cwd = os.getcwd()
            os.chdir(tmpFolderSmt)
            plt.figure(self.result.number)
            # plt.savefig(os.getcwd()+'/'+str(self.name))
            plt.savefig(os.path.join(os.getcwd(), str(self.name)))
            plt.close('all')
            os.chdir(cwd)
