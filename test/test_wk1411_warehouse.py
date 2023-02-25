import os, sys, unittest

# set the code and test dir
test_dir = os.path.dirname(__file__)
code_dir = os.path.normpath(test_dir + "/../Lec_1")

sys.path.append(code_dir)

import wk1411_warehouse as s

class Test_warehouse(unittest.TestCase):

    def setUp(self) -> None:
        self.totals = {'a' : 10, 'b' : 20, 'c' : 5}
        self.w = s.Warehouse(self.totals)

    # test for def warehouseProcess
    def test_receive_commodities(self):
       self.assertEqual(s.werehouseProcess(self.totals, ['receive', 'a', 15]), {'a' : 25, 'b' : 20, 'c' : 5}) 
    
    def test_ship_commodities(self):
        self.assertEqual(s.werehouseProcess(self.totals, ['ship', 'b', 10]), {'a' : 10, 'b' : 10, 'c' : 5})

    def test_ship_not_enough_commodities(self):
        self.assertEqual(s.werehouseProcess(self.totals, ['ship', 'c', 10]), {'a' : 10, 'b' : 20, 'c' : 5})

    def test_receive_new_commodities(self):
        self.assertEqual(s.werehouseProcess(self.totals, ['receive', 'd', 10]), {'a' : 10, 'b' : 20, 'c' : 5, 'd' : 10})
    
    def test_ship_unavailable_commodities(self):
        self.assertEqual(s.werehouseProcess(self.totals, ['ship', 'd', 5]), {'a' : 10, 'b' : 20, 'c' : 5})

    # test for class Warehouse:
    def test_init_commodities_total_lookup(self):
        self.assertEqual(self.w.lookoup('a'), 10, "a is incorrect lookup")
        self.assertEqual(self.w.lookoup('b'), 20, "b is incorrect lookup")
        self.assertEqual(self.w.lookoup('c'), 5, "c is incorrect lookup")
        self.assertEqual(self.w.lookoup('d'), 0, "d is incorrect lookup should be returning 0")

    def test_receive_commodities_in_Warehouse_class(self):
        # prep
        self.w.process(('receive', 'a', 10))
        # assert:
        self.assertEqual(self.w.lookoup('a'), 20)
    
    def test_ship_commodities_in_warehouse(self):
        self.w.process(('ship', 'b', 7))
        self.assertEqual(self.w.lookoup('b'), 13)
    
    def test_receive_new_commodities_in_warehouse(self):
        self.w.process(('receive', 'd', 7))
        self.assertEqual(self.w.lookoup('d'), 7)
        self.assertEqual(self.w.lookoup('a'), 10, "a lookoup is incorrect")

    def test_ship_insufficient_available_totals_commodity_raise_value_error(self):
        with self.assertRaises(ValueError) as e:
            self.w.process(('ship', 'c', 15))

        # test the totals integrity
        self.assertEqual(self.w.lookoup('c'), 5)
        self.assertTrue("insufficient available items to ship from warehouse" in e.exception.args)
    
    def test_ship_unidentified_commodity_raises_value_error(self):
        with self.assertRaises(ValueError) as e:
            self.w.process(('ship', 'd', 10))

        # check the totals integrity
        self.assertEqual(self.w.lookoup('d'), 0, "totals compormised on d")
        self.assertTrue("unidentified commodity in the warehouse" in e.exception.args)

    def test_unidentified_order_raises_value_error(self):
        with self.assertRaises(ValueError) as e:
            self.w.process(('count', 'b', 15))
        
        # test the integrrity of the totals dict
        self.assertEqual(self.w.lookoup('b'), 20, "totals b compormised should be 20")
        self.assertTrue("unidentified order given" in e.exception.args)

if __name__ == '__main__':
    unittest.main()