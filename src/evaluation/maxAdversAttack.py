"""
This file implements the 'maxAdversAttack' class, which is a result that plots one advers. attack in parallel coordinates. I.e. it gets the solution from an smt-solver and visualizes them next to each other. 
"""
from .resultSMT import resultSMT
# from ..utils.myUtils import solutionsToPoints
import matplotlib.pyplot as plt
import time
# from ..utils.myUtils import saveSmtSolutions


class maxAdversAttack(resultSMT):
	def __init__(self, name = 'maxAdversAttack', accuracy = 0.1):
		super(maxAdversAttack, self).__init__(name)
		self.result = None
		self.smtSolutions = None
		self.accuracy = accuracy

	def calcResult(self, algorithm, trainDataset, smt):
		if 'adversAttack' in smt.abstractConstr:
			smt.addAEConstr(algorithm)
			maxAdversAttack = smt.getMaxAdversAttack(startValue = smt.abstractConstr['adversAttack']['severity'], accuracy = self.accuracy, algorithm = algorithm, trainDataset = trainDataset)
			self.result  = maxAdversAttack['severity']
			self.smtSolutions = maxAdversAttack['smtModel']

	def storeSMTResult(self, tmpFolderSmt):
		self.saveSmtSolutions(tmpFolderSmt)
		file = './maxAdversAttackSeverity.csv'
		with open(file, 'w') as file:
			file.write('\n')
			file.write('The severity of this solution is: {}'.format(self.result))
