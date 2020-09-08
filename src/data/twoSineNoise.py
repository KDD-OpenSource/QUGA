"""this file creates Sine Noise Data"""
from .dataset import dataset

import numpy as np
import pandas as pd


"""
The twoSineNoise class is a Dataset that returns two classes of sine curves with Noise. One starts at 0 and the other at pi
It has the following parameters:
	-> wavelength of the Wave
	-> number of 2pi cycles
	-> step_size
	-> Std-Variance of Noise (default = 0.1)
"""


class twoSineNoise(dataset):
    """docstring for twoSineNoise"""

    def __init__(self, name, seed, purposeFlg, wavelength, num0, numPi, var):
        super(twoSineNoise, self).__init__(name, seed, purposeFlg, tsFlg=False)
        self.num0 = num0
        self.numPi = numPi
        self.var = var
        self.wavelength = wavelength
        xAxis = np.arange(0, 2 * np.pi, (2 * np.pi) / wavelength)
        yAxis = np.sin(np.arange(0, 2 * np.pi, (2 * np.pi) / wavelength))
        yAxisShift = np.sin(
            np.arange(
                np.pi,
                np.pi + 2 * np.pi,
                (2 * np.pi) / wavelength))
        num0Points = pd.DataFrame(
            data=[
                yAxis +
                np.random.normal(
                    0,
                    var,
                    wavelength) for i in range(num0)])
        numPiPoints = pd.DataFrame(
            data=[
                yAxisShift +
                np.random.normal(
                    0,
                    var,
                    wavelength) for i in range(numPi)])
        self.data = pd.concat([num0Points, numPiPoints]).sample(
            frac=1).reset_index(drop=True)
