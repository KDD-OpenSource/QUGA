"""
This class is used to estimate the maximum error in a customBoundingBox by
sampling points in the box, applying the autoencoder to them and saving the
largest error. One specifies times after which the maximum error is captured
instead of giving the number of samples.
"""
import numpy as np
import pandas as pd
from .resultSMT import resultSMT
import os
import json
import time

class maxErrorEst(resultSMT):
    """This class estimates the maximum Error in a given box"""
    def __init__(self, times_s, errFct ,name='maxErrorEst'):
        super(maxErrorEst, self).__init__(name)
        self.algorithm = None
        self.name = 'maxErrorEst'
        self.maxErrorEst = None
        self.result = None
        self.boundingBox = None
        self.times_s = times_s
        self.errFct = errFct

    def calcResult(self, algorithm, trainDataset, smt):
        if 'customBoundingBox' in smt.abstractConstr:
            self.boundingBox = smt.abstractConstr['customBoundingBox']
        else:
            raise Exception('This plot only makes sense with a bounding box.')
        self.algorithm = algorithm
        self.result = []
        start = time.time()
        while(time.time() < start + self.times_s[-1]):
            numSamples = 0
            tmpMax = 0
            for time_s in self.times_s:
                numSamples, tmpMax = self.sampleUntilFixedTime(
                        numSamples,
                        algorithm,
                        start,
                        time_s,
                        tmpMax
                        )
                self.result.append({'time': time_s,
                                    'maxErrorEst': tmpMax,
                                    'numSamples': numSamples})

    def sampleUntilFixedTime(self, numSamples, algorithm, start, time_s, tmpMax):
        while(time.time() < start + time_s):
            uniformSample = np.random.uniform(
                low=np.array(self.boundingBox).transpose()[0],
                high=np.array(self.boundingBox).transpose()[1],
                size=(1,len(self.boundingBox))
                )
            numSamples = numSamples + 1
            prediction = np.array(
                algorithm.predict(
                    pd.DataFrame(uniformSample)))
            if self.errFct == 'LInfty':
                maxErrorEst = np.absolute(
                    np.subtract(
                        uniformSample,
                        prediction)).max()
            elif self.errFct == 'L2':
                maxErrorEst = np.square(
                    np.subtract(
                        uniformSample,
                        prediction)).sum()
            else:
                raise Exception('Need an error fct for sampling.')
            if maxErrorEst > tmpMax:
                tmpMax = maxErrorEst
        return numSamples, tmpMax

    def storeSMTResult(self, tmpFolderSmt):
        cwd = os.getcwd()
        os.chdir(tmpFolderSmt)
        with open(os.path.join(os.getcwd(), str(self.name) + '_' + str(self.boundingBox)[:20] + '.txt'), 'w') as file:
            json.dump(self.result, file, indent=0)
        os.chdir(cwd)
