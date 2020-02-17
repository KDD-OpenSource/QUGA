import abc
from .result import result
from itertools import product
import os
import matplotlib.pyplot as plt
import pandas as pd
'''I think this class really makes no sense. What do I encapsulate here for? What are shared properties of 'results' that are worth sharing? (Not existing currently) '''


"""
NOTE THAT IF YOU COMPARE TEST AND TRAIN DATA THEY NEED TO HAVE THE SAME STRUCTURE
Note that if only one dataset is needed for the plot we use the test_data per default
"""
class resultAE(result):
	def __init__(self, name):
		self.name = name
		self.result = None
		pass

	def storeAEResult(self, folder, trainDataset,testDataset, algorithm, testName):
	# we create a folder with the current timestamp. In this folder all the plots should be stored as files
		cwd = os.getcwd()
		os.chdir(folder)

		if isinstance(self.result, plt.Figure):
			self.result.suptitle(f'Alg: {algorithm.name},\n Train-Dataset: {trainDataset.name}, \n Test-Dataset: {testDataset.name}')
			plt.savefig(os.getcwd()+'\\'+str(self.name))
			plt.close('all')
		elif isinstance(self.result, pd.DataFrame):
			self.result.to_csv(os.getcwd()+'\\'+str(self.name) + '.csv', header = False)
		else:
			print("Your result is not in the appropriate format, hence it did not get saved")
			#some other code
		if self.name  == 'pwDistance':
			sequencePlotPw = sequencePlotInd(seed = self.seed)
			pwDistFig = sequencePlotPw.getResult(algorithm, trainDataset, testDataset, self.result.iloc[-1:,-2:])
			plt.savefig(os.getcwd() + '\\' + str('pwDistancePlot'))
			plt.close('all')

		os.chdir(cwd)
