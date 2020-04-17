import unittest
from smt_solver import smt_solver
import numpy as np
from z3 import *

class test_smt_solver(unittest.TestCase):
	smt_solver_instance = smt_solver(name = 'test_solver')

	def test_0_net_constraint_solver(self):
		print('Run Test for net_constraint_solver')
		self.smt_solver_instance.net_weight_matrix = [np.array([[1,2],[1,2]]), np.array([[1,2]]), np.array([[7],[9]])]
		self.smt_solver_instance.net_bias = [np.array([13]), np.array([15,16])]
		result = self.smt_solver_instance.net_constraint_constructor(var_names = 'x')
		real_vars = [Real('x0_0'), Real('x0_1'),Real('x1_0'),Real('x2_0'), Real('x2_1')]

		supposed_result = [
		real_vars[2] == If(1*real_vars[0] +2* real_vars[1] + 13< 0, 0, 1*real_vars[0] +2* real_vars[1] + 13),
		real_vars[3] == If(7* real_vars[2] + 15 < 0, 0, 7*real_vars[2] + 15),
		real_vars[4] == If(9*real_vars[2] + 16 < 0, 0, 9*real_vars[2] + 16)
		]
		
		self.assertEqual(str(result), str(supposed_result))	


if __name__ == '__main__':
    unittest.main()