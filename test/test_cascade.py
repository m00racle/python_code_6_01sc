"""  
test for cascade SM code
"""
import os
import sys
import unittest
import cascade as c
from state_machine import Delay, Increment

# set the code and test dir
test_dir = os.path.dirname(__file__)
code_dir = os.path.normpath(test_dir + "/../Lec_2_State_Machine")

sys.path.append(code_dir)



class TestCascasdeClass(unittest.TestCase):
    """  
    test the Cascade class
    """

    def test_cascading_two_delay_state_machines(self):
        """  
        testing two Delay SMs arrange in cascade as one SM
        """
        # arrange:
        m1 = Delay(99)
        m2 = Delay(22)
        casc = c.Cascade(m1, m2)
        inputs = [3,8,2,4,6,5]
        expected_outputs = [22, 99, 3, 8, 2, 4]
        # assert
        # self.fail('NO TEST')
        self.assertEqual(casc.transduce(inputs), expected_outputs)

    def test_cascading_increment_delay_state_machines(self):
        """  
        Based on module exercise on State Machine
        """
        # arrange
        # Increment state machine with increment 2 for each inputs
        i = Increment(2)
        # delay SM with init State 99
        d = Delay(99)
        # Cascade them all:
        casc = c.Cascade(i, d)

        # assert
        self.assertEqual(casc.transduce([3.5, 8, 2.1, 4, 65]), [99, 5.5, 10, 4.1, 6])

class TestIncrementClass(unittest.TestCase):
    """  
    testing Increment class
    both safe and unsafe
    """
    def test_increment_numbers_valid(self):
        """  
        test the increment with valid int and float
        """
        # arrange
        inputs = [3.5, 8, 2.1, 4, 65]
        incr = 2
        expected_outputs = [5.5, 10, 4.1, 6, 67]

        # action
        inc = Increment(incr)
        self.assertEqual(inc.transduce(inputs), expected_outputs)
        
    def test_increment_non_numbers(self):
        """  
        Test handling non numbers 
        When the input is non numbers it must output None
        """
        inputs = [2.2, True, None, 'a', 9]
        k = 2.5
        expected_outputs = [4.7, None, None, None, 11.5]

        # action
        inc = Increment(k)
        # assert
        self.assertEqual(inc.transduce(inputs), expected_outputs)

if __name__ == '__main__':
    unittest.main()