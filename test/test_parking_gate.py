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