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
	folderPathDate = os.getcwd() + '\\results\\' + str(currentTime.strftime("%Y.%m.%d"))
	createAndChangeWD(folderPathDate)	

	folderPathSeed = os.getcwd() + '\\' + str(seed)[:5]
	createAndChangeWD(folderPathSeed)

	return folderPathSeed



def storeAEResult(folder, trainDataset,testDataset, algorithm, result, testName):
	# we create a folder with the current timestamp. In this folder all the plots should be stored as files
	cwd = os.getcwd()

	os.chdir(folder)

	resultToBeSaved = result.getResult(algorithm, trainDataset, testDataset)
	if isinstance(resultToBeSaved, plt.Figure):
		resultToBeSaved.suptitle(f'Alg: {algorithm.name},\n Train-Dataset: {trainDataset.name}, \n Test-Dataset: {testDataset.name}')
		plt.savefig(os.getcwd()+'\\'+str(result.name))
		plt.close('all')
	elif isinstance(resultToBeSaved, pd.DataFrame):
		resultToBeSaved.to_csv(os.getcwd()+'\\'+str(result.name) + '.csv', header = False)
	else:
		print("Your result is not in the appropriate format, hence it did not get saved")
		#some other code
	if result.name  == 'pwDistance':
		sequencePlotPw = sequencePlotInd(seed = result.seed)
		pwDistFig = sequencePlotPw.getResult(algorithm, trainDataset, testDataset, resultToBeSaved.iloc[-1:,-2:])
		plt.savefig(os.getcwd() + '\\' + str('pwDistancePlot'))
		plt.close('all')

	os.chdir(cwd)

def pointsToTimeseries(points: np.array):
	# one could think about incorporating a window_step 
	# this function averages for each point in time over the windows
	if len(points.shape) != 2:
		raise Exception('Not clear how to produce the Timeseries, as the shape of the array is not like a matrix')
	else:
		# largeMatrix = np.empty(shape =(points.shape[0]+windowLength - 1, points.shape[0]))
		windowLength = points.shape[1]
		numWindows = points.shape[0]
		largeMatrix = np.empty(shape =(numWindows, numWindows+windowLength-1))
		largeMatrix[:] = np.nan
		for i in range(numWindows):
			largeMatrix[i,i:i+windowLength] = points[i]

		timeseriesResult = np.nanmean(largeMatrix, axis = 0)
		return pd.DataFrame(timeseriesResult)

def loadParamsFromJson(file):
	with open(file) as jsonFile:
		data = json.load(jsonFile)
	return data
	# print(data)

def saveSmtSolutions(solutions, tmpFolderSmt):
	if solutions == [None]:
		pass
	else:
		cwd = os.getcwd()
		os.chdir(tmpFolderSmt)
		file = './smtSolutions.csv'
		with open(file, 'w') as file:
			# file.write('Time used for calculation (in seconds): ')
			# file.write(str(timeForCalc))
			# file.write('\n')	
			solutionCount = 0
			for solution in solutions:
				solutionCount = solutionCount + 1
				file.write('Solution: {}'.format(solutionCount))
				file.write('Time used for calculation (in seconds): {}'.format(solution['calcDuration']))
				file.write('\n')
				for elem in solution['model']:
					file.write(str(elem))
					file.write(': ')
					numerator = solution['model'][elem].numerator_as_long()
					denominator = solution['model'][elem].denominator_as_long()
					decimal = float(numerator/denominator)
					file.write(str(decimal))
					file.write('\n')
				file.write('\n')
		os.chdir(cwd)


def splitResults(results, flg1, flg2):
	resultsAE = []
	resultsSmt = []
	for elem in results:
		if elem.aeSmtFlg == flg1:
			resultsAE.append(elem)
		elif elem.aeSmtFlg == flg2:
			resultsSmt.append(elem)
		else:
			raise Exception('Any result should belong a result type indicated by a given flg')

	return resultsAE, resultsSmt


def addFolder(folder, object):
	'''
	This function adds a new folder inside the folder 'folder' with the name given by 'object'. It then switches to the new folder and returns its value.	
	'''
	os.chdir(folder)
	newFolderPath = os.getcwd() + \
		'\\' + \
		object.name[:5] + '_' + str(object.id)[:5]
	if not os.path.exists(newFolderPath):
		os.mkdir(newFolderPath)
	os.chdir(newFolderPath)

	return newFolderPath


def loadAE(folder):
	cwd = os.getcwd()
	while 'autoencoder.pth' not in os.listdir():
		os.chdir('..')

	aeParameters = loadParamsFromJson('parameters.txt')
	modelAE = autoencoder(
		name = aeParameters['name'],
		seed = eval(aeParameters['seed']),
		architecture = eval(aeParameters['architecture']),
		bias = eval(aeParameters['bias']),
		# We are a little bit sloppy here, as we do not read torch.nn.ReLU() from the parameters file. In this particular situation that is ok, because SMT can only deal with ReLUs anyway
		activationFct = torch.nn.ReLU(),
		)

	modelAE.module.load_state_dict(torch.load('./autoencoder.pth'))
	return modelAE

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
	plt.savefig(os.getcwd()+'\\'+str(smtResult.name))
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