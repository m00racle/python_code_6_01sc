import os
import sys

# set the code and test dir
test_dir = os.path.dirname(__file__)
code_dir = os.path.normpath(test_dir + "/../Lec_1")

sys.path.append(code_dir)

import unittest

import wk143_list_comp as s

class Test_list_comp(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_even_square_func(self):
        self.assertEqual(s.evenSquare([-5,-4,-3,-2,-1,0,1,2,3,4,5]), [-4,-2,0,2,4])
    
    def test_sum_abs_prod_func_even(self):
        self.assertEqual(s.sumAbsProd([2,-3], [4,-5]), 45)
    
    def test_sum_abs_prod_func_commutative(self):
        self.assertTrue(s.sumAbsProd([1,-2,3],[-4,5]) > 0, "The return is still in default")
        self.assertEqual(s.sumAbsProd([1,-2,3],[-4,5]), s.sumAbsProd([-4,5],[1,-2,3]))