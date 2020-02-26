"""
This file implements the 'maxAdversAttackQualPlot' class, which is a result that plots one advers. attack in parallel coordinates. I.e. it gets the solution from an smt-solver and visualizes them next to each other. 
"""

from .resultSMT import resultSMT
from ..utils.myUtils import solutionsToPoints
import matplotlib.pyplot as plt
import time
import os

class maxAdversAttackQualPlot(resultSMT):
	def __init__(self, accuracy,name = 'maxAdversAttackQualPlot'):
		super(maxAdversAttackQualPlot, self).__init__(name)
		self.result = None
		self.smtSolutions = None
		self.accuracy = accuracy

	def calcResult(self, algorithm, trainDataset, smt):
		# before smt_solutions were the solutions calculated before, now it is just the model
		# add adversAttackPair constraints
		if 'adversAttack' in smt.abstractConstr:
			smt.addAEConstr(algorithm)
			maxAdversAttack = smt.getMaxAdversAttack(startValue = smt.abstractConstr['adversAttack']['severity'], accuracy = self.accuracy, algorithm = algorithm, trainDataset = trainDataset)
			self.result  = maxAdversAttack['severity']
			self.smtSolutions = maxAdversAttack['smtModel']
			if len(self.smtSolutions) != 0:
			# I want smt_solutions to be in the same format as trainData and 
				allX = [x for x in self.smtSolutions[0]['model'] if str(x)[0]=='x']
				largestLayer = max([int(str(x)[2]) for x in allX])
				lastLayerVars = [x for x in self.smtSolutions[0]['model'] if str(x)[2] == str(largestLayer)]
				solutionPoints = solutionsToPoints(self.smtSolutions,['x_0','x'+'_'+str(largestLayer)])
				fig, ax = plt.subplots(nrows=2, ncols=len(solutionPoints), squeeze = False)
				for column in range(len(solutionPoints)):
					ax[0, column].plot(solutionPoints[column][0])
					ax[0, column].title.set_text('Input of AE:')
				for column in range(len(solutionPoints)):
					ax[1, column].plot(solutionPoints[column][1])
					ax[1, column].title.set_text('Output of AE:')
				self.result = fig

	def storeSMTResult(self, tmpFolderSmt):
		if self.result != None:
			self.saveSmtSolutions(tmpFolderSmt)
			cwd = os.getcwd()
			os.chdir(tmpFolderSmt)
			plt.figure(self.result.number)
			plt.savefig(os.getcwd()+'\\'+str(self.name))
			plt.close('all')
			os.chdir(cwd)

