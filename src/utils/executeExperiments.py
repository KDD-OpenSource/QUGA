"""
This file executes every experiment as specified by the lists 'algorithms', 'datasets', 'smts' and 'results'.
Furthermore it creates the respective folder-structure and thereafter stores the results.
"""

import os
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import torch
from .myUtils import splitDatasets, createFolderStructure, addFolder, loadParamsFromJson, loadAE, storeSmtResult, loadDataset
from ..data.dataset import dataset
from ..algorithms.autoencoder import autoencoder
from ..algorithms.smtSolver import smtSolver
from ..evaluation.resultAE import resultAE
from ..evaluation.resultSMT import resultSMT
from itertools import product
import multiprocessing as mp
from z3 import *


def executeExperiments(
        settings,
        objects,
):
    algorithms, trainDatasets, testDatasets, validationDatasets, smts, resultsAE, resultsSMT = decomposeObjects(objects)
    runFolder = createFolderStructure(settings.seed)
    start = time.time()

    # this trains all autoencoders on all training sets and calculates
    # their respective results on test datasets. The results are stored in
    # runFolder
    if settings.experimentScope == 'ae_smt' or settings.experimentScope == 'ae':
        trainDatasetAEFolders = execAEExperiments(
            algorithms, trainDatasets, testDatasets, resultsAE, runFolder)

    # this runs all smts on all trained autoencoders
    if settings.experimentScope == 'ae_smt' or settings.experimentScope == 'smt':
        collectedResults = execSMTExperiments(
            trainDatasetAEFolders, smts, resultsSMT)


    end = time.time()
    calcTime = end - start
    writeSettingsFile(settings, calcTime, runFolder)


def execAEExperiments(
        algorithms,
        trainDatasets,
        testDatasets,
        resultsAE,
        runFolder):
    trainDatasetAEFolders = []
    for algorithm in algorithms:
        trainDatasetAEFolders.extend(
            execFixedAlg(
                algorithm,
                trainDatasets,
                testDatasets,
                resultsAE,
                runFolder))
    return trainDatasetAEFolders


def execFixedAlg(algorithm, trainDatasets, testDatasets, resultsAE, runFolder):
    trainDatasetAEFolders = []
    for trainDataset in trainDatasets:
        tmpFolderTrain = addAEFolderstructure(
            runFolder, algorithm, trainDataset)
        algorithm.trainAE(trainDataset)
        storeTrainedAE(algorithm, trainDataset, tmpFolderTrain)
        trainDatasetAEFolders.append(tmpFolderTrain)
        execFixedTrainDataset(
            algorithm,
            trainDataset,
            testDatasets,
            resultsAE,
            tmpFolderTrain)
    return trainDatasetAEFolders


def execFixedTrainDataset(
        algorithm,
        trainDataset,
        testDatasets,
        resultsAE,
        tmpFolderTrain):
    for testDataset in testDatasets:
        tmpFolderTest = addFolder(tmpFolderTrain, testDataset)
        testDataset.saveData(tmpFolderTest)
        execFixedTestDataset(
            algorithm,
            trainDataset,
            testDataset,
            resultsAE,
            tmpFolderTest)


def execFixedTestDataset(
        algorithm,
        trainDataset,
        testDataset,
        resultsAE,
        tmpFolderTest):
    for resultAE in resultsAE:
        execFixedResultAE(
            algorithm,
            trainDataset,
            testDataset,
            resultAE,
            tmpFolderTest)


def execFixedResultAE(
        algorithm,
        trainDataset,
        testDataset,
        resultAE,
        tmpFolderTest):
    resultAE.calcResult(algorithm, trainDataset, testDataset)
    resultAE.storeAEResult(
        tmpFolderTest,
        trainDataset,
        testDataset,
        algorithm,
        testName='test')


def decomposeObjects(objects):
    trainDatasets, testDatasets, validationDatasets = splitDatasets(objects[1])
    resultsAE, resultsSMT = splitResults(objects[3])
    return objects[0], trainDatasets, testDatasets, validationDatasets, objects[2], resultsAE, resultsSMT


def addAEFolderstructure(runFolder, algorithm, trainDataset):
    tmpFolderAlg = addFolder(runFolder, algorithm)
    tmpFolderTrain = addFolder(tmpFolderAlg, trainDataset)
    return tmpFolderTrain


def storeTrainedAE(algorithm, trainDataset, tmpFolderTrain):
    trainDataset.saveData(tmpFolderTrain)
    algorithm.saveAE(tmpFolderTrain)


def splitResults(results):
    resultsAE = []
    resultsSmt = []
    for elem in results:
        if isinstance(elem, resultAE):
            resultsAE.append(elem)
        elif isinstance(elem, resultSMT):
            resultsSmt.append(elem)
        else:
            raise Exception(
                'Any result should belong a result type indicated by a given flg')
    return resultsAE, resultsSmt


def execSMTExperiments(trainDatasetAEFolders, smts, resultsSMT):
    pool = mp.Pool(mp.cpu_count())
    arg_list = []
    for folder, smt in product(trainDatasetAEFolders, smts):
        arg_list.append([folder, smt, resultsSMT])
    collectedResults = []
    for arguments in arg_list:
        collectedResults.append(
            pool.apply_async(
                execFixedFolder,
                args=arguments))
    pool.close()
    pool.join()
    #import pdb; pdb.set_trace()

    #arg_list = []
    #for folder, smt in product(trainDatasetAEFolders, smts):
    #    arg_list.append((folder, smt, resultsSMT))
    #collectedResults = []
    #for arguments in arg_list:
    #    collectedResults.append(execFixedFolder(*arguments))

    return collectedResults

def execFixedFolder(folder, smt, resultsSMT):
    print('process id:', os.getpid())
    print(folder)
    autoencoder = loadAE(folder)
    trainDataset = loadDataset(folder, 'trainDataset')
    results = []
    results.append(
        execFixedSMT(
            folder,
            smt,
            resultsSMT,
            autoencoder,
            trainDataset))
    return results


def execFixedSMT(folder, smt, resultsSMT, autoencoder, trainDataset):
    tmpFolderSmt = addFolder(folder, smt)
    smt.saveSMTParameters(tmpFolderSmt)
    results = []
    for resultSMT in resultsSMT:
        results.append(
            execFixedResultSMT(
                smt,
                resultSMT,
                autoencoder,
                tmpFolderSmt,
                trainDataset))
    return results


def execFixedResultSMT(
        smt,
        resultSMT,
        autoencoder,
        tmpFolderSmt,
        trainDataset):
    smt.clearSmt()
    resultSMT.calcResult(
        algorithm=autoencoder,
        trainDataset=trainDataset,
        smt=smt)
    print(resultSMT.result)
    resultSMT.storeSMTResult(tmpFolderSmt)
    print('Autoencoder: {}'.format(autoencoder.architecture))
    print('resultSMT: {}'.format(resultSMT.name))
    if 'collResults' in resultSMT.__dir__():
        print(resultSMT.collResults)
        return resultSMT
    else:
        return None


def writeSettingsFile(settings, calcTime, folder):
    file = os.path.join(folder, settings.testName + '.txt')
    with open(file, 'w') as file:
        file.write('This run took {} seconds.'.format(calcTime))
        file.write('\n')
        file.write(settings.description)
