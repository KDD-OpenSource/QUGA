from .dataset import dataset
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

class eegWaves(dataset):
	"""docstring for eegWaves"""
	def __init__(self, name, seed, purposeFlg):
		super(eegWaves, self).__init__(name, seed, purposeFlg, tsFlg = False)
		cwd = os.getcwd()
		os.chdir('./src/data/ExternalDatasets/eegWaves')
		data = pd.read_csv('./EEG.csv', header = None, sep = ',')

		data.columns = data.columns.astype(str)
		columns = data.columns.values
		columns[14] = 'Class'
		data.columns = columns
		scaler = MinMaxScaler()
		dataScaled = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)
		# dataClass1 = dataNoNa[dataNoNa['Class'] == 1]
		# dataClass1WithoutClass = dataClass1.drop(columns = ['Class'])
		# cleanedData = dataClass1WithoutClass.values.reshape(-1,1)
		# lengthAdjustedData = cleanedData[:length]
		self.data = dataScaled.iloc[:,:14]
		os.chdir(cwd)