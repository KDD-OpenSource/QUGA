from src.algorithms import autoencoder, smtSolver
from src.data import sineNoise, twoSineNoise, circleNoise, smallKitchenAppliances, twoSineFrequenciesNoise, twoSineAmplitudesNoise, eegWaves, ecg5000, twoSineFrequenciesNoiseTest, sampleBoxTest
from src.evaluation import origReconTsPlot, origReconParallelPlot, origReconPairPlot, adversAttackPairQualPlot, maxAdversAttack, maxSumAdversAttack, avgError, avgErrorAEParamPlot, maxAdversAttackAEParamPlot, maxAdversAttackQualPlot, latentSpaceSMTPlot, latentSpaceSMTPlot3D, maxAdversGrowingBoxPlot, maxErrorEst, maxErrorEstAEParamPlot, joinedAEParamPlot, maxAdversAttackErrorEstAEParamPlot, theoMaxErrorEstAEParamPlot, maxAdversMovingBoxPlot, maxLInftyErrorEst, timeMaxErrorPlot
import torch.nn as nn
import math
import uuid
from itertools import product

algorithmInputLayerSize = 35
numberSineCycles = 50


sineclass_small = [[math.sin((2*math.pi*x)/(algorithmInputLayerSize)) - 0.1,math.sin((2*math.pi*x)/(algorithmInputLayerSize))+0.1] for x in range(algorithmInputLayerSize)]
sineclass_largeBeg = [[math.sin((2*math.pi*x)/(3*algorithmInputLayerSize)) - 0.1,math.sin((2*math.pi*x)/(3*algorithmInputLayerSize))+0.1] for x in range(algorithmInputLayerSize)]
sineclass_largeMid = [[math.sin((2*math.pi*x)/(3*algorithmInputLayerSize)) - 0.1,math.sin((2*math.pi*x)/(3*algorithmInputLayerSize))+0.1] for x in range(algorithmInputLayerSize,2*algorithmInputLayerSize)]
sineclass_largeEnd = [[math.sin((2*math.pi*x)/(3*algorithmInputLayerSize)) - 0.1,math.sin((2*math.pi*x)/(3*algorithmInputLayerSize))+0.1] for x in range(2*algorithmInputLayerSize,3*algorithmInputLayerSize)]


def objectCreator(kwargs):
	objectDicts = []
	for elem in kwargs:
		for combinations in product(*elem["arguments"].values()):
			tempDict = dict(zip(elem["arguments"].keys(), combinations))
			combinationsStr = [str(elem).replace(' ','').replace('<function','')[:5] for elem in combinations]
			# TODO If name already exists, take that name. Else make it the string
			tempName = str(elem["objectType"].__name__)[:5]+'_'+'_'.join(combinationsStr)
			tempDict['name'] = tempName
			objectDicts.append({'objectType': elem["objectType"], "arguments": tempDict})
	
	objects = []
	for elem in objectDicts:
		objects.append(elem["objectType"](**elem["arguments"]))
	return objects


def getAlgorithms(seed):
	algorithms = objectCreator([
		{"objectType": autoencoder,
		"arguments":
			{
			'architecture': [
			[algorithmInputLayerSize,5,algorithmInputLayerSize],
			],
			'seed': [seed],
			'lr': [0.001],
			'bias': [True],
			'activationFct': [nn.ReLU()],
			'initialization': [nn.init.xavier_normal_],
			'batchSize' : [30],
			'epochs': [100]
			}
		}
	])
	return algorithms

def getDatasets(seed):
	datasets = objectCreator([
		{
		"objectType": twoSineFrequenciesNoise,
		"arguments":
			{
			'seed': [seed],
			'purposeFlg': ['train','test'],
			'windowStep': [algorithmInputLayerSize],
			# 'numCycles0': [20,40,60,80,100,150,200,250,500],
			'numCycles0': [250],
			'cycleLength0': [3*algorithmInputLayerSize],
			'numCycles1': [500],
			'cycleLength1': [algorithmInputLayerSize],
			'var': [0.1]
			}
		},

		{
		"objectType": sampleBoxTest,
		"arguments":
			{
			'seed': [seed],
			'purposeFlg': ['test'],
			'box': [
			sineclass_small,
			sineclass_largeBeg,
			sineclass_largeMid,
			sineclass_largeEnd
			],
			'numPoints': [500]
			}
		}

	])
	return datasets

def getSmts():
	smts = objectCreator([
		{"objectType": smtSolver,
		"arguments":
			{
			'abstractConstr': [
			{
			'adversAttack': {'severity': 2},
			'customBoundingBox' : sineclass_small
			}, 
			{
			'adversAttack': {'severity': 2},
			'customBoundingBox' : sineclass_largeBeg
			}, 
			{
			'adversAttack': {'severity': 2},
			'customBoundingBox' : sineclass_largeMid
			}, 
			{
			'adversAttack': {'severity': 2},
			'customBoundingBox' : sineclass_largeEnd
			},
			],
			'numSolutions' : [5],
			'boundaryAroundSolution': [0.1],
			}
		}

		])
	return smts

def getResults():
	results = [
	# origReconTsPlot(numDataPoints = 700),
	# maxAdversAttack(accuracy = 0.025),
	# maxAdversAttackQualPlot(accuracy = 0.025),
	# avgError(),
	# maxLInftyErrorEst(times_s = [3,10]),
	# maxErrorEst(times_s = [10,20]),
	timeMaxErrorPlot(times_s = [60*1*i for i in range(1,181)])
	# timeMaxErrorPlot(times_s = [i for i in range(1,5)])
	# timeMaxErrorPlot(times_s = [1,2,3,4,5])
	]	
	return results