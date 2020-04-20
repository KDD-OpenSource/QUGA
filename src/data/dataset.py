import numpy as np
import pandas as pd
import os
import uuid
import json
import copy

class dataset():
	"""this is the superclass for Datasets"""
	def __init__(self, name, seed, purposeFlg, tsFlg, windowStep = 1, obj_id = None):
		self.name = name
		self.seed = seed
		if obj_id == None:
			self.obj_id = uuid.uuid4()
		else:
			self.obj_id = obj_id
		self.purposeFlg = purposeFlg
		self.tsFlg = tsFlg
		self.data = None
		self.windowStep = windowStep

	# NOTE THAT THE CHANGES HAPPEN INPLACE
	def boundedData(data: pd.DataFrame):
		columns = list(data)
		for col in columns:
			colMin = min(data[col])
			colMax = max(data[col])
			data[col] = (data[col] - colMin)/(colMax-colMin)
		return data
				

	def timeseriesToPoints(self, windowLength):
		if self.tsFlg is False:
			pass
		else:
			flattenedData = np.array(self.data).flatten()
			if (flattenedData.shape[0] - windowLength)%self.windowStep == 0:
				windows = [flattenedData[i*self.windowStep:i*self.windowStep+windowLength] for i in range(int((self.data.shape[0]-windowLength)/self.windowStep)+1)]
			else:
				raise Exception('Could not divide time series into autoencoder data, because windowLength, windowLength and the length of the Timeseries do not fit together.')
			self.data = pd.DataFrame(windows)
			self.tsFlg = False

	def pointsToTimeseries(self):
		# one could think about incorporating a window_step 
		# this function averages for each point in time over the windows
		if self.tsFlg is True:
			pass
		else:
			# largeMatrix = np.empty(shape =(self.data.shape[0]+windowLength - 1, self.data.shape[0]))
			windowLength = self.data.shape[1]
			if self.windowStep > windowLength:
				raise Exception('Your time window is shorter than the window step. You will end up with a TS with nan-values.')
			numWindows = self.data.shape[0]
			# largeMatrix = np.empty(shape =(numWindows, numWindows+windowLength-1))
			largeMatrix = np.empty(shape =(numWindows, windowLength + (numWindows-1) * self.windowStep))
			largeMatrix[:] = np.nan
			for i in range(numWindows):
				largeMatrix[i,i*self.windowStep:i*self.windowStep+windowLength] = self.data.iloc[i]

			timeseriesResult = np.nanmean(largeMatrix, axis = 0)
			self.data = pd.DataFrame(timeseriesResult)
			self.tsFlg = True

	def saveData(self, folder):
		# self.data.to_csv(folder + '/'+str(self.name) + '.csv')
		self.data.to_csv(os.path.join(folder, str(self.name) + '.csv'))
		dataDict = copy.deepcopy(self.__dict__)
		dataDict.pop('data')
		for key in list(dataDict.keys()):
			dataDict[key] = str(dataDict[key])
		# algorithmDictAdj['test_name'] = test_name
		if self.purposeFlg == 'train':
			# with open(folder + '/' + 'parameters_trainDataset.txt', 'w') as jsonFile:
			with open(os.path.join(folder, 'parameters_trainDataset.txt'), 'w') as jsonFile:
				json.dump(dataDict, jsonFile, indent = 0)
		elif self.purposeFlg == 'test':		
			# with open(folder + '/' + 'parameters_testDataset.txt', 'w') as jsonFile:
			with open(os.path.join(folder, 'parameters_testDataset.txt'), 'w') as jsonFile:
				json.dump(dataDict, jsonFile, indent = 0)
		else:
			# raise Exception(f'The purposeFlg of the dataset {self.data.name} is neither train nor test')
			raise Exception('The purposeFlg of the dataset is neither train nor test')
