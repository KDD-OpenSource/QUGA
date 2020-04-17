"""this file creates Sine Noise Data"""
from .dataset import dataset

import numpy as np
import pandas as pd


# cycleLengths = [40,120]
# cycleSplits = [1,3]
# numPerCluster = [[0],[30,100,30]]

"""
The twoSineFrequenciesNoiseTest class is a Dataset that returns two classes of sine curves with Noise. One starts at 0 and the other at pi
It has the following parameters:
	-> wavelength of the Wave
	-> number of 2pi cycles
	-> step_size
	-> Std-Variance of Noise (default = 0.1)
"""
class twoSineFrequenciesNoiseTest(dataset):
	"""docstring for twoSineFrequenciesNoiseTest"""
	# def __init__(self, name, seed, purposeFlg, numCycles0, cycleLength0, numCycles1, cycleLength1, var, windowStep = 1):
	def __init__(self, name, seed, purposeFlg, cycleLengths, cycleSplits, numPerCluster, var, windowStep = 1):
		super(twoSineFrequenciesNoiseTest, self).__init__(name=name, seed=seed, purposeFlg = purposeFlg, windowStep = windowStep,tsFlg = True)
		totalPoints = pd.DataFrame()
		import pdb; pdb.set_trace()
		for cycleInd in range(len(cycleLengths)):
			for splitInd in range(len(cycleSplits)):
				# yAxis = []
				yAxis = np.sin(np.arange(0,2*np.pi, (2*np.pi)/cycleLengths[cycleInd]))
				yAxis.reshape(cycleSplits[cycleInd],-1)
				if len(yAxis.shape) ==1:
					yAxis = np.array([yAxis]) 

				for clusterSizeInd in range(len(numPerCluster[splitInd])):
					cyclesPoints = pd.DataFrame(data = [yAxis[clusterSizeInd] + np.random.normal(0,var,int(cycleLengths[cycleInd]/cycleLengths[cycleInd])) for i in range(numPerCluster[splitInd][clusterSizeInd])])
					totalPoints = pd.concat([totalPoints, cyclesPoints]).sample(frac = 1).reset_index(drop = True)


		# yAxis0 = np.sin(np.arange(0,2*np.pi, (2*np.pi)/cycleLength0))
		# yAxis1 = np.sin(np.arange(0,2*np.pi, (2*np.pi)/cycleLength1))
		# cycles0Points = pd.DataFrame(data = [yAxis0 + np.random.normal(0,var,cycleLength0) for i in range(numCycles0)])
		# cycles1Points = pd.DataFrame(data=[yAxis1 + np.random.normal(0,var,cycleLength1) for i in range(numCycles1)])

		# totalPoints = pd.concat([cycles0Points, cycles1Points]).sample(frac = 1).reset_index(drop = True)
		self.data = pd.DataFrame(totalPoints.values.reshape(-1,1)).dropna().reset_index(drop=True)
