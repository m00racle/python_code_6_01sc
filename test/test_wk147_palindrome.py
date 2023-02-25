import os
import sys

# set the code and test dir
test_dir = os.path.dirname(__file__)
code_dir = os.path.normpath(test_dir + "/../Lec_1")

sys.path.append(code_dir)

import unittest

import wk147_palindrome as s

class Test_Palindrome(unittest.TestCase):
    
    def setUp(self) -> None:
        return super().setUp()

    def test_is_palindrome_true(self):
        self.assertTrue(s.isPalindrome('able was I ere I saw elba'))

    def test_is_palindrome_false(self):
        self.assertFalse(s.isPalindrome('a man a plan a canal panama'))

if __name__ == '__main__':
    unittest.main()