import numpy as np
import pandas as pd
from .result import result
from ..utils import myUtils


class avgError(result):
	"""This class plots the reconstructed vs the original plot"""
	def __init__(self, name ='avgError'):
		super(avgError, self).__init__(name, aeSmtFlg = 'ae')
		self.algorithm = None
		self.data = None
		self.name = 'avgError'
		self.avgError = None

	def getResult(self, algorithm, trainData, testData):
		self.algorithm = algorithm
		self.trainData = trainData
		self.testData = testData
		self.orig = np.array(self.testData.data)
		if self.testData.tsFlg == True:
			testData.timeseriesToPoints(windowLength = algorithm.architecture[0])
			self.recon = np.array(algorithm.predict(self.testData.data))
			self.avgError = pd.DataFrame([np.square(np.subtract(self.recon, self.testData.data)).sum(axis=1).mean()])
			testData.pointsToTimeseries()
		else:
			raise Exception('avg Error for non-TS Data has not been tested')
			# self.recon = np.array(algorithm.predict(self.testData.data))
			# self.avgErrog = np.square(np.subtract(self.recon, self.testData.data)).sum(axis=1).mean()

		return self.avgError