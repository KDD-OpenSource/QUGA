"""this file creates Sine Noise Data"""
from .dataset import dataset

import numpy as np
import pandas as pd



"""
The sineNoise class is a Dataset that returns a sine-Wave with Noise
It has the following parameters:
	-> length of the Wave
	-> number of 2pi cycles
	-> step_size
	-> Std-Variance of Noise (default = 0.1)
"""
class sineNoise(dataset):
	"""docstring for SineNoise"""
	def __init__(self, name, seed, purposeFlg,length, cycles, var, bounded):
		super(sineNoise, self).__init__(name, seed, purposeFlg, tsFlg = True)
		self.length = length
		self.cycles = cycles
		self.var = var	
		xAxis = np.arange(0, 2*np.pi*cycles, (2*np.pi*cycles)/length)
		yAxis = np.sin(xAxis)
		noise = np.random.normal(0,var, length)
		yAxisWithNoise = yAxis+noise
		if bounded:
			self.data = dataset.boundedData(pd.DataFrame(yAxisWithNoise))
		else:
			self.data = pd.DataFrame(yAxisWithNoise)