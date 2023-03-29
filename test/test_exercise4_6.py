import os, sys, unittest

# set test directory
test_dir = os.path.dirname(__file__)
code_dir = os.path.normpath(test_dir + "/../Lec_2_State_Machine")

sys.path.append(code_dir)

from exercise4_6 import Exercise1b, Exercise1cHelper
from state_machine import Repeat

class TestExercise4_6(unittest.TestCase):
    def setUp(self) -> None:
        self.inputs = [1, 2, 3, 100, 4, 9, 500, 51, -2, 57, 103, 1, 1, 1, 1, -10, 207, 3, 1]
        self.expected = [1, 3, 6, 106, 4, 13, 513, 51, 49, 106]

    def test_exercise_4_6_1_B(self):
        self.assertEqual(Exercise1b().transduce(self.inputs), self.expected)

    def test_exercise_4_6_1_C(self):
        newSM = Repeat(Exercise1cHelper, 3)
        self.assertEqual(newSM.transduce(self.inputs), self.expected)