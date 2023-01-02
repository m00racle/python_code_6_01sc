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

    def proposed_test_increment_feedback_output(self):
        """  
        Test the output only for the incrementer state machine implementing feedback
        NOTE: I need means to limit the run of the feedback to prevent infinite loop.
        """
        self.fail("NO TEST")

    def proposed_test_increment_feedback_verbose(self):
        """  
        test the verbose printed output of the increment state machine

        """
        self.fail("NO TEST")