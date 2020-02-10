"""
This file implements the 'origReconParallelPlot' class which plots both the original and the (AE-)reconstructed data in parallel coordinates
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .result import result
from ..utils import myUtils

class origReconParallelPlot(result):
	"""docstring for origReconParallelPlot"""
	def __init__(self, name ='origReconParallelPlot'):
		super(origReconParallelPlot, self).__init__(name, aeSmtFlg = 'ae')
		self.algorithm = None
		self.trainData = None
		self.testData = None
		self.orig = None
		self.recon = None
		self.figure = None

	def getResult(self, algorithm, trainData, testData):
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
		fig, ax = plt.subplots(2,1, sharey = True, figsize = (20,10))
		self.orig = self.orig.transpose()
		self.recon = self.recon.transpose()
		ax[0].plot(self.orig, linewidth = 0.5, marker = '.')
		ax[0].title.set_text('Original:')
		ax[1].plot(self.recon, linewidth = 0.5, marker = '.')	
		ax[1].title.set_text('Reconstruction:')
		return fig
