"""
This file implements the 'maxAdversAttack' class, which is a result that plots one advers. attack in parallel coordinates. I.e. it gets the solution from an smt-solver and visualizes them next to each other. 
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


class maxAdversAttack(resultSMT):
	def __init__(self, name = 'maxAdversAttack', accuracy = 0.1):
		super(maxAdversAttack, self).__init__(name)
		self.result = None
		self.calcTime = None
		self.smtSolutions = None
		self.accuracy = accuracy
		self.AEError = None
		self.theoMaxError = None

	def calcResult(self, algorithm, trainDataset, smt):
		if 'adversAttack' in smt.abstractConstr:
			smt.addAEConstr(algorithm)
			maxAdversAttack = smt.getMaxAdversAttack(startValue = smt.abstractConstr['adversAttack']['severity'], accuracy = self.accuracy, algorithm = algorithm, trainDataset = trainDataset)
			self.result  = maxAdversAttack['severity']
			self.calcTime = maxAdversAttack['calcTime']
			self.smtSolutions = maxAdversAttack['smtModel']
			# Todo: extract max variable to account for different architectures
			points = solutionsToPoints(self.smtSolutions, ['x_0', 'x_2'])
			pointsDF = pd.DataFrame(points[0][0]).transpose()
			autoencoderSolution = algorithm.getAEResults(pointsDF)[1]
			# smtSolutionsError = euclidean_distances([points[0][0]],[points[0][1]])
			pointsDFValues = pointsDF.values
			autoencoderSolutionValues = autoencoderSolution.values
			self.AEError = np.mean(np.square(np.subtract(pointsDFValues,autoencoderSolutionValues)))
			self.theoMaxError = np.array([self.result*self.result for x in range(pointsDF.shape[1])]).flatten().mean()




	def storeSMTResult(self, tmpFolderSmt):
		self.saveSmtSolutions(tmpFolderSmt)
		cwd = os.getcwd()
		os.chdir(tmpFolderSmt)		
		file = './maxAdversAttackSeverity.csv'
		with open(file, 'w') as file:
			file.write('The severity of this solution is: {}'.format(self.result))
			file.write('\n')
			file.write('The MSE on this point is: {}'.format(self.AEError))
			file.write('\n')
			file.write('The theoretical maximum Error for the severity is: {}'.format(self.theoMaxError))
			file.write('\n')
			file.write('The calculation Time is: {}'.format(self.calcTime))
		os.chdir(cwd)

