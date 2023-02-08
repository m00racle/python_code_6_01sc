import os, sys, unittest, io

test_dir = os.path.dirname(__file__)
code_dir = os.path.normpath(test_dir + "/../Lec_2_State_Machine")

sys.path.append(code_dir)

import state_machine as sm
import conditional as c

class TestSwitchClass(unittest.TestCase):
    """  
    unit tests for class Switch
    """

    def test_two_accumulator_sm_constituent_scenario(self):
        """  
        given two accumulator SM class as constituent
        """
        inps = [2,3,4,200,300,400,1,2,3]
        s = c.Switch(lambda i: i > 100, sm.Accumulator(), sm.Accumulator())

        # assert
        self.assertEqual(s.transduce(inps), [2,5,9,200,500,900,10,12,15])


class TestClassMultiplex(unittest.TestCase):
    """  
    unit test for class Multiplex
    """

    def test_two_accumulator_sm_constituent_scenario(self):
        """  
        givent two accumulator SM class as constituent in Mux
        """
        inps = [2,3,4,200,300,400,1,2,3]
        m = c.Multiplex(lambda i: i > 100, sm.Accumulator(), sm.Accumulator())

        # assert
        self.assertEqual(m.transduce(inps), [2,5,9,209,509,909,910,912, 915])

    def test_accumulator_gain_constituent_scenario(self):
        inps = [2,3,4,200,300,400,1,200,3]
        m = c.Multiplex(lambda i: i > 100, sm.Accumulator(), sm.Gain(1))
        # assert
        self.assertEqual(m.transduce(inps), [2, 3, 4, 209, 509, 909, 1, 1110, 3])