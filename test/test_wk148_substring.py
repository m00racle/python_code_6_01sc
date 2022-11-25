import os
import sys

# set the code and test dir
test_dir = os.path.dirname(__file__)
code_dir = os.path.normpath(test_dir + "/../Lec_1")

sys.path.append(code_dir)

import unittest

import wk148_substring as s

class Test_substring(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_substring_is_true(self):
        self.assertTrue(s.isSubstring('barfoobar', 'foo'))

    def test_substing_is_false(self):
        self.assertFalse(s.isSubstring('barfoobar', 'fot'))
    
    def test_substring_in_the_end(self):
        self.assertTrue(s.isSubstring('barfotfoo', 'foo'))

    