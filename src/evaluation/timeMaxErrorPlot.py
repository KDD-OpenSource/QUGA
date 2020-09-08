import pandas as pd
import json
import tikzplotlib as tikz
from .resultSMT import resultSMT
from .maxAdversAttack import maxAdversAttack
from .maxLInftyErrorEst import maxLInftyErrorEst
from .maxErrorEst import maxErrorEst
import matplotlib.pyplot as plt
import os


class timeMaxErrorPlot(resultSMT):
    """docstring for timeMaxErrorPlot"""

    def __init__(self, times_s, accuracy=0.025, name='timeMaxErrorPlot'):
        super(timeMaxErrorPlot, self).__init__(name)
        self.times_s = times_s
        self.accuracy = accuracy
        self.maxLInftyErrorEst = None
        self.maxErrorEst = None
        self.maxAdversAttack = None

    def calcResult(self, algorithm, trainDataset, smt):
        self.maxAdversAttack = maxAdversAttack(accuracy=self.accuracy)
        # self.maxLInftyErrorEst = maxLInftyErrorEst(self.times_s)
        self.maxErrorEst = maxErrorEst(self.times_s)
        self.maxAdversAttack.calcResult(algorithm, trainDataset, smt)
        # self.maxLInftyErrorEst.calcResult(algorithm, trainDataset, smt)
        self.maxErrorEst.calcResult(algorithm, trainDataset, smt)

        fig, ax = plt.subplots(1, 1, figsize=(20, 10))

        # maxAdversLInftyDataFrame = pd.DataFrame(data=[[self.maxAdversAttack.calcTime,self.maxAdversAttack.result]], columns = ['calcTime','Result'])
        # maxAdversLInftyDataFrame.plot(x = 'calcTime', y = 'Result', ax = ax, style = 'rx')

        # maxAdversAEErrorDataFrame = pd.DataFrame(data=[[self.maxAdversAttack.calcTime,self.maxAdversAttack.AEError]], columns = ['calcTime','Result'])
        # maxAdversAEErrorDataFrame.plot(x = 'calcTime', y = 'Result', ax = ax, style = 'bx')

        ax.plot(
            self.maxAdversAttack.calcTime,
            self.maxAdversAttack.result,
            color='red',
            marker='+')
        ax.plot(
            self.maxAdversAttack.calcTime,
            self.maxAdversAttack.AEError,
            color='blue',
            marker='*')

        maxErrorEstTmpTimes = [elem['time']
                               for elem in self.maxErrorEst.result]
        maxErrorEstTmpResult = [elem['maxErrorEst']
                                for elem in self.maxErrorEst.result]
        maxLInftyErrorEstTmpResult = [
            elem['maxLInftyErrorEst'] for elem in self.maxErrorEst.result]
        # maxLInftyErrorEstTmpTimes = [elem['time'] for elem in self.maxLInftyErrorEst.result]
        # maxLInftyErrorEstTmpResult = [elem['maxLInftyErrorEst'] for elem in self.maxLInftyErrorEst.result]
        ax.plot(
            maxErrorEstTmpTimes,
            maxErrorEstTmpResult,
            color='blue',
            marker='.')
        ax.plot(
            maxErrorEstTmpTimes,
            maxLInftyErrorEstTmpResult,
            color='red',
            marker='.')
        self.result = fig
        # plt.show()
        # print(self.maxAdversAttack.result)
        # print(self.maxLInftyErrorEst.result)
        # print(self.maxErrorEst.result)

    def storeSMTResult(self, tmpFolderSmt):
        # we create a folder with the current timestamp. In this folder all the
        # plots should be stored as files
        cwd = os.getcwd()
        os.chdir(tmpFolderSmt)
        # with
        # open(os.getcwd()+'/'+str(self.maxErrorEst.name)+'_'+str(self.maxErrorEst.boundingBox)[:20]
        # + '.txt', 'w') as file:
        with open(os.path.join(os.getcwd(), str(self.maxErrorEst.name) + '_' + str(self.maxErrorEst.boundingBox)[:20] + '.txt'), 'w') as file:
            json.dump(self.maxErrorEst.result, file, indent=0)
        # with open(os.getcwd()+'/'+str(self.maxLInftyErrorEst.name)+'_'+str(self.maxLInftyErrorEst.boundingBox)[:20] + '.txt', 'w') as file:
            # json.dump(self.maxLInftyErrorEst.result, file, indent = 0)
        plt.figure(self.result.number)
        # plt.savefig(os.getcwd()+'/'+str(self.name))
        # tikz.save(os.getcwd()+'/'+str(self.name) + '.tex')
        plt.savefig(os.path.join(os.getcwd(), str(self.name)))
        tikz.save(os.path.join(os.getcwd(), str(self.name) + '.tex'))
        plt.close('all')
        file = './maxAdversAttackSeverity.csv'
        with open(file, 'w') as file:
            file.write(
                'The severity of this solution is: {}'.format(
                    self.maxAdversAttack.result))
            file.write('\n')
            file.write(
                'The MSE on this point is: {}'.format(
                    self.maxAdversAttack.AEError))
            file.write('\n')
            file.write(
                'The theoretical maximum Error for the severity is: {}'.format(
                    self.maxAdversAttack.theoMaxError))
            file.write('\n')
            file.write(
                'The calculation Time is: {}'.format(
                    self.maxAdversAttack.calcTime))
        os.chdir(cwd)
