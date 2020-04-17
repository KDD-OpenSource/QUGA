import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .resultSMT import resultSMT
from .maxAdversAttack import maxAdversAttack
from ..utils import myUtils
from itertools import product

class maxAdversMovingBoxPlot(resultSMT):
	"""This class plots the reconstructed vs the original plot"""
	def __init__(self, name ='maxAdversMovingBoxPlot', accuracy = 0.1):
		super(maxAdversMovingBoxPlot, self).__init__(name)
		self.name = 'maxAdversMovingBoxPlot'
		self.collResults = pd.DataFrame(columns = ['algorithm', 'trainDataset', 'smtBBPosition','maxAdversAttack'])
		self.maxMaxAdversAttack = None
		self.result = None
		self.figures = None
		self.accuracy = accuracy
		# ToDo: customBoundingBox berechnen

	def calcResult(self, algorithm, trainDataset, smt):
		maxAdversAttackTmp = maxAdversAttack(accuracy = self.accuracy)
		maxAdversAttackTmp.calcResult(algorithm, trainDataset, smt)
		smtBBPosition = [(smt.abstractConstr['customBoundingBox'][i][1] + smt.abstractConstr['customBoundingBox'][i][0])/2 for i in range(len(smt.abstractConstr['customBoundingBox']))]
		smtBBDistToZero = np.sqrt(np.square(np.array([(smt.abstractConstr['customBoundingBox'][i][1] + smt.abstractConstr['customBoundingBox'][i][0])/2 for i in range(len(smt.abstractConstr['customBoundingBox']))])).sum())
		# print('smt_id: {}, smtBBPosition: {}'.format(smt.obj_id, smtBBPosition))
		# print(type(smtBBPosition))
		resultToAppend = pd.DataFrame(columns = ['algorithm', 'trainDataset', 'smtBBPosition', 'smtBBDistToZero','maxAdversAttack'], data = [[algorithm, trainDataset, smtBBPosition, smtBBDistToZero,maxAdversAttackTmp.AEError]])
		self.collResults = self.collResults.append(resultToAppend)

	def storeSMTResult(self, folder):
		pass

	def calcCollectedSMTResults(self):
		self.figures = []
		# this is not good I think:
		# prune trainDataset list
		trainDatasets = []
		trainDataset_IDs = []
		algorithms = []
		algorithm_IDs = []
		for trainDataset in self.collResults['trainDataset']:
			if trainDataset.obj_id not in trainDataset_IDs:
				trainDatasets.append(trainDataset)
				trainDataset_IDs.append(trainDataset.obj_id)
		for algorithm in self.collResults['algorithm']:
			if algorithm.obj_id not in algorithm_IDs:
				algorithms.append(algorithm)
				algorithm_IDs.append(algorithm.obj_id)

		for trainDataset in trainDatasets:
			for algorithm in algorithms:
				maxMaxAdversAttack = self.calcMaxMaxAdversAttack()
				self.figures.append({'figure': self.calcCollectedSMTResult(trainDataset, algorithm, maxMaxAdversAttack), 'algorithm': algorithm, 'trainDataset': trainDataset})

	def calcCollectedSMTResult(self, trainDataset, algorithm, maxMaxAdversAttack):
		# tmpDataFrame = self.collResults[(self.collResults['trainDataset'].apply(lambda x:x.obj_id) == trainDataset.obj_id)& (self.collResults['smt'].apply(lambda x:x.obj_id) == smt.obj_id)]
		tmpDataFrame = self.collResults[(self.collResults['trainDataset'].apply(lambda x:x.obj_id) == trainDataset.obj_id)& (self.collResults['algorithm'].apply(lambda x:x.obj_id) == algorithm.obj_id)]
		print(tmpDataFrame)
		# NOTE THAT WE DO NOT NEED TO SORT, AS IT COMES IN SORTED ALREADY!
		# tmpDataFrame.sort_values(by=['smtBBPosition'][2], inplace = True)
		print(tmpDataFrame)
		print(tmpDataFrame.shape[1])
		tmpDataFrame['interpolationIndex'] = range(tmpDataFrame.shape[0])
		# bbPosition = sorted(list(tmpDataFrame['smtBBPosition']))
		# print(bbPosition)
		# bbPositionProjectedRounded = [round(bbPosition[i][0],5) for i in range(len(bbPosition))]
		# print(bbPositionProjectedRounded)
		# fig = plt.figure(figsize = (20,10))
		# fig
		fig = tmpDataFrame.plot.line('interpolationIndex', 'maxAdversAttack', figsize = (20,10)).get_figure()
		# y_pos = np.arange(len(bbPosition))
		# maxAdversAttacks = tmpDataFrame['maxAdversAttack'].values.tolist()
		# plt.plot(y_pos, maxAdversAttacks, marker = '.')
		axes = plt.gca()
		axes.set_ylim([0,1.1*maxMaxAdversAttack])
		# plt.xticks(y_pos, bbPositionProjectedRounded, rotation = 90)
		return fig

	def storeCollectedSMTResults(self, runFolder):
		for figureDict in self.figures:
			self.storeCollectedSMTResult(runFolder, figureDict)

	def storeCollectedSMTResult(self, folder, figureDict):
		plt.figure(figureDict['figure'].number)
		# trainDatasetName = figureDict['trainDataset'].name
		# algName = figureDict['algorithm']
		# smtName = figureDict['smt'].obj_id
		# figureDict['figure'].suptitle(f'Train-Dataset: {trainDatasetName}, SMT: {smtName}')
		plt.savefig(folder + '//'+'maxAdversAttackMoving_'+str(figureDict['algorithm'].obj_id)[:4]+ '_' +str(figureDict['trainDataset'].obj_id)[:4]+'.png')
		# plt.savefig(folder + '//'+'maxAdversAttack_'+str(figureDict['trainDataset'].obj_id)[:4]+'_'+str(figureDict['smt'].obj_id)[:4]+'_'+'.png')


	def calcMaxMaxAdversAttack(self):
		maxMaxAdversAttack = self.collResults['maxAdversAttack'].max()
		return maxMaxAdversAttack


	# I want the plot function to plot over all autoencoders with different architectures (that is we group by everything except by architecture)