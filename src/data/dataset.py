import numpy as np
import pandas as pd
import os
import uuid
import json
import copy

class dataset():
	"""this is the superclass for Datasets"""
	def __init__(self, name, seed, purposeFlg, tsFlg, obj_id = None):
		self.name = name
		self.seed = seed
		if obj_id == None:
			self.obj_id = uuid.uuid4()
		else:
			self.obj_id = obj_id
		self.purposeFlg = purposeFlg
		self.tsFlg = tsFlg
		self.data = None

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
			windows = [flattenedData[i:i+windowLength] for i in range(self.data.shape[0]-windowLength+1)]
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
			numWindows = self.data.shape[0]
			largeMatrix = np.empty(shape =(numWindows, numWindows+windowLength-1))
			largeMatrix[:] = np.nan
			for i in range(numWindows):
				largeMatrix[i,i:i+windowLength] = self.data.iloc[i]

			timeseriesResult = np.nanmean(largeMatrix, axis = 0)
			self.data = pd.DataFrame(timeseriesResult)
			self.tsFlg = True

	def saveData(self, folder):
		self.data.to_csv(folder + '\\'+str(self.name) + '.csv')
		dataDict = copy.deepcopy(self.__dict__)
		dataDict.pop('data')
		for key in list(dataDict.keys()):
			dataDict[key] = str(dataDict[key])
		# algorithmDictAdj['test_name'] = test_name
		if self.purposeFlg == 'train':
			with open('parameters_trainDataset.txt', 'w') as jsonFile:
				json.dump(dataDict, jsonFile, indent = 0)
		elif self.purposeFlg == 'test':		
			with open('parameters_testDataset.txt', 'w') as jsonFile:
				json.dump(dataDict, jsonFile, indent = 0)
		else:
			raise Exception(f'The purposeFlg of the dataset {self.data.name} is neither train nor test')