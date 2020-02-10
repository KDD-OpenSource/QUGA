from src.algorithms import autoencoder, smtSolver
from src.data import sineNoise, circleNoise
from src.evaluation import origReconTsPlot, origReconParallelPlot, origReconPairPlot, adversAttackPairQualPlot, maxAdversAttack
import torch.nn as nn
import math

from itertools import product

def objectCreator(kwargs):
	objectDicts = []
	for elem in kwargs:
		for combinations in product(*elem["arguments"].values()):
			tempDict = dict(zip(elem["arguments"].keys(), combinations))
			combinationsStr = [str(elem).replace(' ','').replace('<function','')[:5] for elem in combinations]
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
			# works really well: [10,3,10]
			# [60,10,1,10,60], 
			# [60,10,2,10,60], 
			# [60,10,3,10,60], 
			# [60,10,4,10,60], 
			# [60,10,5,10,60], 
			# [60,10,6,10,60], 
			# TODO 2 - 15
			[60,1,60],
			[60,2,60],
			[60,3,60],
			[60,4,60],
			[60,5,60],
			[60,6,60],
			[60,7,60],
			[60,8,60],
			[60,9,60],
			[60,10,60]
			],
			'seed': [seed],
			'lr': [0.001],
			'bias': [True],
			'activationFct': [nn.ReLU()],
			'initialization': [nn.init.xavier_normal_],
			'batchSize' : [30],
			'epochs': [20]
			}
		}
	])
	return algorithms

def getDatasets(seed):
	datasets = objectCreator([
		{
		"objectType": sineNoise,
		"arguments":
			{	
			'seed': [seed],
			'purposeFlg': ['train','test'],
			'length': [2000],
			'cycles': [16],
			'var': [0.1],
			'bounded': [False],
			}
		}
	])
	return datasets

def getSmts():
	smts = objectCreator([
		{"objectType": smtSolver,
		"arguments":
			{
			# 'abstractConstr \in advers_attack{proximity, severity}, customBoundingBox(dimensionBounds), bounding_box(number))'
			# if for a certain result we need to dynamically change any given constraint, we present the starting values here
			'abstractConstr': [
				{
				'adversAttack': {'severity': 20},
				# 'adversAttackPair': {'proximity':0.2, 'severity': 1},
				# 'customBoundingBox' : [[0,0.2] for i in range(40)],
				'customBoundingBox' : [[-1,1] for i in range(60)],
				# 'customBoundingBox' : [[math.sin((2*math.pi*x+40)/125)-0.01,math.sin((2*math.pi*x+40)/125)+0.01] for x in range(60)]
				}
			],
			'numSolutions' : [5],
			'boundaryAroundSolution': [0.1],
			}
		}
		])
	return smts

def getResults():
	results = [
	origReconTsPlot(),
	# adversAttackPairQualPlot(),
	maxAdversAttack()
	]	
	return results