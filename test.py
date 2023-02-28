import unittest
from Solvers import DCsolver
import numpy as np
from NetlistParser import netlistParser

class TestDCSolver(unittest.TestCase):
    def test_DCSolver_PotDiv(self):
        A = np.array([[ 0.01, -0.01 , 1.  ], [-0.01, 0.02 , 0.  ], [ 1., 0., 0.  ]])
        Z = np.array([0.0, 0.0, 1.0])
        X = np.array([0.0, 0.0, 0.0])

        DCs = DCsolver(A, Z, X)
        DCs.run()
        np.testing.assert_allclose(DCs.X, np.array([1.0, 0.5, -0.005]), rtol=1e-3)
    
class TestParser(unittest.TestCase):
    def test_parser_PotDiv(self):
        nP = netlistParser('Tests/netlist.net')
        self.assertEqual(nP.vS, [{'num': '1', 'id': 0, 'nN': 0, 'pN': 1, 'value': 1.0}])
        self.assertEqual(nP.r, [{'num': '1', 'id': 1, 'nN': 2, 'pN': 0, 'value': 100.0}, {'num': '2', 'id': 1, 'nN': 1, 'pN': 2, 'value': 100.0}])
        self.assertEqual(nP.nodes, {'N001': 0, '0': 1, 'N002': 2})
    
        
if __name__=="__main__":
    unittest.main()