import json
import tikzplotlib as tikz
from .resultSMT import resultSMT
from .maxAdversAttack import maxAdversAttack
from .maxErrorEst import maxErrorEst
import matplotlib.pyplot as plt
import os


class timeMaxErrorPlot(resultSMT):
    """docstring for timeMaxErrorPlot"""

    def __init__(self, times_s, errFct, accuracy=0.025, name='timeMaxErrorPlot'):
        super(timeMaxErrorPlot, self).__init__(name)
        self.times_s = times_s
        self.accuracy = accuracy
        self.maxErrorEst = None
        self.maxAdversAttack = None
        self.errFct = errFct

    def calcResult(self, algorithm, trainDataset, smt):
        self.maxAdversAttack = maxAdversAttack(accuracy=self.accuracy)
        self.maxErrorEst = maxErrorEst(self.times_s, self.errFct)
        self.maxAdversAttack.calcResult(algorithm, trainDataset, smt)
        self.maxErrorEst.calcResult(algorithm, trainDataset, smt)
        fig, ax = plt.subplots(1, 1, figsize=(20, 10))
        ax.plot(
            self.maxAdversAttack.calcTime,
            self.maxAdversAttack.result,
            color='red',
            marker='+'
            )
        maxErrorEstTmpTimes = [
            elem['time']
            for elem in self.maxErrorEst.result
            ]
        maxErrorEstTmpResult = [
            elem['maxErrorEst']
            for elem in self.maxErrorEst.result
            ]
        ax.plot(
            maxErrorEstTmpTimes,
            maxErrorEstTmpResult,
            color='red',
            marker='.'
            )
        self.result = fig

    def storeSMTResult(self, tmpFolderSmt):
        # we create a folder with the current timestamp. In this folder all the
        # plots should be stored as files
        cwd = os.getcwd()
        os.chdir(tmpFolderSmt)
        filename = str(self.maxErrorEst.name) + '_' + \
            str(self.maxErrorEst.boundingBox)[:20] + '.txt'
        print(filename)
        with open(os.path.join(os.getcwd(), filename), 'w') as file:
            json.dump(self.maxErrorEst.result, file, indent=0)
        plt.figure(self.result.number)
        plt.savefig(os.path.join(os.getcwd(), str(self.name)))
        tikz.save(os.path.join(os.getcwd(), str(self.name) + '.tex'))
        plt.close('all')
        os.chdir(cwd)
