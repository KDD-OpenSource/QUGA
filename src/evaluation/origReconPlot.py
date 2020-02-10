import matplotlib.pyplot as plt
import numpy as np
from .result import result
from ..utils import myUtils


class origReconPlot(result):
	"""This class plots the reconstructed vs the original plot"""
	def __init__(self, name ='origReconPlot'):
		super(origReconPlot, self).__init__(name, aeSmtFlg = 'ae')
		self.algorithm = None
		self.data = None
		self.orig = None
		self.recon = None
		self.name = 'origReconPlot'

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
		ax[0].plot(self.orig, linewidth = 0.0005, marker = '.')
		ax[0].title.set_text('Original:')
		ax[1].plot(self.recon, linewidth = 0.0005, marker = '.')	
		ax[1].title.set_text('Reconstruction:')
		# ax[0].plot(self.orig, linewidth = 0.5)
		# ax[0].title.set_text('Original:')
		# ax[1].plot(self.recon, linewidth = 0.5)	
		# ax[1].title.set_text('Reconstruction:')
		return fig
