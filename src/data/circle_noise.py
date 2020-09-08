from .dataset import dataset
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import product


class circle_noise(dataset):
    """This Class implements a dataset showing a 2-d circle in the first 2 dimensions and gaussian noise in all the other dimensions"""

    def __init__(
            self,
            name,
            seed,
            purpose_flg,
            num_datapoints,
            num_dims_circle,
            num_dims_total):
        super(
            circle_noise,
            self).__init__(
            name,
            seed,
            purpose_flg,
            ts_flg=False)
        self.num_datapoints = num_datapoints
        self.num_dims_total = num_dims_total
        self.num_dims_circle = num_dims_circle
        # first we sample from gaussian, then we calculate x/10 + x
        gaussians_dims_circle = np.random.normal(
            0, 1, size=(num_datapoints, self.num_dims_circle))
        ring_dims_circle = gaussians_dims_circle / 10 + gaussians_dims_circle * \
            1 / (np.linalg.norm(gaussians_dims_circle, axis=1).reshape(-1, 1))
        if self.num_dims_total > self.num_dims_circle:
            gaussians_rest = np.random.normal(
                0,
                1,
                size=(
                    num_datapoints,
                    self.num_dims_total -
                    self.num_dims_circle))
            dataset = np.hstack((ring_dims_circle, gaussians_rest))
            self.data = pd.DataFrame(dataset)
        else:
            self.data = pd.DataFrame(ring_dims_circle)
