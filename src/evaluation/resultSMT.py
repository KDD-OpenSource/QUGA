"""
This class allows for saving the smtSolutions
"""
from .result import result
import os



class resultSMT(result):
    def __init__(self, name):
        self.name = name
        pass

    def saveSmtSolutions(self, tmpFolderSmt):
        if self.smtSolutions is None:
            pass
        else:
            cwd = os.getcwd()
            os.chdir(tmpFolderSmt)
            file = './smtSolutions.csv'
            with open(file, 'w') as file:
                solutionCount = 0
                for solution in self.smtSolutions:
                    solutionCount = solutionCount + 1
                    file.write('Solution: {}'.format(solutionCount))
                    file.write(
                        'Time used for calculation (in seconds): {}'.format(
                            solution['calcDuration']))
                    file.write('\n')
                    for elem in solution['model']:
                        file.write(str(elem))
                        file.write(': ')
                        file.write(str(solution['model'][elem]))
                        file.write('\n')
                        #file.write(str(elem))
                        #file.write(': ')
                        #numerator = solution['model'][elem].numerator_as_long()
                        #denominator = solution['model'][elem].denominator_as_long(
                        #)
                        #decimal = float(numerator / denominator)
                        #file.write(str(decimal))
                        #file.write('\n')
                    file.write('\n')
            os.chdir(cwd)
