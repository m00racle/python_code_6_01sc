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

    def test_two_accumulator_sm_verbose_scenario(self):
        """  
        given two accumulator SM as constituent
        test the verbose output
        """
        # arrange 
        inps = [2,3,4,200,300,400,1,2,3]
        s = c.Switch(lambda i: i > 100, sm.Accumulator(), sm.Accumulator())
        capture = io.StringIO()
        sys.stdout = capture

        expected_print = \
            "Start state: (0, 0)\n"+\
            "In: 2 Out: 2 Next State: (0, 2)\n"+\
            "In: 3 Out: 5 Next State: (0, 5)\n"+\
            "In: 4 Out: 9 Next State: (0, 9)\n"+\
            "In: 200 Out: 200 Next State: (200, 9)\n"+\
            "In: 300 Out: 500 Next State: (500, 9)\n"+\
            "In: 400 Out: 900 Next State: (900, 9)\n"+\
            "In: 1 Out: 10 Next State: (900, 10)\n"+\
            "In: 2 Out: 12 Next State: (900, 12)\n"+\
            "In: 3 Out: 15 Next State: (900, 15)\n"
        
        # action
        s.transduce(inps, verbose=True)
        sys.stdout = sys.__stdout__

        # assert
        self.assertEqual(capture.getvalue(), expected_print)


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

    def test_two_accumulator_sm_verbose_scenario(self):
        inps = [2,3,4,200,300,400,1,2,3]
        m = c.Multiplex(lambda i: i > 100, sm.Accumulator(), sm.Accumulator())
        # arrange
        capture = io.StringIO()
        sys.stdout = capture

        expected_print = \
            "Start state: (0, 0)\n"+\
            "In: 2 Out: 2 Next State: (2, 2)\n"+\
            "In: 3 Out: 5 Next State: (5, 5)\n"+\
            "In: 4 Out: 9 Next State: (9, 9)\n"+\
            "In: 200 Out: 209 Next State: (209, 209)\n"+\
            "In: 300 Out: 509 Next State: (509, 509)\n"+\
            "In: 400 Out: 909 Next State: (909, 909)\n"+\
            "In: 1 Out: 910 Next State: (910, 910)\n"+\
            "In: 2 Out: 912 Next State: (912, 912)\n"+\
            "In: 3 Out: 915 Next State: (915, 915)\n"
        
        # action 
        m.transduce(inps, verbose=True)
        sys.stdout = sys.__stdout__

        # assert
        self.assertEqual(capture.getvalue(), expected_print)
    
    def test_accumulator_gain_constituent_scenario(self):
        inps = [2,3,4,200,300,400,1,200,3]
        m = c.Multiplex(lambda i: i > 100, sm.Accumulator(), sm.Gain(1))
        # assert
        self.assertEqual(m.transduce(inps), [2, 3, 4, 209, 509, 909, 1, 1110, 3])

    def test_accumulator_gain_verbose_scenario(self):
        inps = [2,3,4,200,300,400,1,200,3]
        m = c.Multiplex(lambda i: i > 100, sm.Accumulator(), sm.Gain(1))
        # arrange
        capture = io.StringIO()
        sys.stdout = capture

        expected_print = \
            "Start state: (0, 0)\n"+\
            "In: 2 Out: 2 Next State: (2, 2)\n"+\
            "In: 3 Out: 3 Next State: (5, 3)\n"+\
            "In: 4 Out: 4 Next State: (9, 4)\n"+\
            "In: 200 Out: 209 Next State: (209, 200)\n"+\
            "In: 300 Out: 509 Next State: (509, 300)\n"+\
            "In: 400 Out: 909 Next State: (909, 400)\n"+\
            "In: 1 Out: 1 Next State: (910, 1)\n"+\
            "In: 200 Out: 1110 Next State: (1110, 200)\n"+\
            "In: 3 Out: 3 Next State: (1113, 3)\n"
        
        # action 
        m.transduce(inps, verbose=True)
        sys.stdout = sys.__stdout__

        # assert 
        self.assertEqual(capture.getvalue(), expected_print)

class TestClassIf(unittest.TestCase):
    """  
    Testing the conditional.py If class
    """
    def setUp(self) -> None:
        self.i = c.If(lambda i: i > 100, sm.Gain(1), sm.Accumulator())

    def test_if_gain_accumulator_set_sm_gain_scenario(self):
        """  
        Test If class with SM1: Gain(1) and SM2: Accumulator()
        Scenrio choose SM1 to run the whole
        """
        feeds = [200,3,4,200,300,400,1,200,3]
        # assert
        self.assertEqual(self.i.transduce(feeds), [200,3,4,200,300,400,1,200,3])

    def test_if_gain_accumulator_set_accumulaor_scenario(self):
        """  
        Test If class with SM1: Gain(1) and SM2: Accumulator()
        Scenrio choose SM2 to run the whole
        """
        feeds = [2,3,4,200,300,400,1,200,3]
        # assert
        self.assertEqual(self.i.transduce(feeds), [2,5,9,209,509,909,910,1110,1113])

    def test_if_gain_accumulator_set_accumulaor_verbose_scenario(self):
        """  
        Test If class with SM1: Gain(1) and SM2: Accumulator()
        Scenrio choose SM2 to run the whole
        """
        feeds = [2,3,4,200,300,400,1,200,3]
        capture = io.StringIO()
        sys.stdout = capture
        expected_print = \
            "Start state: ('start', None)\n"+\
            "In: 2 Out: 2 Next State: ('runningSM2', 2)\n"+\
            "In: 3 Out: 5 Next State: ('runningSM2', 5)\n"+\
            "In: 4 Out: 9 Next State: ('runningSM2', 9)\n"+\
            "In: 200 Out: 209 Next State: ('runningSM2', 209)\n"+\
            "In: 300 Out: 509 Next State: ('runningSM2', 509)\n"+\
            "In: 400 Out: 909 Next State: ('runningSM2', 909)\n"+\
            "In: 1 Out: 910 Next State: ('runningSM2', 910)\n"+\
            "In: 200 Out: 1110 Next State: ('runningSM2', 1110)\n"+\
            "In: 3 Out: 1113 Next State: ('runningSM2', 1113)\n"
        # action
        self.i.transduce(feeds, verbose=True)
        sys.stdout = sys.__stdout__
        # assert
        self.assertEqual(capture.getvalue(), expected_print)