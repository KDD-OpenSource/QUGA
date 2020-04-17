"""Main Module of AE_SMT Framework
"""
import matplotlib
matplotlib.use('Agg')
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
	# settings.testName = 'OrigReconQualSmallKitchen'
	# settings.testName = 'MoxingBoxesWithLargerCirclesIn10Steps_takingHalfSinewaves'
	# settings.testName = 'MoxingBoxesThroughMiddleWith50Dims'
	# settings.testName = 'CreatingAGoodOrigReconSineCurvePlot'
	# settings.testName = 'NewDataSet_KitchenAppliances_MonEvening'
	# settings.testName = 'GrowingBoxAroundSineTrainPointCorrected'	
	# settings.testName = 'AdversAttackOnSmallCluster_DifferentImbalancedDatasets_WithMaxErrorEsts'	
	# settings.testName = 'TestECGReconstruction_WindowStep35_200Epochs_AVGError'
	# settings.testName = 'ECG_WithAdversAttack_WithSamplEsts'
	# settings.testName = 'ECG_WithSamplEsts_2_25'
	# settings.testName = 'Synthetic_MaxAdversWithSamplEstsUptoK_25'


	# settings.testName = 'FindOutBox_ECG'
	# settings.testName = 'Frequency_TestSet'


	# settings.testName = 'ParallelPlotECGTestSet'


	# settings.testName = 'ParallelPlotECGTrainSet_140TimeSteps'
	# settings.testName = 'SyntheticDataFullExperiment' 
	# settings.testName = 'RealDataFullExperiment_200Epochs_FOR_AVERAGE_ERROR' 
	# settings.testName = 'RealDataFullExperiment_WithOutOrigReconPlot' 
	# settings.testName = 'RealDataFullExperiment_WithOutOrigReconPlot_WithoutSampling' 
	# settings.testName = 'SyntheticDataFull_WithoutOrigRecon_WithoutSampling' 
	# settings.testName = 'SyntheticDataFull_WithoutOrigRecon_WithSampling_HopeBetterReconstruction' 
	# settings.testName = 'TestSynthMaxAdversAttackScale' 
	# settings.testName = 'TestSynthMaxAdversAttackScale' 
	# settings.testName = 'FULLSYNTHETIC_20_60_100_Epochs' 
	# settings.testName = 'RealECG_200_Epochs_k_25' 
	# settings.testName = 'TestAEParamPlots' 
	# settings.testName = 'TestTimeMaxErrorPlot'
	# settings.testName = 'TestLInftyEst'
	# settings.testName = 'PlottingTimeVSErrors_2Hours'
	settings.testName = 'NONTEST_PlottingTimeVSErrors_2Hours_OLDAESYN'


	# settings.testName = 'NumSamplesForEstimationVSmaxAdversEst'	

	# settings.testName = 'TwoSineCurves_MultipleFrequencies_NonAveraging'	
	settings.description = ''
	# settings.experimentScope = 'ae_smt'
	settings.experimentScope = 'smt'
	settings.resultFolders = None
	return settings


def getExperimentObjects(seed):
	algorithms = getAlgorithms(seed)
	datasets = getDatasets(seed)
	smts = getSmts()
	results = getResults()
	return algorithms, datasets, smts, results


main()
