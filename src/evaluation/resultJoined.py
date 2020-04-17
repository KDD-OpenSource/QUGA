from .result import result
import abc
import os
'''I think this class really makes no sense. What do I encapsulate here for? What are shared properties of 'results' that are worth sharing? (Not existing currently) '''


"""
NOTE THAT IF YOU COMPARE TEST AND TRAIN DATA THEY NEED TO HAVE THE SAME STRUCTURE
Note that if only one dataset is needed for the plot we use the test_data per default
"""
class resultJoined(result):
	def __init__(self, name):
		self.name = name
		pass
