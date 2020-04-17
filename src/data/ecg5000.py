from .dataset import dataset
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class ecg5000(dataset):
	"""docstring for ecg5000"""
	def __init__(self, name, seed, purposeFlg, length = -1, windowStep = 1):
		super(ecg5000, self).__init__(name = name, seed = seed, purposeFlg = purposeFlg, tsFlg = True, windowStep = windowStep)
		cwd = os.getcwd()
		os.chdir('./src/data/ExternalDatasets/ecg5000')
		if purposeFlg == 'train':
			for file in os.listdir():
				if 'TRAIN' in file:
					filename = file
		if purposeFlg == 'test':
			for file in os.listdir():
				if 'TEST' in file:
					filename = file
		data = pd.read_csv('./'+filename, header = None)
		# column 0 contains a class label
		data.drop(columns = [0], inplace = True)
		cleanedData = data.values.reshape(-1,1)
		if length == -1:
			lengthAdjustedData = cleanedData
		else:
			lengthAdjustedData = cleanedData[:length]			
		self.data = pd.DataFrame(lengthAdjustedData)
		os.chdir(cwd)