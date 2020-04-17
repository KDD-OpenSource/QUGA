"""
This file implements the 'origReconParallelPlot' class which plots both the original and the (AE-)reconstructed data in parallel coordinates
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .resultAE import resultAE
from ..utils import myUtils

class origReconParallelPlot(resultAE):
	"""docstring for origReconParallelPlot"""
	def __init__(self, name ='origReconParallelPlot'):
		super(origReconParallelPlot, self).__init__(name)
		self.algorithm = None
		self.trainData = None
		self.testData = None
		self.orig = None
		self.recon = None
		self.figure = None

	def calcResult(self, algorithm, trainData, testData):
		self.algorithm = algorithm
		self.trainData = trainData
		# self.testData = testData
		
		# TMP!
		self.testData = trainData
		# import pdb;pdb.set_trace()

		self.orig = np.array(self.testData.data)
		if self.testData.tsFlg == True:
			self.testData.timeseriesToPoints(windowLength = algorithm.architecture[0])
			self.recon = np.array(algorithm.predict(self.testData.data))

			# testData.pointsToTimeseries()
			# self.recon = myUtils.pointsToTimeseries(self.recon)
		else:
			self.recon = np.array(algorithm.predict(self.testData.data))
		# fig, ax = plt.subplots(2,1, sharey = True, figsize = (20,10))
		fig, ax = plt.subplots(1,1, sharey = True, figsize = (20,10))
		self.testData.data = self.testData.data.transpose()
		# self.orig = self.orig.transpose()
		self.recon = self.recon.transpose()
		# ax[0].plot(self.orig, linewidth = 0.5, marker = '.', alpha = 0.2)
		# ax[0].plot(self.testData.data, linewidth = 0.5, marker = '.', alpha = 0.1)
		ax.title.set_text('Original:')
		ax.plot(self.testData.data, linewidth = 0.5, alpha = 0.05)
		# ax[0].title.set_text('Original:')
		# ax[1].plot(self.recon, linewidth = 0.5, alpha = 0.1)	
		# ax[1].title.set_text('Reconstruction:')
		# ax.plot(self.recon, linewidth = 0.5, alpha = 0.1)	
		# ax.title.set_text('Reconstruction:')
		self.result = fig