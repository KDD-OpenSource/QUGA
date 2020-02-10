"""
This file executes every experiment as specified by the lists 'algorithms', 'datasets', 'smts' and 'results'.
Furthermore it creates the respective folder-structure and thereafter stores the results.
"""

import os
import datetime
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import torch
from .myUtils import splitDatasets, createFolderStructure, storeAEResult, addFolder, loadParamsFromJson, saveSmtSolutions, splitResults, loadAE, storeSmtResult
from ..data.dataset import dataset
from ..algorithms.autoencoder import autoencoder
from ..algorithms.smtSolver import smtSolver
from itertools import product


def executeExperiments(
	settings,
	objects,
	):
	algorithms, trainDatasets, testDatasets, validationDatasets, smts, resultsAE, resultsSMT = decomposeObjects(objects)

	currentTime = datetime.datetime.now()
	runFolder = createFolderStructure(settings.seed)

	if settings.experimentScope == 'ae_smt' or settings.experimentScope == 'ae':
		resultFolders = []
		for algorithm, trainDataset, testDataset, resultAE in product(algorithms, trainDatasets, testDatasets, resultsAE):
			tmpFolderTrain, tmpFolderTest = addAEFolderstructure(runFolder, algorithm, trainDataset, testDataset)
			algorithm.trainAE(trainDataset)
			storeAEExperiment(algorithm, trainDataset, testDataset, resultAE, tmpFolderTrain, tmpFolderTest, settings)
			resultFolders.append(tmpFolderTest)

	if settings.experimentScope == 'ae_smt' or settings.experimentScope == 'smt':
		# go through all folders in result folders, 
		# maxAdversDict = []

		maxAdversDict = {'algorithm':[], 'maxAdversAttack':[]}
		for folder, smt, resultSMT in product(resultFolders, smts, resultsSMT):
			smt.clearSmt()
			# The current problem is, that we have one smt object for all of the AE, but we need to have different smts for each AE
			autoencoder = loadAE(folder)
			tmpFolderSmt = addFolder(folder, smt)
			resultSMT.getResult(autoencoder = autoencoder, trainData = None, testData = None, smt = smt)
			storeSmtResult(resultSMT, tmpFolderSmt)
			# maxAdversDict.append({'algorithm': autoencoder, 'maxAdversAttack': resultSMT.result})
			maxAdversDict['algorithm'].append(autoencoder)
			maxAdversDict['maxAdversAttack'].append(resultSMT.result)
			print('Autoencoder: {}'.format(autoencoder.architecture))

		plotArchitecture(maxAdversDict, runFolder)

		# AEArchitectures = [x.architecture for x in maxAdversDict['algorithm']]
		# y_pos = np.arange(len(AEArchitectures))
		# maxAdversAttacks = maxAdversDict['maxAdversAttack']
		# errors = [0.1 for i in range(len(maxAdversAttacks))]
		# plt.errorbar(y_pos, maxAdversAttacks, errors, linestyle='None')

		# # plt.bar(y_pos, maxAdversAttacks)
		# plt.xticks(y_pos, AEArchitectures)
		# plt.savefig(runFolder + '//'+'plot_with_errors.png')
		# plt.show()

		# TODO: store final error as result to be plotted



def decomposeObjects(objects):
	trainDatasets, testDatasets, validationDatasets = splitDatasets(objects[1])
	resultsAE, resultsSMT = splitResults(objects[3], 'ae', 'smt')

	return objects[0], trainDatasets, testDatasets, validationDatasets, objects[2], resultsAE, resultsSMT

def plotArchitecture(maxAdversDict, runFolder):
		AEArchitectures = [x.architecture for x in maxAdversDict['algorithm']]
		y_pos = np.arange(len(AEArchitectures))
		maxAdversAttacks = maxAdversDict['maxAdversAttack']
		errors = [0.1 for i in range(len(maxAdversAttacks))]
		plt.errorbar(y_pos, maxAdversAttacks, errors, linestyle='None')

		# plt.bar(y_pos, maxAdversAttacks)
		plt.xticks(y_pos, AEArchitectures)
		plt.savefig(runFolder + '//'+'plot_with_errors.png')

def addAEFolderstructure(runFolder, algorithm, trainDataset, testDataset):
	tmpFolderAlg = addFolder(runFolder, algorithm)
	tmpFolderTrain = addFolder(tmpFolderAlg, trainDataset)
	tmpFolderTest = addFolder(tmpFolderTrain, testDataset)
	return tmpFolderTrain, tmpFolderTest,

def storeAEExperiment(algorithm, trainDataset, testDataset, resultAE, tmpFolderTrain, tmpFolderTest, settings):
	trainDataset.saveData(tmpFolderTrain)
	testDataset.saveData(tmpFolderTest)
	algorithm.saveAE(tmpFolderTrain)
	storeAEResult(tmpFolderTest, trainDataset, testDataset, algorithm, resultAE, testName = settings.testName)
