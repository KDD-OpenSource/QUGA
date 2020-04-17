		{"objectType": autoencoder,
		"arguments":
			{
			'architecture': [
			[algorithmInputLayerSize,5,algorithmInputLayerSize],
			# [algorithmInputLayerSize,10,algorithmInputLayerSize],
			# [algorithmInputLayerSize,14,algorithmInputLayerSize],
			],
			'seed': [seed],
			'lr': [0.001],
			'bias': [True],
			'activationFct': [nn.ReLU()],
			'initialization': [nn.init.xavier_normal_],
			'batchSize' : [30],
			'epochs': [400]
			}
		}
