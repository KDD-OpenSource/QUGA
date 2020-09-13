from ..utils import myUtils
from .resultAE import resultAE
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


class origReconTsPlot(resultAE):
    """This class plots the reconstructed vs the original plot"""

    def __init__(self, numDataPoints=-1, name='origReconTsPlot'):
        super(origReconTsPlot, self).__init__(name)
        self.algorithm = None
        self.data = None
        self.orig = None
        self.recon = None
        self.name = 'origReconTsPlot'
        self.numDataPoints = numDataPoints

    def calcResult(self, algorithm, trainData, testData):
        self.algorithm = algorithm
        self.trainData = trainData
        self.testData = testData
        self.orig = np.array(self.testData.data)
        if self.numDataPoints == -1:
            numDataPoints = self.orig.shape[0]
        else:
            numDataPoints = self.numDataPoints
        # tsFlg indicates whether the time series is already given in sequences
        # for the autoencoder to use or whether we have to extract sequences
        # from a contiguous timeseries with a sliding window
        if self.testData.tsFlg:
            testData.timeseriesToPoints(windowLength=algorithm.architecture[0])
            self.recon = np.array(algorithm.predict(self.testData.data))
            testData.pointsToTimeseries()
            self.recon = myUtils.pointsToTimeseries(
                self.recon, windowStep=testData.windowStep)
        else:
            self.recon = np.array(algorithm.predict(self.testData.data))

        fig, ax = plt.subplots(1, 1, figsize=(20, 10))
        ax.plot(self.orig[:numDataPoints], label='Original', color='blue')
        ax.plot(self.recon[:numDataPoints],
                label='Reconstruction', color='red')
        plt.legend(loc='best')
        self.result = fig
