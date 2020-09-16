from src.algorithms import autoencoder, smtSolver
from src.data import ecg5000, sampleBoxTest
from src.evaluation import origReconTsPlot, maxAdversAttack, avgError, maxAdversAttackQualPlot, timeMaxErrorPlot
import torch.nn as nn
import math
import uuid
from itertools import product

algorithmInputLayerSize = 35
numberSineCycles = 50

# Boxes:
class0_0_35_bottom = [
    [0.75, 1.25], [-1.01, -0.51], [-2.71, -2.21], [-3.63, -3.13], [-4.23,
        -3.73], [-4.15, -3.65], [-3.60, -3.10], [-2.62, -2.12], [-1.91, -1.41],
    [-1.44, -0.94], [-0.91, -0.41], [-0.56, -0.06], [-0.49, 0.01], [-0.46,
        0.04], [-0.46, 0.04], [-0.48, 0.02], [-0.40, 0.10], [-0.36, 0.14],
    [-0.40, 0.10], [-0.43, 0.07], [-0.44, 0.06], [-0.43, 0.07], [-0.47, 0.03],
    [-0.51, -0.01], [-0.52, -0.02], [-0.54, -0.04], [-0.57, -0.07], [-0.58,
        -0.08], [-0.61, -0.11], [-0.62, -0.12], [-0.63, -0.13], [-0.68, -0.18],
    [-0.74, -0.24], [-0.77, -0.27], [-0.78, -0.28]
    ]
class0_36_70_bottom = [
    [-0.78, -0.28], [-0.78, -0.28], [-0.84, -0.34], [-0.82, -0.32], [-0.78,
        -0.28], [-0.75, -0.25], [-0.67, -0.17], [-0.64, -0.14], [-0.57, -0.07],
    [-0.46, 0.04], [-0.39, 0.11], [-0.36, 0.14], [-0.31, 0.19], [-0.29, 0.21],
    [-0.23, 0.27], [-0.15, 0.35], [-0.16, 0.34], [-0.20, 0.30], [-0.21, 0.29],
    [-0.20, 0.30], [-0.22, 0.28], [-0.20, 0.30], [-0.18, 0.32], [-0.15, 0.35],
    [-0.15, 0.35], [-0.15, 0.35], [-0.13, 0.37], [-0.08, 0.42], [-0.09, 0.41],
    [-0.11, 0.39], [-0.06, 0.44], [0.01, 0.51], [-0.03, 0.47], [0.01, 0.51],
    [0.09, 0.59]
    ]
class0_71_105_up = [ 
    [ 0.12, 0.62], [ 0.13, 0.63], [ 0.14, 0.64], [ 0.17, 0.67], [ 0.21, 0.71],
    [ 0.25, 0.75], [ 0.25, 0.75], [ 0.27, 0.77], [ 0.26, 0.76], [ 0.27, 0.77],
    [ 0.28, 0.78], [ 0.21, 0.71], [ 0.19, 0.69], [ 0.20, 0.70], [ 0.15, 0.65],
    [ 0.06, 0.56], [ 0.09, 0.59], [ 0.14, 0.64], [ 0.16, 0.66], [ 0.12, 0.62],
    [ 0.09, 0.59], [ 0.07, 0.57], [ 0.03, 0.53], [ 0.08, 0.58], [ 0.12, 0.62],
    [ 0.19, 0.69], [ 0.28, 0.78], [ 0.38, 0.88], [ 0.46, 0.96], [ 0.58, 1.08],
    [ 0.76, 1.26], [ 0.96, 1.46], [ 1.13, 1.63], [ 1.24, 1.74], [ 1.27, 1.77]
    ]
