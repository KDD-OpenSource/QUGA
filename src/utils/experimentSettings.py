import numpy as np

class ExperimentSettings():
	"""This class stores all the settings of the experiments"""
	def __init__(self):
		self.seed = np.random.randint(np.iinfo(np.uint32).max, dtype=np.uint32)
		np.random.seed(self.seed)
		self.test_name = None
		# experimentScope \in {'ae_smt', 'ae', 'smt'}
		self.experimentScope = None 
		self.result_folders = None
		self.description = None
		#Example for result folder:
		# result_folders = ['C:\\Users\\Ben\\Desktop\\Projekte\\Eigene Paper\\AE+SMT\\Experiments\\AE_SMT\\results\\2020.01.20\\11927\\autoe_cir_cir_82dff']
 