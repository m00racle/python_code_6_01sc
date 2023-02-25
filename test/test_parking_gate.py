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
        

    def test_car_coming_and_existing_normal_scenario(self):
        """  
        test the parking gate state machine based on normal scenarion
        no violation here
        """
        # arrange
        inputs = [('bottom', False, False), ('bottom', True, False), ('bottom', True, False), ('middle', True, False), ('middle', True, False), ('middle', True, False), ('top', True, False), ('top', True, False), ('top', True, False), ('top', True, True), ('top', True, True), ('top', True, False), ('middle', True, False), ('middle', True, False), ('middle', True, False), ('bottom', True, False), ('bottom', True, False)]

        outputs = ['nop', 'lift', 'lift', 'lift', 'lift', 'lift', 'nop', 'nop', 'nop', 'drop', 'drop', 'drop', 'drop', 'drop', 'drop', 'nop', 'lift']

        printout = \
            "Start state: waiting\n" +\
            "In: ('bottom', False, False) Out: nop Next State: waiting\n" +\
            "In: ('bottom', True, False) Out: lift Next State: raising\n" +\
            "In: ('bottom', True, False) Out: lift Next State: raising\n" +\
            "In: ('middle', True, False) Out: lift Next State: raising\n" +\
            "In: ('middle', True, False) Out: lift Next State: raising\n" +\
            "In: ('middle', True, False) Out: lift Next State: raising\n" +\
            "In: ('top', True, False) Out: nop Next State: raised\n" +\
            "In: ('top', True, False) Out: nop Next State: raised\n" +\
            "In: ('top', True, False) Out: nop Next State: raised\n" +\
            "In: ('top', True, True) Out: drop Next State: lowering\n" +\
            "In: ('top', True, True) Out: drop Next State: lowering\n" +\
            "In: ('top', True, False) Out: drop Next State: lowering\n" +\
            "In: ('middle', True, False) Out: drop Next State: lowering\n" +\
            "In: ('middle', True, False) Out: drop Next State: lowering\n" +\
            "In: ('middle', True, False) Out: drop Next State: lowering\n" +\
            "In: ('bottom', True, False) Out: nop Next State: waiting\n" +\
            "In: ('bottom', True, False) Out: lift Next State: raising\n"
        
        cap = io.StringIO()
        sys.stdout = cap

        # action
        result = self.gate.transduce(inputs, True)
        # capture the printed outputs:
        sys.stdout = sys.__stdout__

        # assert
        self.assertEqual(result, outputs, "OUTPUT LIST INCORRECT")
        self.assertEqual(cap.getvalue(), printout, "VERBOSE INCORRECT")

    def test_car_coming_to_gate_run_off_violation(self):
        """  
        test what happen when car just ran over the gate
        """
        # SCENARIO: car just run trough the gate
        inputs = [('bottom', False, False), ('bottom', True, False), ('bottom', False, True)]

        # assert 
        # with self.assertRaises(Exception) as e:
        #     self.gate.transduce(inputs)
        
        # self.assertTrue(type(e.exception) is pg.RunOverViolation, "TYPE OF EXCEPTION IS WRONG")
        self.assertTrue(self.gate.transduce(inputs), ['nop', 'lift', 'ALERT! run off'])
        self.assertEqual(self.gate.getState(), 'halt', "Violation state is wrong")

        # RESET THE GATE
        self.gate.start()
        # SCENARIO: car just run trough the gate
        inputs = [('bottom', False, False), ('bottom', False, True)]

        # assert 
        # with self.assertRaises(Exception) as e:
        #     self.gate.transduce(inputs)
        
        # self.assertTrue(type(e.exception) is pg.RunOverViolation, "TYPE OF EXCEPTION IS WRONG")
        self.assertEqual(self.gate.transduce(inputs), ['nop', 'ALERT! run off'])
        self.assertEqual(self.gate.getState(), 'halt', "Violation state is wrong")

        

    def test_car_exited_too_soon_violation(self):
        """  
        test what happen when car exited too son without waiting the gat goes to top
        """
         # SCENARIO: car exit too son hit the gate:
        inputs = [('bottom', False, False), ('bottom', True, False), ('middle', False, True)]

        # assert 
        # with self.assertRaises(Exception) as e:
        #     self.gate.transduce(inputs)
        
        # self.assertTrue(type(e.exception) is pg.TooSoonViolation, "TYPE OF EXCEPTION IS FALSE")
        self.assertEqual(self.gate.transduce(inputs), ['nop', 'lift', 'ALERT! too soon'])
        self.assertEqual(self.gate.getState(), 'halt', "Violation state is wrong")

        # SCENARIO: car exit while gate is lowering:
        inputs = [('bottom', False, False), ('bottom', True, False), ('middle', True, False), ('top', True, False), ('top', True, True), ('middle', False, True)]
        
        # # assert 
        # with self.assertRaises(Exception) as e:
        #     self.gate.transduce(inputs)
        
        # self.assertTrue(type(e.exception) is pg.TooSoonViolation, "TYPE OF EXCEPTION IS FALSE")
        self.assertEqual(self.gate.transduce(inputs), ['nop', 'lift', 'lift', 'nop', 'drop', 'ALERT! too soon'])
        self.assertEqual(self.gate.getState(), 'halt', "Violation state is wrong")

    def test_verbose_violations(self):
        """  
        test as amy violation as possible
        """
        # arrange
        inputs = [('bottom', False, True), ('bottom', True, False), ('restart', False, False), ('bottom', True, False), ('middle', True, False), ('middle', True, False), ('top', True, False), ('top', True, False), ('top', True, False), ('top', True, True), ('top', True, True), ('top', True, False), ('middle', False, True), ('middle', True, False), ('restart', True, False), ('middle', True, False), ('top', True, False)]

        outputs = ['ALERT! run off', 'ALERT! run off', 'nop', 'lift', 'lift', 'lift', 'nop', 'nop', 'nop', 'drop', 'drop', 'drop', 'ALERT! too soon', 'ALERT! too soon', 'nop', 'lift', 'nop']

        printout = \
            "Start state: waiting\n" +\
            "In: ('bottom', False, True) Out: ALERT! run off Next State: halt\n" +\
            "In: ('bottom', True, False) Out: ALERT! run off Next State: halt\n" +\
            "In: ('restart', False, False) Out: nop Next State: waiting\n" +\
            "In: ('bottom', True, False) Out: lift Next State: raising\n" +\
            "In: ('middle', True, False) Out: lift Next State: raising\n" +\
            "In: ('middle', True, False) Out: lift Next State: raising\n" +\
            "In: ('top', True, False) Out: nop Next State: raised\n" +\
            "In: ('top', True, False) Out: nop Next State: raised\n" +\
            "In: ('top', True, False) Out: nop Next State: raised\n" +\
            "In: ('top', True, True) Out: drop Next State: lowering\n" +\
            "In: ('top', True, True) Out: drop Next State: lowering\n" +\
            "In: ('top', True, False) Out: drop Next State: lowering\n" +\
            "In: ('middle', False, True) Out: ALERT! too soon Next State: halt\n" +\
            "In: ('middle', True, False) Out: ALERT! too soon Next State: halt\n" +\
            "In: ('restart', True, False) Out: nop Next State: waiting\n" +\
            "In: ('middle', True, False) Out: lift Next State: raising\n" +\
            "In: ('top', True, False) Out: nop Next State: raised\n"
        
        cap = io.StringIO()
        sys.stdout = cap

        # action
        result = self.gate.transduce(inputs, True)
        # capture the printed outputs:
        sys.stdout = sys.__stdout__

        # assert
        self.assertEqual(result, outputs, "OUTPUT LIST INCORRECT")
        self.assertEqual(cap.getvalue(), printout, "VERBOSE INCORRECT")

if __name__ == '__main__':
    unittest.main()