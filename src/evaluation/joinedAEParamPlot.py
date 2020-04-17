import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from .resultJoined import resultJoined
from itertools import product

class joinedAEParamPlot(resultJoined):
	"""This class joins all the archplot from already existing ones"""
	def __init__(self, AEParam,name = 'joinedAEParamPlot'):
		super(joinedAEParamPlot, self).__init__(name)
		self.name = name
		self.allCollResults = pd.DataFrame(columns = ['algorithmId', 'trainDatasetId','AEParam'])
		self.figures = None
		self.AEParam = AEParam

	def calcResult(self, resultsAE, resultsSMT):
		for result in resultsAE + resultsSMT:
			if result.name in ['maxAdversAttackAEParamPlot', 'avgErrorAEParamPlot', 'maxErrorEstAEParamPlot', 'maxAdversAttackErrorEstAEParamPlot', 'theoMaxErrorEstAEParamPlot']:
				tmpResult = result.getCollResults()
				if result.name == 'maxErrorEstAEParamPlot':
					sampleSize = str(tmpResult['sampleSize'].iloc[0])
					boundingBox = str(tmpResult['boundingBox'].iloc[0][0])
					maxErrorEstCol = str('maxErrorEstAEParamPlot'+'_'+boundingBox +'_'+ sampleSize)
					tmpResult[maxErrorEstCol] = tmpResult['maxErrorEst']
				tmpResult['algorithmId'] = tmpResult['algorithm'].apply(lambda x: str(x.obj_id))
				tmpResult['AEParam'] = tmpResult['algorithm'].apply(lambda x: str(x.__dict__[self.AEParam]))
				tmpResult['trainDatasetId'] = tmpResult['trainDataset'].apply(lambda x: str(x.obj_id))
				self.allCollResults = pd.merge(self.allCollResults,tmpResult, on = ['algorithmId','trainDatasetId', 'AEParam'], how= 'outer')
		print(self.allCollResults)

		self.figures = []
		for trainDatasetId in self.allCollResults['trainDatasetId'].unique():
			tmpDataFrame = self.allCollResults[self.allCollResults['trainDatasetId'] == trainDatasetId]
			self.figures.append({'trainDatasetId': trainDatasetId, 'figure': self.calcJoinedResult(trainDatasetId, tmpDataFrame)})

	def calcJoinedResult(self, trainDataset, tmpDataFrame):
		# if 'algorithm' in tmpDataFrame.columns:
		# 	AEParams = sorted([x.architecture for x in tmpDataFrame['algorithm']])
		# else:
		# 	AEParams = sorted([x.architecture for x in tmpDataFrame['algorithm_x']])
		AEParams = sorted([x for x in tmpDataFrame['AEParam']])
		import pdb; pdb.set_trace()
		y_pos = np.arange(len(AEParams))
		fig = plt.figure(figsize = (20,10))
		plt.xticks(y_pos, AEParams, rotation = 90)
		currentMax = 0
		for metric in tmpDataFrame.columns:
			# for substring in ['maxAdversAttack', 'avgError', 'maxErrorEstArch', 'maxAdversAttackErrorEst', 'theoMaxErrorEst']:
			for substring in ['avgError', 'maxErrorEstAEParam', 'maxAdversAttackErrorEstAEParam', 'theoMaxErrorEst']:
				if substring in metric:
					print('substring: {}, metric: {}'.format(substring, metric))
			# if metric.strip('_x').strip('_y') in ['maxAdversAttack', 'avgError', 'maxErrorEst']:

					metricValues = tmpDataFrame[metric].values.tolist()
					print('metricValue: {}, currentMax: {}'.format(metricValues, currentMax))

					plt.plot(y_pos, metricValues, marker = '.', label = metric)
					if max(metricValues) > currentMax:
						axes = plt.gca()
						currentMax = max(metricValues)
						axes.set_ylim([0,1.1*currentMax])

		plt.legend(loc='best')

		return fig
		# we should have a new plot for every combination of trainDataset and Autoencoder
		# also for different testSets, we should have new plots

	def storeJoinedResults(self, runFolder):
		print(self.figures)
		for figureDict in self.figures:
			self.storeJoinedResult(runFolder, figureDict)

	def storeJoinedResult(self, folder, figureDict):
		plt.figure(figureDict['figure'].number)
		trainDatasetId = figureDict['trainDatasetId']
		plt.savefig(folder + '//'+'joinedResult'+'_'+str(trainDatasetId)[:5]+'.png')
