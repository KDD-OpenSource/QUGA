from src.algorithms import autoencoder, smtSolver
from src.data import sineNoise, circleNoise
from src.evaluation import origReconTsPlot, origReconParallelPlot, origReconPairPlot, adversAttackPairQualPlot, maxAdversAttack, avgError, avgErrorArchPlot, maxAdversAttackArchPlot, maxAdversAttackQualPlot, latentSpaceSMTPlot, latentSpaceSMTPlot3D
import torch.nn as nn
import math
import uuid

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
			# [60,3,60],
			# [5,3,5],
			# [5,3,5],
			# [30,3,30],

			# [30,3,30],
			[10,3,10]
			# [15,5,15],
			# [15,5,15],
			# [15,5,15],
			# [15,5,15],
			# [15,5,15],
			# [15,5,15],
			# [15,5,15],
			# [15,5,15],
			# [30,3,30],
			# [30,3,30],
			# [30,3,30],
			# [30,3,30],
			# [30,3,30],
			# [30,3,30],
			# [30,3,30],
			# [30,3,30],
			# [30,3,30],

			# [30,5,30],
			# [30,5,30],
			# [30,5,30],
			# [30,5,30],
			# [30,5,30],
			# [30,5,30],
			# [30,5,30],
			# [30,5,30],
			# [30,5,30],
			# [30,5,30],
			# # [30,10,30],
			# [30,7,30],
			# [30,7,30],
			# [30,7,30],
			# [30,7,30],
			# [30,7,30],
			# [30,7,30],
			# [30,7,30],
			# [30,7,30],
			# [30,7,30],
			# [30,7,30],

			# [50,10,50],
			# [50,10,50],
			# [50,10,50],
			# [50,10,50],
			# [50,10,50],
			# [50,10,50],
			# [50,10,50],
			# [50,10,50]
			# [60,15,60]
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
			'length': [2500],
			'cycles': [50],
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
			'abstractConstr': [
				{
				'adversAttack': {'severity': 2},
				# 'adversAttackPair': {'proximity':0.2, 'severity': 0.3},
				# 'customBoundingBox' : [[0,0.2] for i in range(40)],
				'customBoundingBox' : [[math.sin((2*math.pi*x+0)/50)-0.01,math.sin((2*math.pi*x+0)/50)+0.01] for x in range(10)]
				# 'customBoundingBox' : [[-1,1] for i in range(60)],
				# 'customBoundingBox' : [[math.sin((2*math.pi*x+0)/125)-0.01,math.sin((2*math.pi*x)/125)+0.01] for x in range(60)]
				}
			,			
				{
				'adversAttack': {'severity': 2},
				'customBoundingBox' : [[-1,1] for i in range(10)]
				}
			# ,			
			# 	{
			# 	'adversAttack': {'severity': 10},
			# 	'customBoundingBox' : [[math.sin((2*math.pi*x+60)/50)-0.01,math.sin((2*math.pi*x+60)/50)+0.01] for x in range(50)]
			# 	}
			# ,			
			# 	{
			# 	'adversAttack': {'severity': 10},
			# 	'customBoundingBox' : [[math.sin((2*math.pi*x+90)/50)-0.01,math.sin((2*math.pi*x+90)/50)+0.01] for x in range(50)]
			# 	}
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
	maxAdversAttack(),
	avgError(),
	avgErrorArchPlot(),
	maxAdversAttackArchPlot(accuracy = 0.1),
	maxAdversAttackQualPlot(accuracy = 0.1),
	# latentSpaceSMTPlot3D(accuracy = 0.1),
	# latentSpaceSMTPlot(accuracy = 0.1)
	]	
	return results