class0_106_140_up = [
    [1.27, 1.77], [1.25, 1.75], [1.13, 1.63], [0.98, 1.48], [0.80, 1.30],
    [0.59, 1.09], [0.34, 0.84], [0.08, 0.58], [-0.11, 0.39], [-0.18, 0.32],
    [-0.25, 0.25], [-0.32, 0.18], [-0.41, 0.09], [-0.44, 0.06], [-0.42, 0.08],
    [-0.42, 0.08], [-0.46, 0.04], [-0.54, -0.04], [-0.54, -0.04], [-0.44,
        0.06], [-0.46, 0.04], [-0.42, 0.08], [-0.39, 0.11], [-0.33, 0.17],
    [-0.08, 0.42], [0.34, 0.84], [0.64, 1.14], [0.73, 1.23], [0.80, 1.30],
    [0.77, 1.27], [0.54, 1.04], [0.29, 0.79], [0.20, 0.70], [0.11, 0.61],
    [0.12, 0.62]
    ]
class1_0_35_up = [
    [1.75, 2.25], [-0.47, 0.03], [-1.29, -0.79], [-1.82, -1.32], [-2.51,
        -2.01], [-2.74, -2.24], [-2.82, -2.32], [-2.67, -2.17], [-2.40, -1.90],
    [-1.98, -1.48], [-1.55, -1.05], [-1.26, -0.76], [-1.01, -0.51], [-0.74,
        -0.24], [-0.49, 0.01], [-0.29, 0.21], [-0.13, 0.37], [-0.01, 0.49],
    [0.05, 0.55], [0.07, 0.57], [0.10, 0.60], [0.09, 0.59], [0.07, 0.57],
    [0.09, 0.59], [0.09, 0.59], [0.09, 0.59], [0.10, 0.60], [0.10, 0.60],
    [0.09, 0.59], [0.09, 0.59], [0.10, 0.60], [0.09, 0.59], [0.08, 0.58],
    [0.09, 0.59], [0.10, 0.60]
    ]
class1_36_70_up = [
    [0.08, 0.58], [0.04, 0.54], [0.01, 0.51], [0.00, 0.50], [-0.00, 0.50],
    [-0.00, 0.50], [-0.01, 0.49], [-0.02, 0.48], [-0.05, 0.45], [-0.06, 0.44],
    [-0.06, 0.44], [-0.08, 0.42], [-0.09, 0.41], [-0.10, 0.40], [-0.11, 0.39],
    [-0.12, 0.38], [-0.13, 0.37], [-0.15, 0.35], [-0.15, 0.35], [-0.13, 0.37],
    [-0.14, 0.36], [-0.14, 0.36], [-0.16, 0.34], [-0.17, 0.33], [-0.15, 0.35],
    [-0.15, 0.35], [-0.14, 0.36], [-0.13, 0.37], [-0.12, 0.38], [-0.10, 0.40],
    [-0.09, 0.41], [-0.07, 0.43], [-0.07, 0.43], [-0.05, 0.45], [-0.03, 0.47]
    ]
class1_71_105_bottom = [
    [ -0.02, 0.48], [ 0.01, 0.51], [ 0.04, 0.54], [ 0.06, 0.56], [ 0.08, 0.58],
    [ 0.11, 0.61], [ 0.13, 0.63], [ 0.16, 0.66], [ 0.19, 0.69], [ 0.22, 0.72],
    [ 0.23, 0.73], [ 0.25, 0.75], [ 0.26, 0.76], [ 0.27, 0.77], [ 0.27, 0.77],
    [ 0.29, 0.79], [ 0.32, 0.82], [ 0.32, 0.82], [ 0.33, 0.83], [ 0.35, 0.85],
    [ 0.36, 0.86], [ 0.37, 0.87], [ 0.36, 0.86], [ 0.39, 0.89], [ 0.41, 0.91],
    [ 0.42, 0.92], [ 0.40, 0.90], [ 0.41, 0.91], [ 0.43, 0.93], [ 0.45, 0.95],
    [ 0.44, 0.94], [ 0.45, 0.95], [ 0.48, 0.98], [ 0.48, 0.98], [ 0.50, 1.00]
    ]
