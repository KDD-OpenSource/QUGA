"""
This file implements the 'origReconPairPlot' class which plots both the original and the (AE-)reconstructed data with each dimension paired
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .resultAE import resultAE
from ..utils import myUtils
from itertools import product

class origReconPairPlot(resultAE):
	"""docstring for origReconPairPlot"""
	def __init__(self, name ='origReconPairPlot'):
		super(origReconPairPlot, self).__init__(name)
		self.algorithm = None
		self.trainData = None
		self.testData = None
		self.orig = None
		self.recon = None
		self.figure = None
		self.numDims = None

	def calcResult(self, algorithm, trainData, testData):
		self.algorithm = algorithm
		self.trainData = trainData
		self.testData = testData
		self.orig = np.array(self.testData.data)
		if self.testData.tsFlg == True:
			testData.timeseriesToPoints(windowLength = algorithm.architecture[0])
			self.recon = np.array(algorithm.predict(self.testData.data))
			testData.pointsToTimeseries()
			self.recon = myUtils.pointsToTimeseries(self.recon)
		else:
			self.recon = np.array(algorithm.predict(self.testData.data))
		self.numDims = algorithm.architecture[0]
		fig, ax = plt.subplots(self.numDims, self.numDims, sharey = True, figsize = (20,20))
		for i,j in product(range(self.numDims), range(self.numDims)):
			ax[i,j].scatter(self.orig[:,i], self.orig[:,j], color = 'blue')
			ax[i,j].scatter(self.recon[:,i], self.recon[:,j], color = 'orange')
			self.result = fig