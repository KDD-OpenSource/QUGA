"""this file creates Sine Noise Data"""
from .dataset import dataset

import numpy as np
import pandas as pd


"""
The sampleBoxTest class is a Dataset that returns two classes of sine curves with Noise. One starts at 0 and the other at pi
It has the following parameters:
	-> wavelength of the Wave
	-> number of 2pi cycles
	-> step_size
	-> Std-Variance of Noise (default = 0.1)
"""


class sampleBoxTest(dataset):
    """docstring for sampleBoxTest"""

    def __init__(self, name, seed, purposeFlg, box, numPoints, windowStep=1):
        super(
            sampleBoxTest,
            self).__init__(
            name=name,
            seed=seed,
            purposeFlg=purposeFlg,
            windowStep=windowStep,
            tsFlg=False)
        uniformSample = np.random.uniform(
            low=np.array(box).transpose()[0],
            high=np.array(box).transpose()[1],
            size=(
                numPoints,
                len(box)))

        self.data = pd.DataFrame(uniformSample)
        # yAxis0 = np.sin(np.arange(0,2*np.pi, (2*np.pi)/cycleLength0))
        # yAxis1 = np.sin(np.arange(0,2*np.pi, (2*np.pi)/cycleLength1))
        # cycles0Points = pd.DataFrame(data = [yAxis0 + np.random.normal(0,var,cycleLength0) for i in range(numCycles0)])
        # cycles1Points = pd.DataFrame(data=[yAxis1 + np.random.normal(0,var,cycleLength1) for i in range(numCycles1)])

        # totalPoints = pd.concat([cycles0Points, cycles1Points]).sample(frac = 1).reset_index(drop = True)
        # self.data = pd.DataFrame(totalPoints.values.reshape(-1,1)).dropna().reset_index(drop=True)