class1_106_140_bottom = [
    [0.50, 1.00], [0.48, 0.98], [0.48, 0.98], [0.49, 0.99], [0.51, 1.01],
    [0.50, 1.00], [0.51, 1.01], [0.52, 1.02], [0.49, 0.99], [0.46, 0.96],
    [0.43, 0.93], [0.40, 0.90], [0.34, 0.84], [0.28, 0.78], [0.23, 0.73],
    [0.19, 0.69], [0.13, 0.63], [ 0.06, 0.56], [-0.00, 0.50], [-0.08, 0.42],
    [-0.16, 0.34], [-0.27, 0.23], [-0.34, 0.16], [-0.41, 0.09], [-0.57, -0.07],
    [-0.80, -0.30], [-1.07, -0.57], [-1.50, -1.00], [-2.01, -1.51], [-2.53,
        -2.03], [-2.99, -2.49], [-3.30, -2.80], [-3.51, -3.01], [-2.99, -2.49],
    [-2.72, -2.22]
    ]


def objectCreator(kwargs):
    objectDicts = []
    for elem in kwargs:
        for combinations in product(*elem["arguments"].values()):
            tempDict = dict(zip(elem["arguments"].keys(), combinations))
            combinationsStr = [
                str(elem).replace(
                    ' ', '').replace(
                    '<function', '')[
                    :5] for elem in combinations]
            tempName = str(elem["objectType"].__name__)[
                :5] + '_' + '_'.join(combinationsStr)
            tempDict['name'] = tempName
            objectDicts.append(
                {'objectType': elem["objectType"], "arguments": tempDict})

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
                     [algorithmInputLayerSize, 5, algorithmInputLayerSize],
                 ],
                 'seed': [seed],
                 'lr': [0.001],
                 'bias': [True],
                 'activationFct': [nn.ReLU()],
                 'initialization': [nn.init.xavier_normal_],
                 'batchSize': [30],
                 'epochs': [200]
             }
         }
    ])
    return algorithms


def getDatasets(seed):
    datasets = objectCreator([
        {
            "objectType": ecg5000,
            "arguments":
                {
                    'seed': [seed],
                    'windowStep': [35],
                    'purposeFlg': ['train'],
                }
        },
        {
            "objectType": sampleBoxTest,
            "arguments":
                {
                    'seed': [seed],
                    'purposeFlg': ['test'],
                    'box': [
                        # 0 - 35  class 0  (Bottom Part)
                        class0_0_35_bottom,
                        # 36 - 70  class 0  (Bottom Part)
                        class0_36_70_bottom,
                        # 71 - 105  class 0  (Upper Peak)
                        class0_71_105_up,
                        # 106 - 140  class 0  (Upper Peak)
                        class0_106_140_up,
                        # 0 - 35 Class 1 (Upper Part)
                        class1_0_35_up,
                        # 36 - 70 Class 1 (Upper Part)
                        class1_36_70_up,
                        # 71 - 105 Class 1 (Bottom Part)
                        class1_71_105_bottom,
                        # 106 - 140 Class 1 (Bottom Part)
                        class1_106_140_bottom
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


                     # ECG Boxes
                     {
                         'adversAttack': {'severity': 2},
                         'customBoundingBox': class0_0_35_bottom
                     },
                     {
                         'adversAttack': {'severity': 2},
                         'customBoundingBox': class0_36_70_bottom
                     },
                     {
                         'adversAttack': {'severity': 2},
                         'customBoundingBox': class0_71_105_up
                     },
                     {
                         'adversAttack': {'severity': 2},
                         'customBoundingBox': class0_106_140_up
                     },
                     {
                         'adversAttack': {'severity': 2},
                         'customBoundingBox': class1_0_35_up
                     },
                     {
                         'adversAttack': {'severity': 2},
                         'customBoundingBox': class1_36_70_up
                     },
                     {
                         'adversAttack': {'severity': 2},
                         'customBoundingBox': class1_71_105_bottom
                     },
                     {
                         'adversAttack': {'severity': 2},
                         'customBoundingBox': class1_106_140_bottom
                     },
                 ],

                 'numSolutions': [5],
                 'boundaryAroundSolution': [0.1],
             }
         }

    ])
    return smts


def getResults():
    results = [
        origReconTsPlot(numDataPoints=700),
        maxAdversAttack(accuracy=0.025),
        maxAdversAttackQualPlot(accuracy=0.025),
        avgError(),
        timeMaxErrorPlot(times_s=[60*1*i for i in range(1,181)], errFct = 'LInfty'),
    ]
    return results

