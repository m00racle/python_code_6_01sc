import os, sys, unittest

# set the code and test dir
test_dir = os.path.dirname(__file__)
code_dir = os.path.normpath(test_dir + "/../Lec_1")

sys.path.append(code_dir)

import wk1410_fruit_class as s

class Test_fruit_class(unittest.TestCase):

    def setUp(self) -> None:
        self.salad = s.FruitSalad(['bananas', 'apples'], 2)
        return super().setUp()
    
    def test_attribute_ori_class(self):
        self.assertEqual(s.FruitSalad.fruits, ['melons', 'pineapples'])
    
    def test_attibute_ori_serving(self):
        self.assertEqual(s.FruitSalad.servings, 4)
    
    def test_attribute_fruits_in_salad(self):
        self.assertEqual(self.salad.fruits, ['bananas', 'apples'])

    def test_attribute_init_servings_in_salad(self):
        self.assertEqual(self.salad.servings, 2)

    def test_str_method_of_salad_instance_object(self):
        self.assertEqual(str(self.salad), "2 servings of fruit salad with ['bananas', 'apples']")

    def test_add_function_append_fruit_string_to_fruits_in_salad(self):
        # preps
        self.salad.add('guavas')
        self.assertEqual(self.salad.fruits, ['bananas', 'apples', 'guavas'])

    def test_servings_of_salad_instance(self):
        for i in range(self.salad.servings):
            self.assertEqual(self.salad.serve(), 'enjoy')
        
        self.assertEqual(self.salad.serve(), 'sorry')
