from .dataset import dataset
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from itertools import product


class circleNoise(dataset):
	"""This Class implements a dataset showing a 2-d circle in the first 2 dimensions and gaussian noise in all the other dimensions"""
	def __init__(self, name, seed, purposeFlg, numDatapoints, numDimsCircle, numDimsTotal):
		super(circleNoise, self).__init__(name, seed, purposeFlg, tsFlg = False)
		self.numDatapoints = numDatapoints
		self.numDimsTotal = numDimsTotal
		self.numDimsCircle = numDimsCircle
		# first we sample from gaussian, then we calculate x/10 + x
		gaussiansDimsCircle = np.random.normal(0,1,size = (numDatapoints, self.numDimsCircle))
		ringDimsCircle = gaussiansDimsCircle/10 + gaussiansDimsCircle*1/(np.linalg.norm(gaussiansDimsCircle, axis = 1).reshape(-1,1))
		if self.numDimsTotal > self.numDimsCircle:
			gaussiansRest = np.random.normal(0,1,size = (numDatapoints, self.numDimsTotal-self.numDimsCircle))
			dataset = np.hstack((ringDimsCircle, gaussiansRest))
			self.data = pd.DataFrame(dataset)
		else:
			self.data = pd.DataFrame(ringDimsCircle)