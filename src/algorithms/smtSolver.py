from z3 import *
import numpy as np
import uuid
import time
import json
import os
import shutil


class smtSolver():
    def __init__(self, name, abstractConstr=None, numSolutions=1,
                    boundaryAroundSolution=0.3):
        '''
        Forms an interface with the planet library to solve SMT formulas.

        name            --  the objects name
        id              --  the objects id
        abstractConstr  --  a list of abstract constraints such as boundingBox,
                            customBoundingBox, etc...
        variables       --  variables of the smt model. They correspond to nodes
                            in the neural net
        maxAdvesAttack  --  stores a list of algorithm, trainset and their
                            respective maxAdversAttacks
        folder          --  indicates the folder in which the smtResults are
                            saved
        '''
        self.name = name
        self.obj_id = uuid.uuid4()
        self.abstractConstr = abstractConstr
        self.variables = []
        self.maxAdversAttack = []
        self.folder = None
        self.Constr = []
        self.adversConstr = []

    def readAE(self, autoencoder):
        """ Read the autoencoders parameters and translates them to variables
        and constraints.
        """
        weightMatrix, bias = self.constructAEMatrixBias(autoencoder)
        self.variables.extend(self.constrNetVars('x', weightMatrix))
        self.addNetConstr(self.variables, weightMatrix, bias)

    def constrNetVars(self, varName, weightMatrix):
        """ Return variables used by smt Model and write them to smtSolver
        object
        """
        smtVars = []
        matrixLength = len(weightMatrix)
        for layer in range(matrixLength):
            smtVars.append(
                self.constrLayerVars(
                    varName,
                    layer,
                    weightMatrix
                    ))
        return smtVars

    def constrLayerVars(self, varName, layer, weightMatrix):
        """ Return the smt variables for one layer of the autoencoder
        """
        return  [
            Real(varName + '_' + str(layer) + '_' + str(i))
            for i in range(weightMatrix[layer].shape[0])
            ]

    def addNetConstr(self, smtVars, weightMatrix, bias):
        """ Write the net constraints of the autoencoder to the planet file
        ('ae_example.rlv')
        """
        matrixLength = len(weightMatrix)
        for layer in range(1, matrixLength - 1):
            for destNeuron in range(len(smtVars[layer])):
                self.addFixedConstr(
                    'ReLU',
                    weightMatrix,
                    bias,
                    destNeuron,
                    smtVars,
                    layer
                    )
        for destNeuron in range(len(smtVars[matrixLength - 1])):
            self.addFixedConstr(
                'Linear',
                weightMatrix,
                bias,
                destNeuron,
                smtVars
                )

    def addFixedConstr(self, varType, weightMatrix, bias,
                            destNeuron, smtVars, layer = -1):
        """ Writes one particular constraint to the file 'openFile'
        """
        if layer == -1:
            layer = len(weightMatrix)-1

        weightedSum = Sum([weightMatrix[layer][destNeuron][sourceNeuron] *
           smtVars[layer - 1][sourceNeuron] for sourceNeuron in range(len(smtVars[layer - 1]))])
        if varType == 'ReLU':
            self.Constr.append(smtVars[layer][destNeuron] == If(weightedSum +
                bias[layer - 1][destNeuron] < 0, 0, weightedSum +
                bias[layer - 1][destNeuron]))
        if varType == 'Linear':
            self.Constr.append(smtVars[layer][destNeuron] == weightedSum
                    + bias[layer-1][destNeuron])

    def constructAEMatrixBias(self, autoencoder):
        """ Return the autoencoders weight matrix and biases
        """
        netWeightMatrices = []
        netBiases = []
        localCount = 1
        for param in autoencoder.module.parameters():
            # the first layer of M is never really used. We just add it to have
            # the variables for the input layer
            if localCount == 1:
                netWeightMatrices.append(
                    np.random.normal(
                        size=(
                            param.size()[1],
                            param.size()[1]
                            )
                        )
                    )
                localCount = 2
            if len(param.size()) == 2:
                netWeightMatrices.append(param.detach().numpy())
            else:
                netBiases.append(param.detach().numpy())
        return netWeightMatrices, netBiases

    def readFolder(self, smtFolder):
        """ Save the folder in the smtModel
        """
        self.folder = smtFolder

    def addCustomConstr(self, exceptions=[]):
        """ write custom constraints into the planet file
        """
        for elem in self.abstractConstr:
            if elem not in exceptions:
                self.customConstrConstructer(elem)

    def customConstrConstructer(self, abstractConstr):
        """ Call the respective function for the respective abstract Constraint
        to write to planet file
        """
        if abstractConstr == 'adversAttack':
            self.setAdversAttConstr(
                self.abstractConstr['adversAttack']['severity']
                )
        if abstractConstr == 'boundingBox':
            self.addBoundingBoxConstr(
                self.abstractConstr['boundingBox']
                )
        if abstractConstr == 'customBoundingBox':
            self.addCustomBoundingBoxConstr(
                self.abstractConstr['customBoundingBox']
                )

    def getSatisfiability(self, z3Output):
        """ Return sat or unsat from planetOutput
        """
        if z3Output == sat:
            return 'SAT'
        elif z3Output == unsat:
            return 'UNSAT'
        else:
            raise Exception('z3Output is neither sat nor unsat.')

    def getMaxAdversAttack(self, startValue, accuracy, algorithm, trainDataset):
        """ Return the maximum adversarial attack (L_Infty Norm) for the given
        accuracy, algorithm and trainDataset
        """
        for maxAdversAttack in self.maxAdversAttack:
            if [algorithm, trainDataset] == maxAdversAttack['algTrainPair']:
                return maxAdversAttack
        self.addMaxAdversAttack(startValue, accuracy, algorithm, trainDataset)
        maxAdversAttackFiltered = [
            x for x in self.maxAdversAttack 
            if x['algTrainPair'] == [algorithm, trainDataset]
            ]
        return maxAdversAttackFiltered[0]

    def addMaxAdversAttack(self, startValue, accuracy, algorithm,
                            trainDataset):
        """ saves the maximum adversarial attack of a given algorithm and
        trainDataset to the smtSolver object. This prevents it from calculating
        it multiple times.
        """
        startFull = time.time()
        severity, currentBestSmtSolution = self.calcMaxAdversAttack(
            startValue,
            accuracy
            )
        endFull = time.time()
        calcTimeFull = endFull - startFull
        self.maxAdversAttack.append(
                {
                    'severity': severity,
                    'calcTime': calcTimeFull,
                    'smtModel': [currentBestSmtSolution],
                    'algTrainPair': [algorithm, trainDataset]
                }
            )

    def calcMaxAdversAttack(self, startValue, accuracy):
        """ Return the severity, the severity Change and the best Solution for
        the adversarial attack.
        """
        # Add all custom Constraints, but the adversAttack Constraints
        currentBestSmtSolution = None
        solver = Solver()
        solver.add(self.Constr)
        startValue, sat = self.getStartValueMaxAdvers(solver,
                startValue=startValue)
        # binSearchPair consists of severity and severityChange. They are stored
        # in such a way, so that they are mutable
        binSearchPair = [startValue, startValue/2]
        while(2 * binSearchPair[1] > accuracy or currentBestSmtSolution is None):
            z3Output, calcDuration, sat = self.binSearchStep(
                binSearchPair,
                sat,
                solver
                )
            if sat == 'SAT':
                currentBestSmtSolution = self.updateSolution(
                    z3Output,
                    calcDuration
                    )
        return binSearchPair[0], currentBestSmtSolution

    def binSearchStep(self, binSearchPair, sat, solver):
        """ Update the binSearchPair according to sat. Then return the output
        of planet along with new sat value and the duration of the calculation.
        """
        self.updateBinSearchPair(binSearchPair, sat)
        self.setAdversAttConstr(binSearchPair[0])
        start = time.time()
        z3Output = self.applyZ3ToAdvers(solver)
        sat = self.getSatisfiability(z3Output[0])
        print('checks model')
        print(binSearchPair[0])
        end = time.time()
        calcDuration = end - start
        return z3Output, calcDuration, sat


    def getStartValueMaxAdvers(self, solver, startValue=20):
        """ Return the start value along with its sat value for a maximum
        adversarial calculation.
        Should not be used from anywhere but within the class.
        """
        adversAttConstr = self.setAdversAttConstr(startValue)
        z3Output = self.applyZ3ToAdvers(solver)
        sat = self.getSatisfiability(z3Output[0])
        while (sat == 'SAT'):
            startValue = startValue * 2
            adversAttConstr = self.setAdversAttConstr(startValue)
            z3Output = self.applyZ3ToAdvers(solver)
            sat = self.getSatisfiability(z3Output[0])
        print(startValue)
        return startValue, sat

    def updateSolution(self, z3Output, calcDuration):
        """ Return the interpretation with the calculation duration of the new
        smt Solution
        """
        currentBestSmtSolution = {
            'model': self.getInterpretation(z3Output[1]),
            'calcDuration': calcDuration
            }
        return currentBestSmtSolution

    def updateBinSearchPair(self, binSearchPair, sat):
        """ Updates the binSearchPair consisting of severity and severityChange
        """
        if sat == 'UNSAT':
            binSearchPair[0] = binSearchPair[0] - binSearchPair[1]
        else:
            binSearchPair[0] = binSearchPair[0] + binSearchPair[1]
        binSearchPair[1] = binSearchPair[1] / 2

    def applyZ3ToAdvers(self, solver):
        """ Return the output of applying the planet solver to the planetFile
        """
        solver.push()
        solver.add(self.adversConstr)
        z3Output = solver.check()
        solver.pop()
        if z3Output == sat:
            z3Model = solver.model()
            return [z3Output, z3Model]
        else:
            return [z3Output]

    def addBoundingBoxConstr(self, boundingBox):
        """ Writes the bounding box constraints to the planet file
        """
        self.Constr.extend([And(self.variables[0][i] < boundingBox,
              self.variables[0][i] > -boundingBox) for i in range(len(self.variables[0]))])

    def addCustomBoundingBoxConstr(self, customBoundingBox):
        """ Writes the custom bounding box constraints to the planet file
        """
        for i in range(len(customBoundingBox)):
            if customBoundingBox[i][1] < customBoundingBox[i][0]:
                raise Exception('Your CustomBoundingBox is infeasible')
        self.Constr.extend([And(self.variables[0][i] < customBoundingBox[i][1],
                                  self.variables[0][i] > customBoundingBox[i][0]) for i in range(len(self.variables[0]))])

    def setAdversAttConstr(self, severity):
        """ Writes the adversarial attack constraints togethor with the already
        existing constraints into a new planet file called
        'ae_example_adversTmp'. This accounts for the iterating approach with
        binary search to obtain the maximum adversarial attack.
        """
        self.adversConstr = []
        orConstr = []
        for i in range(len(self.variables[0])):
            orConstr.extend([self.variables[0][i] -
                self.variables[len(self.variables) - 1][i] > severity,
                self.variables[len(self.variables) - 1][i] -
                self.variables[0][i] > severity])
        self.adversConstr.append(Or(orConstr))

    def getInterpretation(self, z3Output):
        """ Return the intepretation from the planet Output as a dictionary
        containing the variables and their respective value
        """
        sortedModel = sorted([(var, z3Output[var])
                              for var in z3Output], key=lambda x: str(x[0]))
        valuePairs = {}
        for elem in sortedModel:
            #if variable in str(elem[0]):
            numerator = elem[1].numerator_as_long()
            denominator = elem[1].denominator_as_long()
            decimal = float(numerator / denominator)
            valuePairs[str(elem[0])] = decimal
        return valuePairs

    # Miscellaneous functions
    def clearSmt(self):
        """ Clears the smt, so that we can reuse it on a different pair of
        algorithm and training set.
        """
        self.name = self.name
        self.obj_id = uuid.uuid4()
        self.abstractConstr = self.abstractConstr
        self.variables = []
        self.folder = None
        self.Constr = []
        self.adversConstr = []

    def saveSMTParameters(self, folder):
        """ saves the smt parameters into folder
        """
        smtDict = {}
        smtDict['name'] = str(self.__dict__['name'])
        smtDict['obj_id'] = str(self.__dict__['obj_id'])
        smtDict['abstractConstr'] = str(self.__dict__['abstractConstr'])
        with open(os.path.join(folder, 'parameters_smt.txt'), 'w') as jsonFile:
            json.dump(smtDict, jsonFile, indent=0)
