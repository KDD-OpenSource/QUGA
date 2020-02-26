"""
This file contains the implementation of the Autoencoder model. 
The main_class (autoencoder in this case) contains information both about any parameter and the structure of the model. Furthermore it must implement the functions fit and predict. However it does not inherit directly from the nn.Module class. Instead there is the main_class_module, which is an object created by the main_class in the fit-function, which gives you the actual module.
"""

import math
import os
import torch
import torch.nn as nn
import torch.functional as F
import torch.optim as optim
from torch.autograd import Variable
from torch.utils.data import DataLoader
import numpy as np
import copy
import json
import pandas as pd
from .algorithm import algorithm


"""
Parameters to change:
-Activation Function {ReLU, Tanh, Sigmoid, Softmax}
-initialization Scheme {normal (uniformly in [-sqrt(k), sqrt(k)] for k = num(input_features), xavier_normal (glorot-bengio), 
	eye, ... }
-architecture
"""
class autoencoder(algorithm):
	def __init__(
		self, 
		name,
		seed,
		architecture,
		bias,
		lr = 0.0001,
		batchSize = 20,
		activationFct = nn.ReLU(),
		initialization = nn.init.xavier_normal_,
		epochs = 5):
		algorithm.__init__(self, name, seed, architecture, lr, batchSize, epochs)
		# self.seq_length = architecture[0]
		self.activationFct = activationFct
		self.initialization = initialization
		self.batchSize = batchSize
		self.bias = bias
		self.architecture = architecture
		self.module = autoencoderModule(self.architecture, self.bias, self.activationFct, self.initialization)

	def fit(self, data: pd.DataFrame):
		# for param in self.module.parameters():
		# 	print(param)
		# print(self.module.parameters().__dir__)
		data = data.values.astype(np.float32)
		dataTorch = torch.tensor(data)
		# self.module = autoencoderModule(self.architecture, self.bias, self.activationFct, self.initialization)
		optimizer = optim.Adam(self.module.parameters(), lr = self.lr)
		criterion = nn.MSELoss(size_average=None, reduce=None, reduction='mean')
		for j in range(self.epochs):
			epochLoss = 0
			for records in DataLoader(dataTorch, batch_size= self.batchSize):
				inputs = records
				optimizer.zero_grad()
				outputs = self.module(inputs)[1]
				loss = criterion(inputs, outputs)
				epochLoss = epochLoss + loss
				loss.backward()
				optimizer.step()
			print(j)
			print(epochLoss)


	# predict is supposed to return a pd.DataFrame as well
	def predict(self, data: pd.DataFrame):
		data = data.values.astype(np.float32)
		# Note, that we have to add [:,0,:], because we have a list (first :) of tensors. These tensors are of the form [[val_1,val_2,...]], because there is a wrapper in order to account for batch-calculation. With the '0' we get rid of this wrapper (as we are predicting one by one and not in batches)
		dataPredicted = np.array([self.module(record)[1].detach().numpy() for record in DataLoader(data)])[:,0,:]
		dataPredictedDf = pd.DataFrame(dataPredicted)
		return dataPredictedDf

	def getLatentSpace(self, data: pd.DataFrame):
		data = data.values.astype(np.float32)
		# dataTorch = torch.tensor(data)

		latentSpace = [self.module(record)[0] for record in DataLoader(data)]
		latentSpaceDF = pd.DataFrame([point.detach().numpy().flatten() for point in latentSpace])
		# return sequencesOutput
		return latentSpaceDF

	def getLatentSpaceDim(self):
		numLayers = len(self.architecture)
		return self.architecture[math.ceil(numLayers/2)-1]


	def trainAE(self, trainData):
		if trainData.tsFlg == True:
			# converts the timeseries_inplace to points
			trainData.timeseriesToPoints(windowLength = self.architecture[0])
			self.fit(trainData.data)
			# converts the points back to a timeseries
			trainData.pointsToTimeseries()
		else:
			self.fit(trainData.data)

	def saveAE(self, folder):
		'''
		This function stores an Autoencoder in the folder given by 'folder'. To this end it creates a new folder within 'folder' whose name is a combination of the name of the Autoencoder and its id. It then navigates to this folder, saves the Autoencoder there and returns the folder path
		'''
		cwd = os.getcwd()
		os.chdir(folder)
		# TODO: take care of the following problem:
		# We do not go into the folder 'folder', but we do so for 'save_data'
		torch.save(self.module.state_dict(), folder +  '\\autoencoder.pth')
		algorithmDictAdj = copy.deepcopy(self.__dict__)
		for key in list(algorithmDictAdj.keys()):
			algorithmDictAdj[key] = str(algorithmDictAdj[key])
		# algorithmDictAdj['test_name'] = test_name
		with open('parameters_algorithm.txt', 'w') as jsonFile:
			json.dump(algorithmDictAdj, jsonFile, indent = 0)

		os.chdir(cwd)



class autoencoderModule(nn.Module):
	def __init__(self, architecture, bias, activationFct, initialization):
		super(autoencoderModule, self).__init__()
		self.architecture = architecture
		self.activationFct = activationFct
		self.bias = bias
		self.initialization = initialization
		numLayers = len(self.architecture)
		encLayers = self.architecture[:math.ceil(numLayers/2)]
		decLayers = self.architecture[math.floor(numLayers/2):]
		seqEncLayers = [list(elem) for elem in list(zip(encLayers[:-1], encLayers[1:]))]
		seqDecLayers = [list(elem) for elem in list(zip(decLayers[:-1], decLayers[1:]))]
		encLayers = np.array([[nn.Linear(int(a), int(b), bias = self.bias), self.activationFct] for a, b in seqEncLayers]).flatten()
		decLayers = np.array([[nn.Linear(int(a), int(b), bias = self.bias), self.activationFct] for a, b in seqDecLayers]).flatten()[:-1]
		self.encoder = nn.Sequential(*encLayers)
		self.decoder = nn.Sequential(*decLayers)
		for layer in self.encoder:
			if isinstance(layer, nn.Linear):
				self.initialization(layer.weight)
		for layer in self.decoder:
			if isinstance(layer, nn.Linear):
				self.initialization(layer.weight)


	def forward(self, inputData):
		encoding = self.encoder(inputData)
		decoding = self.decoder(encoding)
		return (encoding, decoding)

