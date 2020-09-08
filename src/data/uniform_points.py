"""
This file implements the 'uniform_points' class. It creates data, that is sampled from the uniform distribution on its limits. One can specify the limits for each dimension and the number of points drawn
"""
from .dataset import dataset
import numpy as np
import pandas as pd


class uniform_points(dataset):
    """docstring for uniform_points"""

    def __init__(self, name, seed, purpose_flg, limits, num_data_points):
        super(uniform_points, self).__init__(name, seed, purpose_flg)
        self.limits = np.array(limits)
        self.num_data_points = num_data_points
        data = np.random.uniform(low=self.limits[:, 0], high=self.limits[:, 1], size=(
            self.num_data_points, self.limits.shape[0]))
        # TODO
        self.data_points = [tuple(elem) for elem in data]
        self.data = pd.DataFrame(self.data_points)
