"""
This file implements the 'latentSpaceSMTPlot3D' class, which is a result that plots one advers. attack in parallel coordinates. I.e. it gets the solution from an smt-solver and visualizes them next to each other.
"""
from .resultSMT import resultSMT
from ..utils.myUtils import solutionsToPoints
import matplotlib.pyplot as plt
import time
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import os
from sklearn.metrics.pairwise import euclidean_distances
# from ..utils.myUtils import saveSmtSolutions


class latentSpaceSMTPlot3D(resultSMT):
    def __init__(self, name='latentSpaceSMTPlot3D', accuracy=0.1):
        super(latentSpaceSMTPlot3D, self).__init__(name)
        self.result = None
        self.smtSolutions = None
        self.accuracy = accuracy

    def calcResult(self, algorithm, trainDataset, smt):
        if 'adversAttack' in smt.abstractConstr and algorithm.getLatentSpaceDim() == 3:
            smt.addAEConstr(algorithm)
            maxAdversAttack = smt.getMaxAdversAttack(
                startValue=smt.abstractConstr['adversAttack']['severity'],
                accuracy=self.accuracy,
                algorithm=algorithm,
                trainDataset=trainDataset)
            # maxAdversAttack = smt.getMaxAdversAttack(startValue = smt.abstractConstr['adversAttack']['severity'], accuracy = self.accuracy)
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
            trainLatentPoints = algorithm.getLatentSpace(trainDataset.data)
        return trainLatentPoints

    def getMaxAdversLatentPoint(self, algorithm):
        maxAdversAttackPoint = solutionsToPoints(self.smtSolutions, ['x_0'])
        maxAdversAttackPointDF = pd.DataFrame(maxAdversAttackPoint[0])
        return algorithm.getLatentSpace(maxAdversAttackPointDF)

    def getResultFig(self, trainLatentPoints, maxAdversLatentPoint):
        fig = plt.figure(figsize=(30, 20))
        ax = fig.add_subplot(1, 1, 1, projection='3d')
        ax.scatter(trainLatentPoints.iloc[:,
                                          0],
                   trainLatentPoints.iloc[:,
                                          1],
                   trainLatentPoints.iloc[:,
                                          2],
                   color='blue')
        ax.scatter(maxAdversLatentPoint.iloc[:,
                                             0],
                   maxAdversLatentPoint.iloc[:,
                                             1],
                   maxAdversLatentPoint.iloc[:,
                                             2],
                   color='red')
        minDistancesToAdversLatent = euclidean_distances(
            trainLatentPoints, maxAdversLatentPoint).min()
        fig.suptitle('The minimum distance of any Datapoint to the maxAdversLatentPoint is {}'.format(
            minDistancesToAdversLatent))
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
