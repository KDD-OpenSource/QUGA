import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .resultAE import resultAE
from .avgError import avgError
from ..utils import myUtils
from itertools import product

class maxErrorEstAEParamPlot(resultAE):
	"""This class plots the reconstructed vs the original plot"""

	def __init__(self, AEParam,boundingBox, sampleSize, name ='maxErrorEstAEParamPlot'):
		super(maxErrorEstAEParamPlot, self).__init__(name)
		self.name = 'maxErrorEstAEParamPlot'
		self.collResults = pd.DataFrame(columns = ['algorithm', 'trainDataset', 'maxErrorEst', 'boundingBox', 'sampleSize'])
		self.maxErrorEst = None
		self.result = None
		self.figures = None
		self.boundingBox = boundingBox
		self.sampleSize = sampleSize
		self.AEParam = AEParam

	def calcResult(self, algorithm, trainDataset, testDataset):
		uniformSample = np.random.uniform(low = np.array(self.boundingBox).transpose()[0], high = np.array(self.boundingBox).transpose()[1], size = (self.sampleSize,len(self.boundingBox)))
		self.algorithm = algorithm
		prediction = np.array(algorithm.predict(pd.DataFrame(uniformSample)))
		maxErrorEstTmp = pd.DataFrame([np.square(np.subtract(uniformSample, prediction)).mean(axis=1).max()])
		self.maxErrorEst = maxErrorEstTmp.values.flatten()

		print('maxErrorEst in calcResult: {}'.format(self.maxErrorEst))
		# print(self.maxErrorEst)
		resultToAppend = pd.DataFrame(columns = ['algorithm', 'trainDataset', 'maxErrorEst', 'boundingBox', 'sampleSize'], data = [[algorithm, trainDataset, self.maxErrorEst, self.boundingBox, self.sampleSize]])
		self.collResults = self.collResults.append(resultToAppend)

	def storeAEResult(self, folder, trainDataset,testDataset, algorithm, testName):
		pass

	def calcCollectedAEResults(self):
		self.figures = []
		for trainDataset in self.collResults['trainDataset'].unique():
			maxError = self.calcMaxError()
			self.figures.append({'figure': self.calcCollectedAEResult(trainDataset, maxError), 'trainDataset': trainDataset, 'boundingBox': self.boundingBox, 'sampleSize': self.sampleSize})

	def calcCollectedAEResult(self, trainDataset, maxError):
		tmpDataFrame = self.collResults[(self.collResults['trainDataset'] == trainDataset)]
		AEParams = sorted([x[self.AEParam] for x in tmpDataFrame['algorithm']])
		y_pos = np.arange(len(AEParams))
		avgErrors = tmpDataFrame['maxErrorEst'].values.tolist()
		fig = plt.figure(figsize = (20,10))
		plt.plot(y_pos, avgErrors, marker = '.')
		axes = plt.gca()
		axes.set_ylim([0,1.1*maxError])
		plt.xticks(y_pos, AEParams, rotation = 90)
		return fig

	def storeCollectedAEResults(self, runFolder):
		for figureDict in self.figures:
			self.storeCollectedAEResult(runFolder, figureDict)

	def storeCollectedAEResult(self, folder, figureDict):
		plt.figure(figureDict['figure'].number)
		# trainDatasetName = figureDict['trainDataset'].name
		# figureDict['figure'].suptitle(f'Train-Dataset: {trainDatasetName}, \n Test-Dataset: {testDatasetName}')
		plt.savefig(folder + '//'+'maxEstErrors_'+str(figureDict['trainDataset'].obj_id)[:4]+'_' + str(figureDict['boundingBox'])[:5]+ '_' + str(figureDict['sampleSize'])+'.png')
		# plt.close('all')


	def calcMaxError(self):
		print('in maxErrorEst: {}'.format(self.collResults))
		print('in maxErrorEst: {}'.format(self.collResults['maxErrorEst']))
		maxError = self.collResults['maxErrorEst'].max()
		return maxError


	# I want the plot function to plot over all autoencoders with different architectures (that is we group by everything except by architecture)