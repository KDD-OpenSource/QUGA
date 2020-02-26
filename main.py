"""Main Module of AE_SMT Framework
"""

from src.utils.executeExperiments import executeExperiments
from src.utils.experimentSettings import ExperimentSettings
from src.utils.objectCreator import objectCreator, getAlgorithms, getDatasets, getSmts, getResults

def main():
	settings = getExperimentSettings()
	objects = getExperimentObjects(settings.seed)
	executeExperiments(settings, objects)


def getExperimentSettings():
	settings = ExperimentSettings()
	settings.testName = 'EveryResultSineWavePart'
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