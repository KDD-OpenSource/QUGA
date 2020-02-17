import numpy as np
import pandas as pd
from .resultAE import resultAE
from ..utils import myUtils
from itertools import product

class avgError(resultAE):
	"""This class plots the reconstructed vs the original plot"""
	def __init__(self, name ='avgError'):
		super(avgError, self).__init__(name)
		self.algorithm = None
		self.data = None
		self.name = 'avgError'
		self.avgError = None
		self.result = None

	def calcResult(self, algorithm, trainDataset, testDataset):
		self.algorithm = algorithm
		self.testDataset = testDataset
		self.orig = np.array(self.testDataset.data)
		if self.testDataset.tsFlg == True:
			testDataset.timeseriesToPoints(windowLength = algorithm.architecture[0])
			self.recon = np.array(algorithm.predict(self.testDataset.data))
			self.avgError = pd.DataFrame([np.square(np.subtract(self.recon, self.testDataset.data)).sum(axis=1).mean()])
			testDataset.pointsToTimeseries()
		else:
			raise Exception('avg Error for non-TS Data has not been tested')
			# self.recon = np.array(algorithm.predict(self.testDataset.data))
			# self.avgErrog = np.square(np.subtract(self.recon, self.testDataset.data)).sum(axis=1).mean()

		self.result = self.avgError