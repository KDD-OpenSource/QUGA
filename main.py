"""Main Module of AE_SMT Framework
"""

from src.utils.executeExperiments import executeExperiments
from src.utils.experimentSettings import ExperimentSettings
from src.utils.objectCreator import objectCreator, getAlgorithms, getDatasets, getSmts, getResults

def main():
	if __name__ == '__main__':
		settings = getExperimentSettings()
		objects = getExperimentObjects(settings.seed)
		executeExperiments(settings, objects)


def getExperimentSettings():
	settings = ExperimentSettings()
	settings.testName = 'EveryResultSineWavePart'
	settings.description = ''
	settings.experimentScope = 'ae_smt'
	# settings.experimentScope = 'smt'
	settings.resultFolders = None
	# settings.resultFolders = ['C:\\Users\\Ben\\Desktop\\Projekte\\Eigene Paper\\AE+SMT\\Experiments\\AE_SMT\\results\\2020.02.27\\51431\\autoe_f08e6\\sineN_74d06']

	return settings


def getExperimentObjects(seed):
	algorithms = getAlgorithms(seed)
	datasets = getDatasets(seed)
	smts = getSmts()
	results = getResults()
	return algorithms, datasets, smts, results


main()

