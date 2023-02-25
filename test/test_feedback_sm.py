import os, sys, unittest, io

# set the code and test dir
test_dir = os.path.dirname(__file__)
code_dir = os.path.normpath(test_dir + "/../Lec_2_State_Machine")

sys.path.append(code_dir)
"""  
Test page for Feedback combinator
"""

# import from file targeted for testing
from feedback_sm import Feedback, FeedbackAdd, FeedbackSub, Feedback2
from cascade import Cascade
from state_machine import Increment, Delay, Negation, Adder, Wire, Gain, Multiplier
from parallel import Parallel

class TestFeedback(unittest.TestCase):
    """  
    test scenario for Feedback class
    """

    def test_increment_feedback_output(self):
        """  
        Test the output only for the incrementer state machine implementing feedback
        NOTE: I need means to limit the run of the feedback to prevent infinite loop.
        """
        # arrange
        f = Feedback(Cascade(Increment(2), Delay(3)))
        # assert
        self.assertEqual(f.run(), [3,5,7,9,11,13,15,17,19,21])

    def test_feedback_negation(self):
        f = Feedback(Cascade(Negation(), Delay(False)))
        # assert
        self.assertEqual(f.run(5), [False, True, False, True, False])

    def test_fibonacci_feedback(self):
        fib = Feedback(Cascade(Parallel(Delay(1), Cascade(Delay(1), Delay(0))), Adder()))
        self.assertEqual(fib.run(), [1, 2, 3, 5, 8, 13, 21, 34, 55, 89] )

    def test_factorial_using_Feedback2(self):
        """  
        build factorial state machine using combination of: Feedback, 
        """
        # arrange
        counter = Feedback(Cascade(Increment(1), Delay(1)))
        fact = Cascade(counter, Feedback2(Cascade(Multiplier(), Delay(1))))

        # assert
        self.assertEqual(fact.run(), [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880])

class TestFeedbackAdd(unittest.TestCase):
    """  
    test scenario for FeedbackAdd class
    """
    def test_transduce_sequence_output_sum_all_inputs(self):
        """  
        transduce [0,1,2,3,4,5,6,7,8,9]
        return [0,0,1,3,6,10,15,21,28,36]
        """
        # arrange
        fa = FeedbackAdd(Delay(0), Wire())
        # assert
        self.assertEqual(fa.transduce(range(10)), [0,0,1,3,6,10,15,21,28,36])

    def test_transduce_using_gain_instead_of_wire(self):
        """  
        transduce [0,1,2,3,4,5,6,7,8,9]
        return [0,0,1,3,6,10,15,21,28,36]
        """
        fa = FeedbackAdd(Delay(0), Gain(1.0))
        # assert
        self.assertEqual(fa.transduce(range(10)), [0,0,1,3,6,10,15,21,28,36])

    def test_non_delay_return_raise_type_error_none(self):
        fb = FeedbackAdd(Wire(), Wire())
        # assert
        self.assertEqual(fb.transduce(range(10)), [None] * 10)

class TestFeedbackSub(unittest.TestCase):
    """  
    Test scenario for FeedbackSub class
    """
    def test_transduce_sequence_output_sum_all_inputs(self):
        """  
        transduce [0,1,2,3,4,5,6,7,8,9]
        return [0,0,1,3,6,10,15,21,28,36]
        """
        # arrange
        fs = FeedbackSub(Delay(0), Wire())
        # assert
        self.assertEqual(fs.transduce(range(10)), [0,0,1,1,2,2,3,3,4,4])

    def test_transduce_using_gain_instead_of_wire(self):
        """  
        transduce [0,1,2,3,4,5,6,7,8,9]
        return [0,0,1,3,6,10,15,21,28,36]
        """
        # arrange
        fs = FeedbackSub(Delay(0), Gain(1.0))
        # assert
        self.assertEqual(fs.transduce(range(10)), [0,0,1,1,2,2,3,3,4,4])

    def test_non_delay_return_raise_type_error_none(self):
        fb = FeedbackSub(Wire(), Wire())
        # assert
        self.assertEqual(fb.transduce(range(10)), [None] * 10)

if __name__ == '__main__':
    unittest.main()