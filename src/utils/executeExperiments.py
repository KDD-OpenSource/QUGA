"""
This file executes every experiment as specified by the lists 'algorithms', 'datasets', 'smts' and 'results'.
Furthermore it creates the respective folder-structure and thereafter stores the results.
"""

import os
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from .myUtils import splitDatasets, createFolderStructure, addFolder, loadParamsFromJson, loadAE, storeSmtResult, loadDataset
from ..data.dataset import dataset
from ..algorithms.autoencoder import autoencoder
from ..algorithms.smtSolver import smtSolver
from ..evaluation.resultAE import resultAE
from ..evaluation.resultSMT import resultSMT
from itertools import product


def executeExperiments(
	settings,
	objects,
	):
	algorithms, trainDatasets, testDatasets, validationDatasets, smts, resultsAE, resultsSMT = decomposeObjects(objects)
	runFolder = createFolderStructure(settings.seed)
	start = time.time()


	if settings.experimentScope == 'ae_smt' or settings.experimentScope == 'ae':
		# this executes all the experiments and calculates/stores the (single) results
		trainDatasetAEFolders = execAEExperiments(algorithms, trainDatasets, testDatasets, resultsAE, runFolder)
		# this calculates all the collected results
		for resultAE in resultsAE:
			if 'collResults' in resultAE.__dir__():
				resultAE.calcCollectedAEResults()
				resultAE.storeCollectedAEResults(runFolder)

	# print autoencoder weights
	for algorithm in algorithms:
		for layer in algorithm.module.encoder:
			if isinstance(layer, nn.Linear):
				print(layer.weight)
		for layer in algorithm.module.decoder:
			if isinstance(layer, nn.Linear):
				print(layer.weight)

	if settings.experimentScope =='smt':
		trainDatasetAEFolders = settings.resultFolders



	if settings.experimentScope == 'ae_smt' or settings.experimentScope == 'smt':
		execSMTExperiments(trainDatasetAEFolders, smts, resultsSMT)
		# this calculates all the collected results
		for resultSMT in resultsSMT:
			if 'collResults' in resultSMT.__dir__():
				resultSMT.calcCollectedSMTResults()
				resultSMT.storeCollectedSMTResults(runFolder)

	end = time.time()
	calcTime = end-start
	writeSettingsFile(settings, calcTime, runFolder)

def execAEExperiments(algorithms, trainDatasets, testDatasets, resultsAE, runFolder):
	trainDatasetAEFolders = []
	for algorithm in algorithms:
		trainDatasetAEFolders.extend(execFixedAlg(algorithm, trainDatasets, testDatasets, resultsAE, runFolder))
	return trainDatasetAEFolders

def execFixedAlg(algorithm, trainDatasets, testDatasets, resultsAE, runFolder):
	trainDatasetAEFolders = []
	for trainDataset in trainDatasets:
		tmpFolderTrain = addAEFolderstructure(runFolder, algorithm, trainDataset)
		algorithm.trainAE(trainDataset)
		storeTrainedAE(algorithm, trainDataset, tmpFolderTrain)
		trainDatasetAEFolders.append(tmpFolderTrain)
		execFixedTrainDataset(algorithm, trainDataset, testDatasets, resultsAE, tmpFolderTrain)
	return trainDatasetAEFolders

def execFixedTrainDataset(algorithm, trainDataset, testDatasets, resultsAE, tmpFolderTrain):
	for testDataset in testDatasets:
		tmpFolderTest = addFolder(tmpFolderTrain, testDataset)
		testDataset.saveData(tmpFolderTest)
		execFixedTestDataset(algorithm, trainDataset, testDataset, resultsAE, tmpFolderTest)

def execFixedTestDataset(algorithm, trainDataset, testDataset, resultsAE, tmpFolderTest):
	for resultAE in resultsAE:
		execFixedResultAE(algorithm, trainDataset, testDataset, resultAE, tmpFolderTest)

def execFixedResultAE(algorithm, trainDataset, testDataset, resultAE, tmpFolderTest):
	resultAE.calcResult(algorithm, trainDataset, testDataset)
	resultAE.storeAEResult(tmpFolderTest, trainDataset,testDataset, algorithm, testName = 'test')

def decomposeObjects(objects):
	trainDatasets, testDatasets, validationDatasets = splitDatasets(objects[1])
	resultsAE, resultsSMT = splitResults(objects[3])
	return objects[0], trainDatasets, testDatasets, validationDatasets, objects[2], resultsAE, resultsSMT

def addAEFolderstructure(runFolder, algorithm, trainDataset):
	tmpFolderAlg = addFolder(runFolder, algorithm)
	tmpFolderTrain = addFolder(tmpFolderAlg, trainDataset)
	return tmpFolderTrain

def storeTrainedAE(algorithm, trainDataset, tmpFolderTrain):
	trainDataset.saveData(tmpFolderTrain)
	algorithm.saveAE(tmpFolderTrain)

def splitResults(results):
	resultsAE = []
	resultsSmt = []
	for elem in results:
		if isinstance(elem, resultAE):
			resultsAE.append(elem)
		elif isinstance(elem, resultSMT):
			resultsSmt.append(elem)
		else:
			raise Exception('Any result should belong a result type indicated by a given flg')
	return resultsAE, resultsSmt

def execSMTExperiments(trainDatasetAEFolders, smts, resultsSMT):
	for folder in trainDatasetAEFolders:
		execFixedFolder(folder, smts, resultsSMT)

def execFixedFolder(folder, smts, resultsSMT):
	autoencoder = loadAE(folder)
	trainDataset = loadDataset(folder, 'trainDataset')
	for smt in smts:
		execFixedSMT(folder, smt, resultsSMT, autoencoder, trainDataset)

def execFixedSMT(folder, smt, resultsSMT, autoencoder, trainDataset):
	tmpFolderSmt = addFolder(folder, smt)
	smt.saveSMTParameters(tmpFolderSmt)
	for resultSMT in resultsSMT:
		execFixedResultSMT(smt, resultSMT, autoencoder, tmpFolderSmt, trainDataset)

def execFixedResultSMT(smt, resultSMT, autoencoder, tmpFolderSmt, trainDataset):
	smt.clearSmt()
	resultSMT.calcResult(algorithm = autoencoder, trainDataset = trainDataset,  smt = smt)
	resultSMT.storeSMTResult(tmpFolderSmt)
	print(f'Autoencoder: {autoencoder.architecture}')

def writeSettingsFile(settings, calcTime, folder):
	file = folder + '\\' + settings.testName + '.txt'
	with open(file, 'w') as file:
		file.write(f'This run took {calcTime} seconds.')
		file.write('\n')
		file.write(settings.description)

