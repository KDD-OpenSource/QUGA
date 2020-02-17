"""
This file implements the superclass algorithm from which the class autoencoder inherits (to have the possibility to add further algorithms). -> Note that this violates some coding paradigma. Make it as simple and add stuff later...
This framework only works for algorithms that have an autoencoding structure (i.e. its output is a reconstruction of the input). Otherwise the 'iterate_algorithm'-function is not defined.
"""
import abc
import pandas as pd
import numpy as np
import uuid

class algorithm(metaclass = abc.ABCMeta):
	def __init__(self, name, seed, architecture, lr, batch_size, epochs):
		self.name = name
		self.obj_id = uuid.uuid4()
		self.seed = seed
		self.lr = lr
		self.batch_size = batch_size
		self.epochs = epochs
		self.architecture = architecture
		pass



	@abc.abstractmethod
	def fit(self, X):
		pass

	@abc.abstractmethod
	def predict(self, X):
		pass

	# X is a dataset on which to iterate the algorithm (autoencoder), to this end X is transformed to points via the window_step parameter, k is the number of steps
	# returns a list of Dataframes in which the number of Dataframes is given by k (the number of iterations of the algorithm)
	def iterate_algorithm(self, dataset, k = 1):
		if self.architecture[0] != self.architecture[-1]:
			print('Cannot iterate, because dim(f(x)) != dim(x)')
		results = []
		results.append(dataset)
		for i in range(k):
			results.append(self.predict(results[-1]))
		return results		