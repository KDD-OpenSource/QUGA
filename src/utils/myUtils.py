import pandas as pd
import datetime
import os
import copy
import json
import matplotlib.pyplot as plt
import torch
import numpy as np
from z3 import *
from ..algorithms.autoencoder import autoencoder
from ..data.dataset import dataset
# from ..evaluation.avgError import resultAE
# from ..evaluation.resultSMT import resultSMT

def splitDatasets(datasets):
	trainDatasets = []
	testDatasets = []
	validationDatasets = []
	for elem in datasets:
		if elem.purposeFlg == 'train':
			trainDatasets.append(elem)
		elif elem.purposeFlg == 'test':
			testDatasets.append(elem)
		elif elem.purposeFlg == 'validation':
			validationDatasets.append(elem)
		else:
			raise Exception('Each dataset must be either a test, a train or a validation set.')

	return trainDatasets, testDatasets, validationDatasets



# def creaFFolderStructure(trainDataset, testDataset, algorithm, time):
def createFolderStructure(seed):
	# make folders for seed and time, the rest will put into one folder for each run and done by a file
	currentTime = datetime.datetime.now()

	cwd = os.getcwd()
	print(cwd)
	folderPathDate = os.path.join(os.getcwd(), 'results', str(currentTime.strftime("%Y.%m.%d")))
	createAndChangeWD(folderPathDate)	

	folderPathSeed = os.path.join(os.getcwd(), str(seed)[:5])
	createAndChangeWD(folderPathSeed)

	return folderPathSeed


def pointsToTimeseries(points: np.array, windowStep = 1):
	# one could think about incorporating a window_step 
	# this function averages for each point in time over the windows
	if len(points.shape) != 2:
		raise Exception('Not clear how to produce the Timeseries, as the shape of the array is not like a matrix')
	else:
		# largeMatrix = np.empty(shape =(points.shape[0]+windowLength - 1, points.shape[0]))
		windowLength = points.shape[1]
		numWindows = points.shape[0]
		largeMatrix = np.empty(shape =(numWindows, windowLength + (numWindows-1) * windowStep))
		largeMatrix[:] = np.nan
		for i in range(numWindows):
			largeMatrix[i,i*windowStep:i*windowStep+windowLength] = points[i]
		timeseriesResult = np.nanmean(largeMatrix, axis = 0)
		return pd.DataFrame(timeseriesResult)



def loadParamsFromJson(file):
	with open(file) as jsonFile:
		data = json.load(jsonFile)
	return data
	# print(data)

# def saveSmtSolutions(solutions, tmpFolderSmt):
# 	if solutions == [None]:
# 		pass
# 	else:
# 		cwd = os.getcwd()
# 		os.chdir(tmpFolderSmt)
# 		file = './smtSolutions.csv'
# 		with open(file, 'w') as file:
# 			# file.write('Time used for calculation (in seconds): ')
# 			# file.write(str(timeForCalc))
# 			# file.write('\n')	
# 			solutionCount = 0
# 			for solution in solutions:
# 				solutionCount = solutionCount + 1
# 				file.write('Solution: {}'.format(solutionCount))
# 				file.write('Time used for calculation (in seconds): {}'.format(solution['calcDuration']))
# 				file.write('\n')
# 				for elem in solution['model']:
# 					file.write(str(elem))
# 					file.write(': ')
# 					numerator = solution['model'][elem].numerator_as_long()
# 					denominator = solution['model'][elem].denominator_as_long()
# 					decimal = float(numerator/denominator)
# 					file.write(str(decimal))
# 					file.write('\n')
# 				file.write('\n')
# 		os.chdir(cwd)


# def splitResults(results, flg1, flg2):
# 	resultsAE = []
# 	resultsSmt = []
# 	for elem in results:
# 		if elem.aeSmtFlg == flg1:
# 			resultsAE.append(elem)
# 		elif elem.aeSmtFlg == flg2:
# 			resultsSmt.append(elem)
# 		else:
# 			raise Exception('Any result should belong a result type indicated by a given flg')

# 	return resultsAE, resultsSmt
# def splitResults(results):
# 	resultsAE = []
# 	resultsSmt = []
# 	for elem in results:
# 		if isinstance(elem, resultAE):
# 			resultsAE.append(elem)
# 		elif isinstance(elem, resultSMT):
# 			resultsSmt.append(elem)
# 		else:
# 			raise Exception('Any result should belong a result type indicated by a given flg')

# 	return resultsAE, resultsSmt


def addFolder(folder, fold_object):
	'''
	This function adds a new folder inside the folder 'folder' with the name given by 'fold_object'. It then switches to the new folder and returns its value.	
	'''
	# os.chdir(folder)
	# print(folder)
	# print(fold_object)
	newFolderPath = os.path.join(folder, fold_object.name[:5] + '_' + str(fold_object.obj_id)[:5])
	try:
	   if not os.path.exists(newFolderPath):
	       os.makedirs(newFolderPath)
	except OSError as err:
	   print(err)


	# if not os.path.exists(newFolderPath):
	# 	os.mkdir(newFolderPath)
	# os.chdir(newFolderPath)

	return newFolderPath


