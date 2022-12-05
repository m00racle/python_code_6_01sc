import os, sys, unittest, io

# set the code and test dir
test_dir = os.path.dirname(__file__)
code_dir = os.path.normpath(test_dir + "/../Lec_2_State_Machine")

sys.path.append(code_dir)

from parallel import Parallel

class TestParallel(unittest.TestCase):
    """  
    unit test for Parallel class implementations
    """
    # TODO: develop scenario for testing purposes