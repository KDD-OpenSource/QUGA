"""
This file implements the 'maxAdversAttack' class, which is a result that plots one advers. attack in parallel coordinates. I.e. it gets the solution from an smt-solver and visualizes them next to each other. 
"""

from .result import result
# from ..utils.myUtils import solutionsToPoints
import matplotlib.pyplot as plt
import time

class maxAdversAttack(result):
	def __init__(self, name = 'maxAdversAttack', accuracy = 0.1):
		super(maxAdversAttack, self).__init__(name, aeSmtFlg = 'smt')
		self.result = None
		self.smtSolutions = None
		self.accuracy = accuracy

	def getResult(self, autoencoder, trainData, testData, smt):
		if 'adversAttack' in smt.abstractConstr:
			smt.addAEConstr(autoencoder)
			self.result, self.smtSolutions = smt.calcMaxAdversAttack(startValue = smt.abstractConstr['adversAttack']['severity'], accuracy = self.accuracy)