def loadAE(folder):
	aeParameters = loadAEParam(folder)
	modelAE = autoencoder(
		name = aeParameters['name'],
		seed = eval(aeParameters['seed']),
		architecture = eval(aeParameters['architecture']),
		bias = eval(aeParameters['bias']),
		obj_id = aeParameters['obj_id'],
		# We are a little bit sloppy here, as we do not read torch.nn.ReLU() from the parameters file. In this particular situation that is ok, because SMT can only deal with ReLUs anyway
		activationFct = torch.nn.ReLU(),
		)
	loadAEState(folder, modelAE)
	return modelAE

def loadAEParam(folder):
	while 'autoencoder.pth' not in os.listdir(folder):
		# folder = folder[:folder.rfind('/')]
		folder = os.path.dirname(folder)
	aeParameters = loadParamsFromJson(os.path.join(folder, 'parameters_algorithm.txt'))
	return aeParameters	

# def loadAEState(folder, autoencoder):
# 	cwd = os.getcwd()
# 	os.chdir(folder)
# 	while 'autoencoder.pth' not in os.listdir():
# 		os.chdir('..')
# 	autoencoder.module.load_state_dict(torch.load('./autoencoder.pth'))
# 	os.chdir(cwd)
def loadAEState(folder, autoencoder):
	while 'autoencoder.pth' not in os.listdir(folder):
		# folder = folder[:folder.rfind('/')]
		folder = os.path.dirname(folder)
	autoencoder.module.load_state_dict(torch.load(os.path.join(folder,'autoencoder.pth')))

def loadDataset(folder, datasetType: str):
	datasetParams = loadDatasetParams(folder, datasetType) 	
	datasetInstance = dataset(
		name = datasetParams['name'],
		seed = eval(datasetParams['seed']),
		obj_id = datasetParams['obj_id'],
		purposeFlg = datasetParams['purposeFlg'],
		tsFlg = eval(datasetParams['tsFlg'])
		)
	loadData(folder, datasetInstance)
	return datasetInstance

def loadData(folder, datasetInstance):
	fileName = datasetInstance.name + '.csv'
	while fileName not in os.listdir(folder):
		# folder = folder[:folder.rfind('/')]
		folder = os.path.dirname(folder)
	datasetInstance.data = pd.read_csv(os.path.join(folder, fileName), header = 0, index_col = 0)

def loadDatasetParams(folder, datasetType: str):
	fileName = 'parameters_'+datasetType+'.txt'
	while fileName not in os.listdir(folder):
		# folder = folder[:folder.rfind('/')]
		folder = os.path.dirname(folder)
	datasetParams = loadParamsFromJson(os.path.join(folder, fileName))
	return datasetParams



def storeSmtResult(smtResult, tmpFolderSmt):
	# wrapper for different store functions depending on type of smtResult
	if smtResult.name == 'adversAttackPairQualPlot':
		storeAdvAttPairResult(smtResult, tmpFolderSmt)
	if smtResult.name == 'maxAdversAttack':
		storeMaxAdvAtt(smtResult, tmpFolderSmt)
	pass

def storeAdvAttPairResult(smtResult, tmpFolderSmt):
	# here smtResult is a figure
	saveSmtSolutions(smtResult.smtSolutions, tmpFolderSmt)
	plt.figure = smtResult.result
	# plt.savefig(os.getcwd()+'/'+str(smtResult.name))
	plt.savefig(os.path.join(os.getcwd(), str(smtResult.name)))
	plt.close('all')

def storeMaxAdvAtt(smtResult, tmpFolderSmt):
	saveSmtSolutions(smtResult.smtSolutions, tmpFolderSmt)
	file = './maxAdversAttackSeverity.csv'
	with open(file, 'w') as file:
		file.write('\n')
		file.write('The severity of this solution is: {}'.format(smtResult.result))

def solutionsToPoints(smtSolutions, smtVar):
	if smtSolutions == None or smtVar == None:
		return None
	else:
		smtSolutionModels = [smtSolution['model'] for smtSolution in smtSolutions]
		points = []
		for solution in smtSolutionModels:
			solPoint = []
			sortedSolution = sorted([(variable, solution[variable]) for variable in solution], key = varKeyFunc)
			for var in smtVar:
				varPoint = []
				for elem in sortedSolution:
					if var in str(elem[0]):
						numerator = elem[1].numerator_as_long()
						denominator = elem[1].denominator_as_long()
						decimal = float(numerator/denominator)
						varPoint.append(decimal)
				solPoint.append(varPoint)
			points.append(solPoint)
		return points

def varKeyFunc(smtVar):
	tmp = str(smtVar[0]).split('_')
	return (str(tmp[0]), int(tmp[1]), int(tmp[2]))

def createAndChangeWD(folder):
	if not os.path.exists(folder):
		os.mkdir(folder)
	os.chdir(folder)



def test_AE_SMTSolution(autoencoder, resultSMT):
	smtSolutions = resultSMT.smtSolutions
	points = solutionsToPoints(smtSolutions, ['x_0','x_1', 'x_2'])
	print(points)
	pointsDF = pd.DataFrame(points[0][0]).transpose()
	print(pointsDF)
	autoencoderSolution = autoencoder.getAEResults(pointsDF)
	print(autoencoderSolution)
