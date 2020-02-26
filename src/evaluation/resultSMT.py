from .result import result
import abc
import os
'''I think this class really makes no sense. What do I encapsulate here for? What are shared properties of 'results' that are worth sharing? (Not existing currently) '''


"""
NOTE THAT IF YOU COMPARE TEST AND TRAIN DATA THEY NEED TO HAVE THE SAME STRUCTURE
Note that if only one dataset is needed for the plot we use the test_data per default
"""
class resultSMT(result):
	def __init__(self, name):
		self.name = name
		pass

	def saveSmtSolutions(self, tmpFolderSmt):
		if self.smtSolutions == None:
			pass
		else:
			cwd = os.getcwd()
			os.chdir(tmpFolderSmt)
			file = './smtSolutions.csv'
			with open(file, 'w') as file:
				# file.write('Time used for calculation (in seconds): ')
				# file.write(str(timeForCalc))
				# file.write('\n')	
				solutionCount = 0
				for solution in self.smtSolutions:
					solutionCount = solutionCount + 1
					file.write('Solution: {}'.format(solutionCount))
					file.write('Time used for calculation (in seconds): {}'.format(solution['calcDuration']))
					file.write('\n')
					for elem in solution['model']:
						file.write(str(elem))
						file.write(': ')
						numerator = solution['model'][elem].numerator_as_long()
						denominator = solution['model'][elem].denominator_as_long()
						decimal = float(numerator/denominator)
						file.write(str(decimal))
						file.write('\n')
					file.write('\n')
			os.chdir(cwd)
