"""
This file implements the 'maxSumAdversAttack' class, which is a result that plots one advers. attack in parallel coordinates. I.e. it gets the solution from an smt-solver and visualizes them next to each other.
"""
from .resultSMT import resultSMT
from ..utils.myUtils import solutionsToPoints
import matplotlib.pyplot as plt
import time
import os
from sklearn.metrics.pairwise import euclidean_distances
import pandas as pd
import math
import numpy as np
# from ..utils.myUtils import saveSmtSolutions


class maxSumAdversAttack(resultSMT):
    def __init__(self, name='maxSumAdversAttack', accuracy=0.1):
        super(maxSumAdversAttack, self).__init__(name)
        self.result = None
        self.smtSolutions = None
        self.accuracy = accuracy
        self.AEError = None

    def calcResult(self, algorithm, trainDataset, smt):
        if 'sumAdversAttack' in smt.abstractConstr:
            smt.addAEConstr(algorithm)
            maxSumAdversAttack = smt.getMaxSumAdversAttack(
                startValue=smt.abstractConstr['sumAdversAttack']['severity'],
                accuracy=self.accuracy,
                algorithm=algorithm,
                trainDataset=trainDataset)
            self.result = maxSumAdversAttack['severity']
            self.smtSolutions = maxSumAdversAttack['smtModel']
            points = solutionsToPoints(self.smtSolutions, ['x_0', 'x_2'])
            pointsDF = pd.DataFrame(points[0][0]).transpose()
            autoencoderSolution = algorithm.getAEResults(pointsDF)[1]
            # smtSolutionsError = euclidean_distances([points[0][0]],[points[0][1]])
            pointsDFValues = pointsDF.values
            autoencoderSolutionValues = autoencoderSolution.values
            self.AEError = np.mean(
                np.square(
                    np.subtract(
                        pointsDFValues,
                        autoencoderSolutionValues)))

    def storeSMTResult(self, tmpFolderSmt):
        self.saveSmtSolutions(tmpFolderSmt)
        cwd = os.getcwd()
        os.chdir(tmpFolderSmt)
        file = './maxAdversAttackSeverity.csv'
        with open(file, 'w') as file:
            file.write(
                'The severity of this solution is: {}'.format(
                    self.result))
            file.write('\n')
            file.write('The MSE on this point is: {}'.format(self.AEError))
        os.chdir(cwd)
