"""
This file implements the 'maxAdversAttack' class, which is a result that gives
an example point with the maximum adversarial attack (one possible solution
from the SMT framework). Moreover writes the solution's calculation Time, its
L2 error and the theoretical maximum L2 error obtained by applying the largest
Linfty distance in every dimension
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


class maxAdversAttack(resultSMT):
    def __init__(self, name='maxAdversAttack', accuracy=0.1):
        super(maxAdversAttack, self).__init__(name)
        self.result = None
        self.calcTime = None
        self.smtSolutions = None
        self.accuracy = accuracy
        self.AEError = None
        self.theoMaxError = None

    def calcResult(self, algorithm, trainDataset, smt):
        if 'adversAttack' in smt.abstractConstr:
            smt.readAE(algorithm)
            smt.addCustomConstr(exceptions=['adversAttack'])
            maxAdversAttack = smt.getMaxAdversAttack(
                startValue=smt.abstractConstr['adversAttack']['severity'],
                accuracy=self.accuracy,
                algorithm=algorithm,
                trainDataset=trainDataset)
            self.result = maxAdversAttack['severity']
            self.calcTime = maxAdversAttack['calcTime']
            self.smtSolutions = maxAdversAttack['smtModel']
            # Todo: extract max variable to account for different architectures
            if len(self.smtSolutions) != 0:
                allX = [x for x in self.smtSolutions[0]
                        ['model'] if str(x)[0] == 'x']
                largestLayer = max([int(str(x)[2]) for x in allX])
                lastLayerVars = [x for x in self.smtSolutions[0]
                                 ['model'] if str(x)[2] == str(largestLayer)]
                solutionPoints = solutionsToPoints(
                    self.smtSolutions, [
                        'x_0', 'x' + '_' + str(largestLayer)])
                pointsDF = pd.DataFrame(solutionPoints[0][0]).transpose()
                autoencoderSolution = algorithm.getAEResults(pointsDF)[1]
                pointsDFValues = pointsDF.values
                autoencoderSolutionValues = autoencoderSolution.values
                self.AEError = np.mean(
                    np.square(
                        np.subtract(
                            pointsDFValues,
                            autoencoderSolutionValues)))
                self.theoMaxError = np.array(
                    [self.result * self.result for x in range(pointsDF.shape[1])]).flatten().mean()
            else:
                raise Exception(
                    'Cannot return maxAdversAttack because there is no solution')

    def storeSMTResult(self, tmpFolderSmt):
        if len(self.smtSolutions) !=0:
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
                file.write('\n')
                file.write(
                    'The theoretical maximum Error for the severity is: {}'.format(
                        self.theoMaxError))
                file.write('\n')
                file.write('The calculation Time is: {}'.format(self.calcTime))
            os.chdir(cwd)
