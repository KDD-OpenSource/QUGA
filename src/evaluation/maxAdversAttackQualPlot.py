"""
This file implements the 'maxAdversAttackQualPlot' class, which is a result
that plots one advers. attack in parallel coordinates. I.e. it gets the
solution from an smt-solver and visualizes them next to each other.
"""

from .resultSMT import resultSMT
from ..utils.myUtils import solutionsToPoints
import matplotlib.pyplot as plt
import os
import tikzplotlib as tikz


class maxAdversAttackQualPlot(resultSMT):
    def __init__(self, accuracy, name='maxAdversAttackQualPlot'):
        super(maxAdversAttackQualPlot, self).__init__(name)
        self.result = None
        self.smtSolutions = None
        self.accuracy = accuracy

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
            self.smtSolutions = maxAdversAttack['smtModel']
            if len(self.smtSolutions) != 0:
                # extract input and output to the autoencoder of the maximum
                # adversarial Attack
                # smt_solutions are to be in the same format as trainData
                allX = [x for x in self.smtSolutions[0]
                        ['model'] if str(x)[0] == 'x']
                largestLayer = max([int(str(x)[2]) for x in allX])
                lastLayerVars = [x for x in self.smtSolutions[0]
                                 ['model'] if str(x)[2] == str(largestLayer)]
                solutionPoints = solutionsToPoints(
                    self.smtSolutions, [
                        'x_0', 'x' + '_' + str(largestLayer)])
                fig, ax = plt.subplots(
                    nrows=1, ncols=len(solutionPoints), squeeze=False)
                for column in range(len(solutionPoints)):
                    ax[0, column].plot(solutionPoints[column][0], color='blue')
                    ax[0, column].title.set_text(
                        'Input of AE: Blue, Output: red')
                    ax[0, column].plot(solutionPoints[column][1], color='red')
                self.result = fig

    def storeSMTResult(self, tmpFolderSmt):
        if self.result is not None:
            self.saveSmtSolutions(tmpFolderSmt)
            cwd = os.getcwd()
            os.chdir(tmpFolderSmt)
            plt.figure(self.result.number)
            plt.savefig(os.path.join(os.getcwd(), str(self.name)))
            tikz.save(os.path.join(os.getcwd(), str(self.name) + '.tex'))
            plt.close('all')
            os.chdir(cwd)
