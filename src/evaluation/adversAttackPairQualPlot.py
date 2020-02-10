"""
This file implements the 'adversAttackPairQualPlot' class, which is a result that plots one advers. attack in parallel coordinates. I.e. it gets the solution from an smt-solver and visualizes them next to each other. 
"""

from .result import result
from ..utils.myUtils import solutionsToPoints
import matplotlib.pyplot as plt
import time

class adversAttackPairQualPlot(result):
	def __init__(self, name = 'adversAttackPairQualPlot'):
		super(adversAttackPairQualPlot, self).__init__(name, aeSmtFlg = 'smt')
		self.result = None
		self.smtSolutions = None

	def getResult(self, autoencoder, trainData, testData, smt):
		# before smt_solutions were the solutions calculated before, now it is just the model
		# add adversAttackPair constraints
		if 'adversAttackPair' in smt.abstractConstr:
			smt.addAEConstr(autoencoder)
			smt.addCustomConstr()
			smtSolutions = smt.calculateSolutions()
			if len(smtSolutions) != 0:
			# I want smt_solutions to be in the same format as trainData and testData
				allX = [x for x in smtSolutions[0]['model'] if str(x)[0]=='x']
				largestLayer = max([int(str(x)[2]) for x in allX])
				lastLayerVars = [x for x in smtSolutions[0]['model'] if str(x)[2] == str(largestLayer)]
				solutionPoints = solutionsToPoints(smtSolutions,['x_0','y_0','x'+'_'+str(largestLayer), 'y'+'_'+str(largestLayer)])
				fig, ax = plt.subplots(nrows=2, ncols=len(solutionPoints), sharey=True, squeeze = False)
				for column in range(len(solutionPoints)):
					ax[0, column].plot(solutionPoints[column][0])
					ax[0, column].plot(solutionPoints[column][1])
					ax[0, column].title.set_text('Input of AE:')
				for column in range(len(solutionPoints)):
					ax[1, column].plot(solutionPoints[column][2])
					ax[1, column].plot(solutionPoints[column][3])
					ax[1, column].title.set_text('Output of AE:')
				# plt.show()
			self.result = fig
			self.smtSolutions = smtSolutions


### This is for calculating the time later. We may attach this as a field into the smtSolver class (or better attach it to each new solution)
# start = time.time()
# print('Start Time is: {}'.format(time.strftime("%b %d %Y %H:%M:%S", time.gmtime(start))))
# solutions = smt.calculateSolutions()
# end = time.time()
# print('End Time is: {}\n'.format(time.strftime("%b %d %Y %H:%M:%S", time.gmtime(end))))
# time_for_calc = end - start		


# start = time.time()
# smtSolutions = smt.calculateSolutions()
# end = time.time()
# calcDuration = end - start
# save_smt_solutions(smtSolutions, tmp_folder_smt, calcDuration) 
