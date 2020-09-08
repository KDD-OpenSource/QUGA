import numpy as np
import pandas as pd
# from .resultAE import resultAE
from .resultSMT import resultSMT
from ..utils import myUtils
from itertools import product
import os
import json
import time


class maxLInftyErrorEst(resultSMT):
    """This class estimates the maximum Error in a given box"""
    # def __init__(self, sampleSizes, name ='maxLInftyErrorEst'):

    def __init__(self, times_s, name='maxLInftyErrorEst'):
        super(maxLInftyErrorEst, self).__init__(name)
        self.algorithm = None
        self.name = 'maxLInftyErrorEst'
        self.maxLInftyErrorEst = None
        self.result = None
        self.boundingBox = None
        # self.sampleSizes = sampleSizes
        self.times_s = times_s

    def calcResult(self, algorithm, trainDataset, smt):
        if 'customBoundingBox' in smt.abstractConstr:
            self.boundingBox = smt.abstractConstr['customBoundingBox']

            self.algorithm = algorithm
            self.result = []
            # for time_s in self.times_s:
            # 	start = time.time()
            # 	numSamples = 0
            # 	tmpMax = 0
            # 	while(time.time()< start + time_s):
            # # for sampleSize in self.sampleSizes:
            # # 	start = time.time()
            # 		uniformSample = np.random.uniform(low = np.array(self.boundingBox).transpose()[0], high = np.array(self.boundingBox).transpose()[1], size = (1,len(self.boundingBox)))
            # 		numSamples = numSamples + 1
            # 		prediction = np.array(algorithm.predict(pd.DataFrame(uniformSample)))
            # 		maxLInftyErrorEst = np.absolute(np.subtract(uniformSample, prediction)).max(axis=1).max()
            # 		if maxLInftyErrorEst > tmpMax:
            # 			tmpMax = maxLInftyErrorEst
            # 	end = time.time()
            # 	calcTime = end-start
            # 	maxLInftyErrorEst = tmpMax
            # 	self.result.append({'time': time_s, 'calcTime': calcTime, 'maxLInftyErrorEst': maxLInftyErrorEst, 'numSamples': numSamples})
            # # ToDo: add a plot of that particular point (need to reimplement the errorest for that)
            start = time.time()
            while(time.time() < start + self.times_s[-1]):
                numSamples = 0
                tmpMax = 0
                for time_s in self.times_s:
                    while(time.time() < start + time_s):
                        # for sampleSize in self.sampleSizes:
                        # 	start = time.time()
                        uniformSample = np.random.uniform(
                            low=np.array(
                                self.boundingBox).transpose()[0], high=np.array(
                                self.boundingBox).transpose()[1], size=(
                                1, len(
                                    self.boundingBox)))
                        numSamples = numSamples + 1
                        prediction = np.array(
                            algorithm.predict(
                                pd.DataFrame(uniformSample)))
                        maxLInftyErrorEst = np.absolute(
                            np.subtract(
                                uniformSample,
                                prediction)).max(
                            axis=1).max()
                        if maxLInftyErrorEst > tmpMax:
                            tmpMax = maxLInftyErrorEst
                    maxLInftyErrorEst = tmpMax
                    # self.result.append({'time': time_s, 'calcTime': calcTime, 'maxLInftyErrorEst': maxLInftyErrorEst, 'numSamples': numSamples})
                    self.result.append({'time': time_s,
                                        'maxLInftyErrorEst': maxLInftyErrorEst,
                                        'numSamples': numSamples})

                # end = time.time()
                # calcTime = end-start
                # maxLInftyErrorEst = tmpMax
                # self.result.append({'time': time_s, 'calcTime': calcTime, 'maxLInftyErrorEst': maxLInftyErrorEst, 'numSamples': numSamples})
            # ToDo: add a plot of that particular point (need to reimplement
            # the errorest for that)

    def storeSMTResult(self, tmpFolderSmt):
        # we create a folder with the current timestamp. In this folder all the
        # plots should be stored as files
        cwd = os.getcwd()
        os.chdir(tmpFolderSmt)
        # with
        # open(os.getcwd()+'/'+str(self.name)+'_'+str(self.boundingBox)[:20] +
        # '.txt', 'w') as file:
        with open(os.path.join(os.getcwd(), str(self.name) + '_' + str(self.boundingBox)[:20] + '.txt'), 'w') as file:
            json.dump(self.result, file, indent=0)
        os.chdir(cwd)
