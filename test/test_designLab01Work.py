import os
import sys

# set the code and test dir
test_dir = os.path.dirname(__file__)
code_dir = os.path.normpath(test_dir + "/../Lec_1")

sys.path.append(code_dir)

import unittest

# import the source code that will be tested
import designLab01Work as src

class Test_designLab01Work(unittest.TestCase):
    """  
    test suite for the design Lab 01
    all labwork must pass all test here before submitted.
    """

    def setUp(self) -> None:
        self.v = src.V2(1.0, 2.0)
        self.b = src.V2(2.2, 3.3)
        self.p1 = src.Polynomial([1,2,3])
        self.p2 = src.Polynomial([100,200])

    def test_fib_0_returns_0(self):
        self.assertEqual(src.fib(0), 0, "fib(0) FAILED to return 0")
    
    def test_fib_1_returns_1(self):
        self.assertEqual(src.fib(1), 1, "fib(1) FAILED to returns 1")

    def test_fib_6_returns_8(self):
        self.assertEqual(src.fib(6), 8, "fib(6) FAILED to returns 6")
    
    def test_negative_argument_raise_value_error(self):
        with self.assertRaises(ValueError) as e:
            src.fib(-2)
        
        self.assertTrue("argument cannot be negative" in e.exception.args)
    
    # test for Object Oriented Practice
    def test_print_V2_returns_class_name_and_list(self):
        self.assertEqual(str(src.V2(1.1, 2.2)), "V2[1.1, 2.2]", "V2 __str__ function FAILED")
    
    def test_get_X_retuns_the_first_vector_element(self):
        self.assertEqual(self.v.getX(), 1.0, "getX FAILED")
    
    def test_get_Y_return_the_second_vector_element(self):
        self.assertEqual(self.v.getY(), 2.0, "getY FAILED")
    
    def test_add_v_return_addition_with_vector_in_the_argument(self):
        self.assertEqual(str(self.v.add(self.b)), "V2[3.2, 5.3]", "add function FAILED")

    def test_mul_v_return_vector_to_scalar_multiplication(self):
        self.assertEqual(str(self.v.mul(2)), "V2[2.0, 4.0]", "mul function FAILED")

    def test_add_and_mul_return_scalar_mult_after_vector_add(self):
        self.assertEqual(str(self.v.add(self.b).mul(-1)), "V2[-3.2, -5.3]", "combination functions add and mul FAILED")

    def test_addition_operator_overloading_between_two_vectors(self):
        self.assertEqual(str(src.V2(1.1, 2.2) + src.V2(3.0, 4.0)), "V2[4.1, 6.2]", "addition overloading FAILED")
    
    def test_multiplication_operator_overloadin_between_vector_and_scalar(self):
        self.assertEqual(str(self.b * (-1)), "V2[-2.2, -3.3]", "multiplication operator overloadinf FAILED")

    # test class Polynomial
    def test_print_polynomials(self):
        self.assertEqual(str(self.p1), "1.000 z**2 + 2.000 z + 3.000", "__str__ Polynomial FAILED")
    
    def test_add_function_pass_other_poly_as_argument(self):
        self.assertEqual(str(self.p1.add(self.p2)), "1.000 z**2 + 102.000 z + 203.000", "add function Polynomial FAILED")

    def test_add_function_longer_poly_as_argument(self):
        self.assertEqual(str(self.p2.add(self.p1)), "1.000 z**2 + 102.000 z + 203.000", "add function Polynomial FAILED")

    def test_pass_argument_to_polynomial(self):
        self.assertEqual(self.p1(1), 6.0, "__call__ FAILED")

    def test_pass_negative_argument_to_polynomial(self):
        self.assertEqual(self.p1(-1), 2.0, "__call__ FAILED")

    def test_operator_overloading_addition(self):
        self.assertEqual(str(self.p1 + self.p2), "1.000 z**2 + 102.000 z + 203.000", "__add__ function Polynomial FAILED")
    
    # additional requirement for higher order polynomial but with zero coeffs
    def test_zero_coeff_for_polynomial(self):
        self.assertEqual(str(src.Polynomial([3,0,0,0,0])), "3.000 z**4 ", "zero coeff handler FAILED")

    # : another additional requirement to handle negative coefficient:
    def test_poly_with_negative_coeffs(self):
        self.assertEqual(str(src.Polynomial([-1,-2,-3])), "-1.000 z**2 -2.000 z -3.000", "__str__ Polynomial FAILED")

    def test_poly_argument_for_added_poly(self):
        self.assertEqual((self.p1 + self.p2)(10), 1323.0, "__call__ FAILED")
    
    # TODO: create test for Polynomial multiplication for both internal and/or operator overloading:

    # TODO: create test for root of Polynomial (using the qudratic root equation maybe?) 
    # TODO: What abot more than quadratic root formula?