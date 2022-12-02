import os, sys, unittest, io

# set the code and test dir
test_dir = os.path.dirname(__file__)
code_dir = os.path.normpath(test_dir + "/../Lec_2_State_Machine")

sys.path.append(code_dir)

import parking_gate as pg

class TestParkingGate(unittest.TestCase):
    """  
    Test for Parking Gate state machine
    """
    def test_car_coming_and_existing_normal_scenario(self):
        """  
        test the parking gate state machine based on normal scenarion
        no violation here
        """
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

    