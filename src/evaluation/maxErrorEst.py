import numpy as np
import pandas as pd
from .resultSMT import resultSMT
from ..utils import myUtils
from itertools import product
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
                while(time.time() < start + time_s):
                    numSamples, tmpMax = self.sampleUntilFixedTime(
                        numSamples,
                        algorithm,
                        tmpMax
                        )
                maxErrorEst = tmpMax
                self.result.append({'time': time_s,
                                    'maxErrorEst': maxErrorEst,
                                    'numSamples': numSamples})

    def sampleUntilFixedTime(self, numSamples, algorithm, tmpMax):
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
        # we create a folder with the current timestamp. In this folder all the
        # plots should be stored as files
        cwd = os.getcwd()
        os.chdir(tmpFolderSmt)
        with open(os.path.join(os.getcwd(), str(self.name) + '_' + str(self.boundingBox)[:20] + '.txt'), 'w') as file:
            json.dump(self.result, file, indent=0)
        os.chdir(cwd)
#import numpy as np
#import pandas as pd
## from .resultAE import resultAE
#from .resultSMT import resultSMT
#from ..utils import myUtils
#from itertools import product
#import os
#import json
#import time
#
## class maxErrorEst(resultSMT):
## 	"""This class estimates the maximum Error in a given box"""
## 	def __init__(self, boundingBox, sampleSizes, name ='maxErrorEst'):
## 		super(maxErrorEst, self).__init__(name)
## 		self.algorithm = None
## 		self.name = 'maxErrorEst'
## 		self.maxErrorEst = None
## 		self.result = None
## 		self.boundingBox = boundingBox
## 		self.sampleSizes = sampleSizes
#
#
#class maxErrorEst(resultSMT):
#    """This class estimates the maximum Error in a given box"""
#    # def __init__(self, sampleSizes, name ='maxErrorEst'):
#
#    def __init__(self, times_s, name='maxErrorEst'):
#        super(maxErrorEst, self).__init__(name)
#        self.algorithm = None
#        self.name = 'maxErrorEst'
#        self.maxErrorEst = None
#        self.result = None
#        self.boundingBox = None
#        # self.sampleSizes = sampleSizes
#        self.times_s = times_s
#
#    # def calcResult(self, algorithm, trainDataset, testDataset):
#    # 	self.algorithm = algorithm
#    # 	self.result = []
#    # 	for sampleSize in self.sampleSizes:
#    # 		start = time.time()
#    # 		uniformSample = np.random.uniform(low = np.array(self.boundingBox).transpose()[0], high = np.array(self.boundingBox).transpose()[1], size = (sampleSize,len(self.boundingBox)))
#    # 		prediction = np.array(algorithm.predict(pd.DataFrame(uniformSample)))
#    # 		maxErrorEst = np.square(np.subtract(uniformSample, prediction)).mean(axis=1).max()
#    # 		end = time.time()
#    # 		calcTime = end-start
#    # 		self.result.append({'sampleSize': sampleSize, 'calcTime': calcTime, 'maxErrorEst': maxErrorEst})
#        # ToDo: add a plot of that particular point (need to reimplement the
#        # errorest for that)
#
#    def calcResult(self, algorithm, trainDataset, smt):
#        if 'customBoundingBox' in smt.abstractConstr:
#            self.boundingBox = smt.abstractConstr['customBoundingBox']
#            self.algorithm = algorithm
#            self.result = []
#            # for time_s in self.times_s:
#            # 	start = time.time()
#            # 	numSamples = 0
#            # 	tmpMax = 0
#            # 	while(time.time() < start + time_s):
#            # 	# for sampleSize in self.sampleSizes:
#            # 		# uniformSample = np.random.uniform(low = np.array(self.boundingBox).transpose()[0], high = np.array(self.boundingBox).transpose()[1], size = (sampleSize,len(self.boundingBox)))
#            # 		uniformSample = np.random.uniform(low = np.array(self.boundingBox).transpose()[0], high = np.array(self.boundingBox).transpose()[1], size = (1,len(self.boundingBox)))
#            # 		numSamples = numSamples + 1
#            # 		prediction = np.array(algorithm.predict(pd.DataFrame(uniformSample)))
#            # 		maxErrorEst = np.square(np.subtract(uniformSample, prediction)).mean(axis=1).max()
#            # 		if maxErrorEst > tmpMax:
#            # 			tmpMax = maxErrorEst
#            # 	end = time.time()
#            # 	calcTime = end-start
#            # 	maxErrorEst = tmpMax
#            # 	self.result.append({'time': time_s, 'calcTime': calcTime, 'maxErrorEst': maxErrorEst, 'numSamples': numSamples})
#            start = time.time()
#            while(time.time() < start + self.times_s[-1]):
#                numSamples = 0
#                tmpMax = 0
#                tmpLInftyMax = 0
#                for time_s in self.times_s:
#                    while(time.time() < start + time_s):
#                        # for sampleSize in self.sampleSizes:
#                        # uniformSample = np.random.uniform(low = np.array(self.boundingBox).transpose()[0], high = np.array(self.boundingBox).transpose()[1], size = (sampleSize,len(self.boundingBox)))
#                        uniformSample = np.random.uniform(
#                            low=np.array(
#                                self.boundingBox).transpose()[0], high=np.array(
#                                self.boundingBox).transpose()[1], size=(
#                                1, len(
#                                    self.boundingBox)))
#                        numSamples = numSamples + 1
#                        prediction = np.array(
#                            algorithm.predict(
#                                pd.DataFrame(uniformSample)))
#                        maxErrorEst = np.square(
#                            np.subtract(
#                                uniformSample,
#                                prediction)).mean(
#                            axis=1).max()
#                        maxLInftyErrorEst = np.absolute(
#                            np.subtract(
#                                uniformSample,
#                                prediction)).max(
#                            axis=1).max()
#                        if maxErrorEst > tmpMax:
#                            tmpMax = maxErrorEst
#                        if maxLInftyErrorEst > tmpLInftyMax:
#                            tmpLInftyMax = maxLInftyErrorEst
#                    maxErrorEst = tmpMax
#                    maxLInftyErrorEst = tmpLInftyMax
#                    self.result.append({'time': time_s,
#                                        'maxErrorEst': maxErrorEst,
#                                        'maxLInftyErrorEst': maxLInftyErrorEst,
#                                        'numSamples': numSamples})
#                    # self.result.append({'time': time_s, 'calcTime': calcTime, 'maxErrorEst': maxErrorEst, 'numSamples': numSamples})
#
#                # end = time.time()
#                # calcTime = end-start
#                # maxErrorEst = tmpMax
#                # self.result.append({'time': time_s, 'calcTime': calcTime, 'maxErrorEst': maxErrorEst, 'numSamples': numSamples})
#    # def storeAEResult(self, folder, trainDataset,testDataset, algorithm, testName):
#    # # we create a folder with the current timestamp. In this folder all the plots should be stored as files
#    # 	cwd = os.getcwd()
#    # 	os.chdir(folder)
#    # 	with open(os.getcwd()+'/'+str(self.name)+'_'+str(self.boundingBox)[:20] + '.txt', 'w') as file:
#    # 	with open(os.path.join(os.getcwd(), str(self.name)+'_'+str(self.boundingBox)[:20] + '.txt'), 'w') as file:
#    # 		json.dump(self.result, file, indent = 0)
#    # 	os.chdir(cwd)
#    def storeSMTResult(self, tmpFolderSmt):
#        # we create a folder with the current timestamp. In this folder all the
#        # plots should be stored as files
#        cwd = os.getcwd()
#        os.chdir(tmpFolderSmt)
#        with open(os.path.join(os.getcwd(), str(self.name) + '_' + str(self.boundingBox)[:20] + '.txt'), 'w') as file:
#            json.dump(self.result, file, indent=0)
#        os.chdir(cwd)
