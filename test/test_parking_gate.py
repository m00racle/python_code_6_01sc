import os, sys, unittest, io

# set the code and test dir
test_dir = os.path.dirname(__file__)
code_dir = os.path.normpath(test_dir + "/../Lec_2_State_Machine")

sys.path.append(code_dir)

import parking_gate as pg

class TestFreeGate(unittest.TestCase):
    """  
    Test for Parking Gate state machine
    """
    def setUp(self) -> None:
        self.gate = pg.FreeGate()
        self.gate.start()

    def test_car_coming_and_existing_normal_scenario(self):
        """  
        test the parking gate state machine based on normal scenarion
        no violation here
        """
        # arrange
        inputs = [('bottom', False, False), ('bottom', True, False), ('bottom', True, False), ('middle', True, False), ('middle', True, False), ('middle', True, False), ('top', True, False), ('top', True, False), ('top', True, False), ('top', True, True), ('top', True, True), ('top', True, False), ('middle', True, False), ('middle', True, False), ('middle', True, False), ('bottom', True, False), ('bottom', True, False)]

        outputs = ['nop', 'raise', 'raise', 'raise', 'raise', 'raise', 'nop', 'nop', 'nop', 'lower', 'lower', 'lower', 'lower', 'lower', 'lower', 'nop', 'raise']

        printout = \
            "Stat state: waiting\n" +\
            "In: ('bottom', False, False) Out: nop Next State: waiting\n" +\
            "In: ('bottom', True, False) Out: raise Next State: raising\n" +\
            "In: ('bottom', True, False) Out: raise Next State: raising\n" +\
            "In: ('middle', True, False) Out: raise Next State: raising\n" +\
            "In: ('middle', True, False) Out: raise Next State: raising\n" +\
            "In: ('middle', True, False) Out: raise Next State: raising\n" +\
            "In: ('top', True, False) Out: nop Next State: raised\n" +\
            "In: ('top', True, False) Out: nop Next State: raised\n" +\
            "In: ('top', True, False) Out: nop Next State: raised\n" +\
            "In: ('top', True, True) Out: lower Next State: lowering\n" +\
            "In: ('top', True, True) Out: lower Next State: lowering\n" +\
            "In: ('top', True, False) Out: lower Next State: lowering\n" +\
            "In: ('middle', True, False) Out: lower Next State: lowering\n" +\
            "In: ('middle', True, False) Out: lower Next State: lowering\n" +\
            "In: ('middle', True, False) Out: lower Next State: lowering\n" +\
            "In: ('bottom', True, False) Out: nop Next State: waiting\n" +\
            "In: ('bottom', True, False) Out: raise Next State: raising\n"
        
        cap = io.StringIO()
        sys.stdout = cap

        # action
        result = self.gate.transduce(inputs, True)
        # capture the printed outputs:
        sys.stdout = sys.__stdout__

        # assert
        self.assertEqual(result, outputs, "OUTPUT LIST INCORRECT")
        self.assertEqual(cap.getvalue(), printout, "VERBOSE INCORRECT")
        pass

    def teat_car_coming_to_gate_not_braking_violation(self):
        """  
        test what happen when car just ran over the gate
        """
        pass

    def test_car_exited_too_soon_violation(self):
        """  
        test what happen when car exited too son without waiting the gat goes to top
        """
        pass

    def test_car_exited_but_gate_not_closing_for_the_next_violation(self):
        """  
        test what happen when first car already exited 
        """
        pass

    