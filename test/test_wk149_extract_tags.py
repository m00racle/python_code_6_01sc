import os, sys

# set the code and test dir
test_dir = os.path.dirname(__file__)
code_dir = os.path.normpath(test_dir + "/../Lec_1")

sys.path.append(code_dir)

import unittest
import wk149_extract_tags as s

class Test_extract_tags(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_extract_tags_simple(self):
        self.assertEqual(s.extractTags('[fizz] thing [/fizz] fuzz [zip]'), ['fizz', '/fizz', 'zip'])

    def test_using_single_middle_bracket(self):
        self.assertEqual(s.extractTags('test [using the [] as bracket'), ['using the ['])

    def test_assert_error_end_side(self):
        with self.assertRaises(IndexError) as e:
            s.extractTags('trial [being] judged [by the final move')

        self.assertTrue("invalid tag detected: no enclosure" in e.exception.args)

    def test_assert_error_mistype_closure(self):
        with self.assertRaises(IndexError) as e:
            s.extractTags('this is [mistyped] version [of the[ trial')

        self.assertTrue("invalid tag detected: no enclosure" in e.exception.args)

    def test_assert_error_start_side(self):
        with self.assertRaises(IndexError) as e:
            s.extractTags('this [example [of what ] we want to] test')

        self.assertTrue("invalid tag detected: no enclosure" in e.exception.args)
    