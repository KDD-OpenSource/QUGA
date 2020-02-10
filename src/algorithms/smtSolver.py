from z3 import *
import numpy as np
import uuid
from itertools import product
import time

class smtSolver():
	def __init__(self, name, abstractConstr = None, numSolutions = 1, boundaryAroundSolution = 0.3):
		self.name = name
		self.id = uuid.uuid4()
		self.abstractConstr = abstractConstr
		self.variables = []
		self.aeConstr = []
		self.resultConstr = []
		self.customConstr = []
		self.numConstr = None
		self.netWeightMatrices = None
		self.netBiases = None
		self.satisfiable = None
		self.solver = Solver()
		self.numSolutions = numSolutions
		self.boundaryAroundSolution = boundaryAroundSolution
		# self.max_solution = True?

	# def construct_smt_solver(self, autoencoder):
	# 	self.constructAEMatrixBias(autoencoder)
	# 	for list, res in zip([self.variables, self.aeConstr], self.constructNetConstr('x')):
	# 		list.extend(res)
	# 	self.solver = Solver()
	# 	for elem in self.abstractConstr:
	# 		self.customConstr.extend(self.customConstrConstructer(elem))
	# 	self.solver.add(self.aeConstr)
	# 	self.solver.add(self.customConstr)
	# 	self.numConstr = len(self.solver.assertions())

	def addAEConstr(self, autoencoder):
		self.constructAEMatrixBias(autoencoder)
		for list, res in zip([self.variables, self.aeConstr], self.constructNetConstr('x')):
			list.extend(res)
		self.solver.add(self.aeConstr)
		self.numConstr = len(self.solver.assertions())

	def addCustomConstr(self):
		for elem in self.abstractConstr:
			self.customConstr.extend(self.customConstrConstructer(elem))
		self.solver.add(self.customConstr)
		self.numConstr = len(self.solver.assertions())


	def customConstrConstructer(self, abstractConstr):
		customConstrs = []
		if abstractConstr == 'adversAttack':
			customConstrs.extend(self.getAdversAttConstr(self.abstractConstr['adversAttack']['severity']))

			# TODO I think the outer 'And' is useless (though it does no harm) -> check that
			# orConstrs = []
			# for i in range(len(self.variables[0])):
			# 	orConstrs.extend([self.variables[0][i] - self.variables[len(self.variables)-1][i] > self.abstractConstr['adversAttack']['severity'],self.variables[len(self.variables)-1][i] - self.variables[0][i] > self.abstractConstr['adversAttack']['severity']])
			# customConstrs.append(Or(orConstrs))
		if abstractConstr == 'adversAttackPair':
			for list, res in zip([self.variables, customConstrs], self.constructNetConstr('y')):
				list.extend(res)
			firstSmtVars = [var for var in self.variables if str(var[0])[2] == '0']
			customConstrs.extend([Or(And(firstSmtVars[0][i] - firstSmtVars[1][i] < self.abstractConstr['adversAttackPair']['proximity'], firstSmtVars[0][i]-firstSmtVars[1][i] >= 0), And(firstSmtVars[1][i] - firstSmtVars[0][i]  < self.abstractConstr['adversAttackPair']['proximity'],firstSmtVars[1][i] -firstSmtVars[0][i] >= 0)) for i in range(len(firstSmtVars[0]))])

			# find out the number of layers by using only the self.variables
			allX = [x for x in self.variables if str(x[0])[0]=='x']
			largestLayer = max([int(str(x[0])[2]) for x in allX])
			lastLayerVars = [x for x in self.variables if str(x[0])[2] == str(largestLayer)]
			# TODO Insert the following as parameter into 'abstractConstr'
			# this is for 1 dimension having distance more than severity
			orConstrs = []
			for i in range(len(lastLayerVars[0])):
				orConstrs.extend([lastLayerVars[0][i] - lastLayerVars[1][i] > self.abstractConstr['adversAttackPair']['severity'], lastLayerVars[1][i] - lastLayerVars[0][i]  > self.abstractConstr['adversAttackPair']['severity']])
			customConstrs.append(Or(orConstrs))
			# this is for all the dimensions having distance more than severity
			# customConstrs.extend([Or(lastLayerVars[0][i] - lastLayerVars[1][i] > self.abstractConstr['adversAttackPair']['severity'], lastLayerVars[1][i] - lastLayerVars[0][i]  > self.abstractConstr['adversAttackPair']['severity']) for i in range(len(lastLayerVars[0]))])
		if abstractConstr == 'boundingBox':
			customConstrs.extend([And(self.variables[0][i] < self.abstractConstr['boundingBox'], self.variables[0][i] > -self.abstractConstr['boundingBox']) for i in range(len(self.variables[0]))])

						# 'customBoundingBox' : [[0,0.2],[0,0.2],[0,0.2],[0,0.2],[0,0.2],[0,0.2],[0,0.2],[0,0.2],[0,0.2],[0,0.2]]
		if abstractConstr == 'customBoundingBox':
			customConstrs.extend([And(self.variables[0][i] < self.abstractConstr['customBoundingBox'][i][1],self.variables[0][i] > self.abstractConstr['customBoundingBox'][i][0]) for i in range(len(self.variables[0]))])


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
		# TODO make solutions a list of dictionaries in which there are two fields: calcDuration and solution
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

	def calcMaxAdversAttack(self, startValue, accuracy):
		# Add all custom Constraints, but the adversAttack Constraints
		for elem in self.abstractConstr:
			if elem is not 'adversAttack':
				self.customConstr.extend(self.customConstrConstructer(elem))
		self.solver.add(self.customConstr)
		self.numConstr = len(self.solver.assertions())
		bestSmtSolution = None
		self.solver.push()
		adversAttConstr = self.getAdversAttConstr(startValue)
		self.solver.add(adversAttConstr)
		self.satisfiable = self.solver.check()
		severity = startValue
		severity_change = severity/2
		while(2*severity_change > accuracy):
			if self.satisfiable == unsat:
				severity = severity - severity_change
			else:
				severity = severity + severity_change
			severity_change = severity_change/2	
			self.solver.pop()
			self.solver.push()
			adversAttConstr = self.getAdversAttConstr(severity)
			self.solver.add(adversAttConstr)
			start = time.time()
			self.satisfiable = self.solver.check()
			end = time.time()
			calcDuration = end - start
			if self.satisfiable == sat:
				bestSmtSolution = {'model': self.solver.model(), 'calcDuration': calcDuration}
		return severity, [bestSmtSolution]

		# now I have a function that guarantees, that the resulting model is within a treshold of a bound.
		# TODO Add saving the existing maximum solution
		# Note that at the beginning we are (almost certainly) unsatisfiable



		# return maxSolution

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
