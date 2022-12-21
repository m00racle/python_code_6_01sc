import os, sys, unittest, io

# set the code and test dir
test_dir = os.path.dirname(__file__)
code_dir = os.path.normpath(test_dir + "/../Lec_2_State_Machine")

sys.path.append(code_dir)
"""  
Test page for Feedback combinator
"""

# import from file targeted for testing
from feedback_sm import Feedback

class TestFeedback(unittest.TestCase):
    """  
    test scenario for Feedback class
    """