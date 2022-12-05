import os, sys, unittest, io

# set the code and test dir
test_dir = os.path.dirname(__file__)
code_dir = os.path.normpath(test_dir + "/../Lec_2_State_Machine")

sys.path.append(code_dir)

import cascade as c
from state_machine import Delay

class TestCascasdeClass(unittest.TestCase):
    """  
    test the Cascade class
    """

    def test_cascading_two_delay_state_machines(self):
        # arrange:
        m1 = Delay(99)
        m2 = Delay(22)
        casc = c.Cascade(m1, m2)
        inputs = [3,8,2,4,6,5]
        expected_outputs = [22, 99, 3, 8, 2, 4]
        # assert
        # self.fail('NO TEST')
        self.assertEqual(casc.transduce(inputs), expected_outputs)