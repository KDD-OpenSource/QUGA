from z3 import *
# import z3solver
import numpy as np
import uuid
from itertools import product
import time
import json
import os

class smtSolver():
	def __init__(self, name, abstractConstr = None, numSolutions = 1, boundaryAroundSolution = 0.3):
		self.name = name
		self.obj_id = uuid.uuid4()
		self.abstractConstr = abstractConstr
		self.variables = []
		self.aeConstr = []
		self.resultConstr = []
		self.customConstr = []
		self.numConstr = None
		self.netWeightMatrices = None
		self.netBiases = None
		self.satisfiable = None
		# self.solver = Solver()
		self.solver = None
		self.numSolutions = numSolutions
		self.boundaryAroundSolution = boundaryAroundSolution
		self.maxAdversAttack = []
		self.maxSumAdversAttack = []

	def addAEConstr(self, autoencoder):
		self.constructAEMatrixBias(autoencoder)
		for list, res in zip([self.variables, self.aeConstr], self.constructNetConstr('x')):
			list.extend(res)
		self.solver.add(self.aeConstr)
		self.numConstr = len(self.solver.assertions())

	def addCustomConstr(self, exceptions = []):
		for elem in self.abstractConstr:
			if elem not in exceptions:
				self.customConstr.extend(self.customConstrConstructer(elem))
		self.solver.add(self.customConstr)
		self.numConstr = len(self.solver.assertions())


	def customConstrConstructer(self, abstractConstr):
		customConstrs = []
		if abstractConstr == 'adversAttack':
			customConstrs.extend(self.getAdversAttConstr(self.abstractConstr['adversAttack']['severity']))

		if abstractConstr == 'adversAttackPair':
			for list, res in zip([self.variables, customConstrs], self.constructNetConstr('y')):
				list.extend(res)
			firstSmtVars = [var for var in self.variables if str(var[0])[2] == '0']
			customConstrs.extend([Or(And(firstSmtVars[0][i] - firstSmtVars[1][i] < self.abstractConstr['adversAttackPair']['proximity'], firstSmtVars[0][i]-firstSmtVars[1][i] >= 0), And(firstSmtVars[1][i] - firstSmtVars[0][i]  < self.abstractConstr['adversAttackPair']['proximity'],firstSmtVars[1][i] -firstSmtVars[0][i] >= 0)) for i in range(len(firstSmtVars[0]))])

			allX = [x for x in self.variables if str(x[0])[0]=='x']
			largestLayer = max([int(str(x[0])[2]) for x in allX])
			lastLayerVars = [x for x in self.variables if str(x[0])[2] == str(largestLayer)]
			orConstrs = []
			for i in range(len(lastLayerVars[0])):
				orConstrs.extend([lastLayerVars[0][i] - lastLayerVars[1][i] > self.abstractConstr['adversAttackPair']['severity'], lastLayerVars[1][i] - lastLayerVars[0][i]  > self.abstractConstr['adversAttackPair']['severity']])
			customConstrs.append(Or(orConstrs))
		if abstractConstr == 'boundingBox':
			customConstrs.extend([And(self.variables[0][i] < self.abstractConstr['boundingBox'], self.variables[0][i] > -self.abstractConstr['boundingBox']) for i in range(len(self.variables[0]))])

						# 'customBoundingBox' : [[0,0.2],[0,0.2],[0,0.2],[0,0.2],[0,0.2],[0,0.2],[0,0.2],[0,0.2],[0,0.2],[0,0.2]]
		if abstractConstr == 'customBoundingBox':
			tmpSATProblem = Solver()
			tmpSATProblem.add([And(self.variables[0][i] < self.abstractConstr['customBoundingBox'][i][1],self.variables[0][i] > self.abstractConstr['customBoundingBox'][i][0]) for i in range(len(self.variables[0]))])
			if tmpSATProblem.check() == sat:
				customConstrs.extend([And(self.variables[0][i] < self.abstractConstr['customBoundingBox'][i][1],self.variables[0][i] > self.abstractConstr['customBoundingBox'][i][0]) for i in range(len(self.variables[0]))])
			else:
				raise Exception('Your Custom bounding box given by {} does not allow for a solution. Adjust it!'.format(tmpSATProblem.assertions()))
		return customConstrs

	def constructNetConstr(self, varName):
		smtVars = []
		matrixLength = len(self.netWeightMatrices)
		for layer in range(matrixLength):
			smtVars.append([Real(varName+'_' +str(layer)+'_'+str(i)) for i in range(self.netWeightMatrices[layer].shape[0])])
		Constr = []
		# for layer, destNeuron in product(range(1,matrixLength-1), range(len(smtVars[layer]))):
		for layer in range(1,matrixLength-1):
			for destNeuron in range(len(smtVars[layer])):
				weightedSum = Sum([self.netWeightMatrices[layer][destNeuron][sourceNeuron] * smtVars[layer-1][sourceNeuron] for sourceNeuron in range(len(smtVars[layer-1]))])
				Constr.append(smtVars[layer][destNeuron] == If(weightedSum + self.netBiases[layer-1][destNeuron] < 0, 0, weightedSum + self.netBiases[layer-1][destNeuron]))
		for destNeuron in range(len(smtVars[matrixLength-1])):
			weightedSum = Sum([self.netWeightMatrices[matrixLength-1][destNeuron][sourceNeuron] * smtVars[matrixLength-1-1][sourceNeuron] for sourceNeuron in range(len(smtVars[matrixLength-1-1]))])
			Constr.append(smtVars[matrixLength-1][destNeuron] == weightedSum + self.netBiases[matrixLength-2][destNeuron])
		return smtVars, Constr



	def constructAEMatrixBias(self, autoencoder):
		self.netWeightMatrices = []
		self.netBiases = []
		localCount = 1
		for param in autoencoder.module.parameters():
			# the first layer of M is never really used. We just add it to have the variables for the input layer
			if localCount == 1:
				self.netWeightMatrices.append(np.random.normal(size = (param.size()[1], param.size()[1])))
				localCount = 2
			if len(param.size()) == 2:
				self.netWeightMatrices.append(param.detach().numpy())
			else:
				self.netBiases.append(param.detach().numpy())

	def modelToPoint(self, variable):
		if self.satisfiable == sat:
			model = self.solver.model()
			sortedModel = sorted([(var, model[var]) for var in model], key = lambda x: str(x[0]))
			point = []
			for elem in sortedModel:
				if variable in str(elem[0]):
					numerator = elem[1].numerator_as_long()
					denominator = elem[1].denominator_as_long()
					decimal = float(numerator/denominator)
					point.append(decimal)
			return point

		elif self.satisfiable == unsat:
			raise Exception('Model is not satisfiable, hence we cannot convert the model to a point')
		elif self.satisfiable == None:
			raise Exception('You must first check the smt-model before you can convert the solution into a point')
		else:
			raise Exception('the variable \'satisfiable\' of the smt model does not have a valid value.')

	def calculateSolutions(self):
		solutions = []
		count = 0
		start = time.time()
		self.satisfiable = self.solver.check()
		end = time.time()
		calcDuration = end - start
		while self.satisfiable == sat and count < self.numSolutions:
			solutions.append({'model': self.solver.model(), 'calcDuration' : calcDuration})
			count = count + 1
			self.addSolutionConstr()
			start = time.time()
			if self.solver.check() == unsat:
				self.satisfiable = unsat
			end = time.time()
			calcDuration = end - start
		return solutions


	def addSolutionConstr(self):
		point = self.modelToPoint('x_0')
		# point is a vector of floats
		newConstr = [Or(self.variables[0][i] > point[i] + self.boundaryAroundSolution, self.variables[0][i] < point[i] - self.boundaryAroundSolution) for i in range(len(self.variables[0]))]
		self.resultConstr.extend(newConstr)
		self.solver.add(newConstr)
		print('New solution')

	def addAbstractConstraint(constraint):
		pass

	def getMaxAdversAttack(self, startValue, accuracy, algorithm, trainDataset):
		for maxAdversAttack in self.maxAdversAttack:
			if [algorithm, trainDataset] == maxAdversAttack['algTrainPair']:
				return maxAdversAttack
		self.calcMaxAdversAttack(startValue, accuracy, algorithm, trainDataset)
		maxAdversAttackFiltered = [x for x in self.maxAdversAttack if x['algTrainPair'] == [algorithm,trainDataset]]
		return maxAdversAttackFiltered[0]

	def calcMaxAdversAttack(self, startValue, accuracy, algorithm, trainDataset):
		# Add all custom Constraints, but the adversAttack Constraints
		# print('In the beginning of calcMaxAdversAttack the startValue is {}'.format(startValue))
		self.addCustomConstr(exceptions = ['adversAttack'])
		currentBestSmtSolution = None
		start = time.time()
		startValue = self.getStartValueMaxAdvers(startValue = startValue)
		severity = startValue
		severityChange = severity/2
		# print('After calculating the startValue severity is {}, severityChange is {} and satisfiable is {}'.format(severity, severityChange, self.satisfiable))

		while(2*severityChange > accuracy or currentBestSmtSolution == None):
			currentBestSmtSolution, severity, severityChange = self.updateMaxAdversAttack(severity, severityChange, currentBestSmtSolution)
		end = time.time()
		calcTime = end-start
		self.maxAdversAttack.append({'severity': severity, 'calcTime' : calcTime,'smtModel': [currentBestSmtSolution], 'algTrainPair': [algorithm, trainDataset]})

	def getStartValueMaxAdvers(self, startValue = 20):
		self.solver.push()
		adversAttConstr = self.getAdversAttConstr(startValue)
		self.solver.add(adversAttConstr)
		self.satisfiable = self.solver.check()
		while self.satisfiable == sat:
			startValue = startValue * 2
			# print('Raising the maxAdversAttack to {}'.format(startValue))
			self.solver.pop()
			self.solver.push()
			adversAttConstr = self.getAdversAttConstr(startValue)
			self.solver.add(adversAttConstr)
			self.satisfiable = self.solver.check()
			# print('checks model')
		print(startValue)
		return startValue

	def updateMaxAdversAttack(self, severity, severityChange, currentBestSmtSolution):
		# if currentBestSmtSolution == None:
			# print('currentBestSmtSolution is None')
		# else:
			# print('currentBestSmtSolution is not None')
		# print('At the beginning of updateMaxAdversAttack severity is {}, severityChange is {}.'.format(severity, severityChange))
		if self.satisfiable == unsat:
			severity = severity - severityChange
		else:
			severity = severity + severityChange
		severityChange = severityChange/2	
		self.solver.pop()
		self.solver.push()
		adversAttConstr = self.getAdversAttConstr(severity)
		self.solver.add(adversAttConstr)
		start = time.time()
		self.satisfiable = self.solver.check()
		print('checks model')
		print(severity)
		end = time.time()
		calcDuration = end - start
		if self.satisfiable == sat:
			currentBestSmtSolution = {'model': self.solver.model(), 'calcDuration': calcDuration}
		return currentBestSmtSolution, severity, severityChange

	def getAdversAttConstr(self, severity):
		# TODO I think the outer 'And' is useless (though it does no harm) -> check that
		customConstrs = []
		orConstrs = []
		for i in range(len(self.variables[0])):
			orConstrs.extend([self.variables[0][i] - self.variables[len(self.variables)-1][i] > severity,self.variables[len(self.variables)-1][i] - self.variables[0][i] > severity])
		customConstrs.append(Or(orConstrs))
		return customConstrs


	def clearSmt(self):
		self.name = self.name
		self.id = uuid.uuid4()
		self.abstractConstr = self.abstractConstr
		self.variables = []
		self.aeConstr = []
		self.resultConstr = []
		self.customConstr = []
		self.numConstr = None
		self.netWeightMatrices = None
		self.netBiases = None
		self.satisfiable = None
		self.solver = Solver()
		self.numSolutions = self.numSolutions
		self.boundaryAroundSolution = self.boundaryAroundSolution

	def saveSMTParameters(self, folder):
		smtDict = {}
		smtDict['name'] = str(self.__dict__['name'])
		smtDict['obj_id'] = str(self.__dict__['obj_id'])
		smtDict['abstractConstr'] = str(self.__dict__['abstractConstr'])
		with open(folder + '/'+ 'parameters_smt.txt', 'w') as jsonFile:
			json.dump(smtDict, jsonFile, indent = 0)


	def getSumAdversAttConstr(self, severity):
		customConstrs = []
		absValueSum = Sum([If(self.variables[0][i] - self.variables[len(self.variables)-1][i] > 0, self.variables[0][i] - self.variables[len(self.variables)-1][i], self.variables[len(self.variables)-1][i] - self.variables[0][i]) for i in range(len(self.variables[0]))])
		constr = (absValueSum > severity)
		customConstrs.append(constr)
		print(constr)
		# TEST THIS ONE
		return customConstrs

	def getMaxSumAdversAttack(self, startValue, accuracy, algorithm, trainDataset):
		for maxSumAdversAttack in self.maxSumAdversAttack:
			if [algorithm, trainDataset] == maxSumAdversAttack['algTrainPair']:
				return maxSumAdversAttack
		self.calcMaxSumAdversAttack(startValue, accuracy, algorithm, trainDataset)
		maxSumAdversAttackFiltered = [x for x in self.maxSumAdversAttack if x['algTrainPair'] == [algorithm,trainDataset]]
		return maxSumAdversAttackFiltered[0]

	def calcMaxSumAdversAttack(self, startValue, accuracy, algorithm, trainDataset):
		# Add all custom Constraints, but the adversAttack Constraints
		print('In the beginning of calcMaxSumAdversAttack the startValue is {}'.format(startValue))
		time.sleep(2)
		self.addCustomConstr(exceptions = ['sumAdversAttack'])
		currentBestSmtSolution = None
		startValue = self.getStartValueMaxSumAdvers(startValue = startValue)
		severity = startValue
		severityChange = severity/2
		print('For maxSum: After calculating the startValue severity is {}, severityChange is {} and satisfiable is {}'.format(severity, severityChange, self.satisfiable))
		time.sleep(2)
		while(2*severityChange > accuracy or currentBestSmtSolution == None):		
			time.sleep(2)
			currentBestSmtSolution, severity, severityChange = self.updateMaxSumAdversAttack(severity, severityChange, currentBestSmtSolution)
		self.maxSumAdversAttack.append({'severity': severity, 'smtModel': [currentBestSmtSolution], 'algTrainPair': [algorithm, trainDataset]})

	def getStartValueMaxSumAdvers(self, startValue = 20):
		self.solver.push()
		sumAdversAttConstr = self.getSumAdversAttConstr(startValue)
		self.solver.add(sumAdversAttConstr)
		self.satisfiable = self.solver.check()
		while self.satisfiable == sat:
			startValue = startValue * 2
			print('Raising the maxSumAdversAttack to {}'.format(startValue))
			self.solver.pop()
			self.solver.push()
			sumAdversAttConstr = self.getSumAdversAttConstr(startValue)
			self.solver.add(sumAdversAttConstr)
			self.satisfiable = self.solver.check()
			print('checks model')
		print(startValue)
		return startValue

	def updateMaxSumAdversAttack(self, severity, severityChange, currentBestSmtSolution):
		if currentBestSmtSolution == None:
			print('currentBestSmtSolution is None')
		else:
			print('currentBestSmtSolution is not None')
		print('At the beginning of updateMaxSumAdversAttack severity is {}, severityChange is {}.'.format(severity, severityChange))
		if self.satisfiable == unsat:
			severity = severity - severityChange
		else:
			severity = severity + severityChange
		severityChange = severityChange/2	
		self.solver.pop()
		self.solver.push()
		sumAdversAttConstr = self.getSumAdversAttConstr(severity)
		self.solver.add(sumAdversAttConstr)
		start = time.time()
		self.satisfiable = self.solver.check()
		print('checks model')
		print(severity)
		end = time.time()
		calcDuration = end - start
		if self.satisfiable == sat:
			currentBestSmtSolution = {'model': self.solver.model(), 'calcDuration': calcDuration}
		return currentBestSmtSolution, severity, severityChange
