"""main Module of AE_SMT Framework
documentation of how things should be used should be later
should provide the following:
	-> choice of:
		-> datasets 
		-> SMT and AE variations
		-> evaluation results/types of graphs to be plotted 
			=> each is a list of object that are created in the list
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
	settings.testName = 'My_Test'
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