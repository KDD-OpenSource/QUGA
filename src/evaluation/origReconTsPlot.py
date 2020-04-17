import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from .resultAE import resultAE
from ..utils import myUtils
from itertools import product

class origReconTsPlot(resultAE):
	"""This class plots the reconstructed vs the original plot"""
	def __init__(self, numDataPoints= -1,name ='origReconTsPlot'):
		super(origReconTsPlot, self).__init__(name)
		self.algorithm = None
		self.data = None
		self.orig = None
		self.recon = None
		self.name = 'origReconTsPlot'
		self.numDataPoints = numDataPoints

	def calcResult(self, algorithm, trainData, testData):
		self.algorithm = algorithm
		self.trainData = trainData
		self.testData = testData
		self.orig = np.array(self.testData.data)
		if self.numDataPoints == -1:
			numDataPoints = self.orig.shape[0]
		else:
			numDataPoints = self.numDataPoints
		if self.testData.tsFlg == True:
			testData.timeseriesToPoints(windowLength = algorithm.architecture[0])
			self.recon = np.array(algorithm.predict(self.testData.data))
			testData.pointsToTimeseries()
			self.recon = myUtils.pointsToTimeseries(self.recon, windowStep = testData.windowStep)
		else:
			self.recon = np.array(algorithm.predict(self.testData.data))

		# fig, ax = plt.subplots(1,1, sharey = True, figsize = (20,10))
		fig, ax = plt.subplots(1,1, figsize = (20,10))	
		ax.plot(self.orig[:numDataPoints], label = 'Original', color  = 'blue')
		ax.plot(self.recon[:numDataPoints], label = 'Reconstruction', color = 'red')	
		plt.legend(loc = 'best')
		self.result = fig
