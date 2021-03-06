"""Main Module of AE_SMT Framework
"""
import matplotlib
matplotlib.use('Agg')
from src.utils.objectCreator import objectCreator, getAlgorithms, getDatasets, getSmts, getResults
from src.utils.experimentSettings import ExperimentSettings
from src.utils.executeExperiments import executeExperiments


def main():
    if __name__ == '__main__':
        settings = getExperimentSettings()
        objects = getExperimentObjects(settings.seed)
        executeExperiments(settings, objects)


def getExperimentSettings():
    settings = ExperimentSettings()
    settings.testName = 'MyTestName'
    settings.description = ''
    settings.experimentScope = 'ae_smt'
    settings.resultFolders = None
    return settings


def getExperimentObjects(seed):
    algorithms = getAlgorithms(seed)
    datasets = getDatasets(seed)
    smts = getSmts()
    results = getResults()
    return algorithms, datasets, smts, results


main()
