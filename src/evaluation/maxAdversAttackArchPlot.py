import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .resultSMT import resultSMT
from .maxAdversAttack import maxAdversAttack
from ..utils import myUtils
from itertools import product

class maxAdversAttackArchPlot(resultSMT):
	"""This class plots the reconstructed vs the original plot"""
	def __init__(self, name ='maxAdversAttackArchPlot', accuracy = 0.1):
		super(maxAdversAttackArchPlot, self).__init__(name)
		self.name = 'maxAdversAttackArchPlot'
		self.collResults = pd.DataFrame(columns = ['algorithm', 'trainDataset', 'smt','maxAdversAttack'])
		self.maxMaxAdversAttack = None
		self.result = None
		self.figures = None
		self.accuracy = accuracy

	def calcResult(self, algorithm, trainDataset, smt):
		maxAdversAttackTmp = maxAdversAttack(accuracy = self.accuracy)
		maxAdversAttackTmp.calcResult(algorithm, trainDataset, smt)
		resultToAppend = pd.DataFrame(columns = ['algorithm', 'trainDataset', 'smt', 'maxAdversAttack'], data = [[algorithm, trainDataset, smt, maxAdversAttackTmp.result]])
		self.collResults = self.collResults.append(resultToAppend)

	def storeSMTResult(self, folder):
		pass

	def calcCollectedSMTResults(self):
		self.figures = []
		# this is not good I think:
		# prune trainDataset list
		trainDatasets = []
		trainDataset_IDs = []
		for trainDataset in self.collResults['trainDataset']:
			if trainDataset.obj_id not in trainDataset_IDs:
				trainDatasets.append(trainDataset)
				trainDataset_IDs.append(trainDataset.obj_id)
		for trainDataset in trainDatasets:
			for smt in self.collResults['smt'].unique():
				maxMaxAdversAttack = self.calcMaxMaxAdversAttack()
				self.figures.append({'figure': self.calcCollectedSMTResult(trainDataset, smt, maxMaxAdversAttack), 'smt': smt, 'trainDataset': trainDataset})

	def calcCollectedSMTResult(self, trainDataset, smt, maxMaxAdversAttack):
		tmpDataFrame = self.collResults[(self.collResults['trainDataset'].apply(lambda x:x.obj_id) == trainDataset.obj_id)& (self.collResults['smt'].apply(lambda x:x.obj_id) == smt.obj_id)]
		AEArchitectures = sorted([x.architecture for x in tmpDataFrame['algorithm']])
		y_pos = np.arange(len(AEArchitectures))
		maxAdversAttacks = tmpDataFrame['maxAdversAttack'].values.tolist()
		fig = plt.figure(figsize = (20,10))
		errors = [self.accuracy for x in range(len(y_pos))]
		plt.errorbar(y_pos, maxAdversAttacks, errors, marker = '.')
		axes = plt.gca()
		axes.set_ylim([0,1.1*maxMaxAdversAttack])
		plt.xticks(y_pos, AEArchitectures, rotation = 90)
		return fig

	def storeCollectedSMTResults(self, runFolder):
		for figureDict in self.figures:
			self.storeCollectedSMTResult(runFolder, figureDict)

	def storeCollectedSMTResult(self, folder, figureDict):
		plt.figure(figureDict['figure'].number)
		trainDatasetName = figureDict['trainDataset'].name
		smtName = figureDict['smt'].obj_id
		figureDict['figure'].suptitle(f'Train-Dataset: {trainDatasetName}, SMT: {smtName}')
		plt.savefig(folder + '//'+'maxAdversAttack_'+str(figureDict['trainDataset'].obj_id)[:4]+'_'+str(figureDict['smt'].obj_id)[:4]+'_'+'.png')


	def calcMaxMaxAdversAttack(self):
		maxMaxAdversAttack = self.collResults['maxAdversAttack'].max()
		return maxMaxAdversAttack


	# I want the plot function to plot over all autoencoders with different architectures (that is we group by everything except by architecture)