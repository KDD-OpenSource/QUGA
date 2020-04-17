"""this file creates Sine Noise Data"""
from .dataset import dataset

import numpy as np
import pandas as pd



"""
The twoSineAmplitudesNoise class is a Dataset that returns two classes of sine curves with Noise. One starts at 0 and the other at pi
It has the following parameters:
	-> wavelength of the Wave
	-> number of 2pi cycles
	-> step_size
	-> Std-Variance of Noise (default = 0.1)
"""
class twoSineAmplitudesNoise(dataset):
	"""docstring for twoSineAmplitudesNoise"""
	def __init__(self, name, seed, purposeFlg, cycleLength, numCycles0, cycleAmplitude0, numCycles1, cycleAmplitude1, var):
		super(twoSineAmplitudesNoise, self).__init__(name, seed, purposeFlg, tsFlg = True)
		yAxis0 = cycleAmplitude0 * np.sin(np.arange(0,2*np.pi, (2*np.pi)/cycleLength))
		yAxis1 = cycleAmplitude1 * np.sin(np.arange(0,2*np.pi, (2*np.pi)/cycleLength))
		cycles0Points = pd.DataFrame(data = [yAxis0 + np.random.normal(0,var,cycleLength) for i in range(numCycles0)])
		cycles1Points = pd.DataFrame(data=[yAxis1 + np.random.normal(0,var,cycleLength) for i in range(numCycles1)])

		totalPoints = pd.concat([cycles0Points, cycles1Points]).sample(frac = 1).reset_index(drop = True)
		self.data = pd.DataFrame(totalPoints.values.reshape(-1,1)).dropna().reset_index(drop=True)
