
		# REAL DATA
		# {
		# "objectType": ecg5000,
		# "arguments":
		# 	{
		# 	'seed': [seed],
		# 	'windowStep': [140],
		# 	'purposeFlg': ['train', 'test'],
		# 	}
		# }


		# SYNTHETIC DATA
		# {
		# "objectType": twoSineFrequenciesNoise,
		# "arguments":
		# 	{
		# 	'seed': [seed],
		# 	'purposeFlg': ['train','test'],
		# 	'windowStep': [algorithmInputLayerSize],
		# 	# 'numCycles0': [20,40,60,80,100,150,200,250,500],
		# 	'numCycles0': [250],
		# 	'cycleLength0': [3*algorithmInputLayerSize],
		# 	'numCycles1': [500],
		# 	'cycleLength1': [algorithmInputLayerSize],
		# 	'var': [0.1]
		# 	}
		# },
		# {
		# "objectType": twoSineFrequenciesNoise,
		# "arguments":
		# 	{
		# 	'seed': [seed],
		# 	'purposeFlg': ['test'],
		# 	'windowStep': [algorithmInputLayerSize],
		# 	'numCycles0': [5],
		# 	'cycleLength0': [3*algorithmInputLayerSize],
		# 	'numCycles1': [5],
		# 	'cycleLength1': [algorithmInputLayerSize],
		# 	'var': [0.1]
		# 	}
		# },
		# {
		# "objectType": twoSineFrequenciesNoise,
		# "arguments":
		# 	{
		# 	'seed': [seed],
		# 	'purposeFlg': ['test'],
		# 	'windowStep': [algorithmInputLayerSize],
		# 	'numCycles0': [500],
		# 	'cycleLength0': [3*algorithmInputLayerSize],
		# 	'numCycles1': [500],
		# 	'cycleLength1': [algorithmInputLayerSize],
		# 	'var': [0.1]
		# 	}
		# },
		# {
		# "objectType": twoSineFrequenciesNoise,
		# "arguments":
		# 	{
		# 	'seed': [seed],
		# 	'purposeFlg': ['test'],
		# 	'windowStep': [algorithmInputLayerSize],
		# 	'numCycles0': [500],
		# 	'cycleLength0': [3*algorithmInputLayerSize],
		# 	'numCycles1': [0],
		# 	'cycleLength1': [algorithmInputLayerSize],
		# 	'var': [0.1]
		# 	}
		# },		
		# {
		# "objectType": twoSineFrequenciesNoise,
		# "arguments":
		# 	{
		# 	'seed': [seed],
		# 	'purposeFlg': ['test'],
		# 	'windowStep': [algorithmInputLayerSize],
		# 	'numCycles0': [0],
		# 	'cycleLength0': [3*algorithmInputLayerSize],
		# 	'numCycles1': [500],
		# 	'cycleLength1': [algorithmInputLayerSize],
		# 	'var': [0.1]
		# 	}
		# },


		# TESTDATA
		# {
		# "objectType": twoSineFrequenciesNoiseTest,
		# "arguments":
		# 	{
		# 	'seed': [seed],
		# 	'purposeFlg': ['test'],
		# 	'windowStep': [algorithmInputLayerSize],
		# 	'cycleLengths': [[5,20]],
		# 	'cycleSplits': [[1,4]],
		# 	'numPerCluster': [[[1],[1,1,1,1]]],
		# 	'var': [0.1]
		# 	}
		# },
		{
		"objectType": sampleBoxTest,
		"arguments":
			{
			'seed': [seed],
			'purposeFlg': ['test'],
			'box': [[[math.sin((2*math.pi*x)/(3*algorithmInputLayerSize)) - 0.1,math.sin((2*math.pi*x)/(3*algorithmInputLayerSize))+0.1] for x in range(algorithmInputLayerSize,2*algorithmInputLayerSize)]],
			'numPoints': [10],
			}
		},
