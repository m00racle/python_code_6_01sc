import os, sys, unittest, io

# set the code and test dir
test_dir = os.path.dirname(__file__)
code_dir = os.path.normpath(test_dir + "/../Lec_2_State_Machine")

sys.path.append(code_dir)

from parallel import Parallel, Parallel2, ParallelAdd
from state_machine import Accumulator, Average2, UpDown

class TestParallel(unittest.TestCase):
    """  
    unit test for Parallel class implementations
    """
    # : develop scenario for testing purposes
    def test_parallel_all_valid_data(self):
        """  
        Pretty simple test:
        have 2 SM accumulator and Average2 working at parallel with 1 shared inputs
        Only assert the outputs since this is all valid data
        """
        sm1 = Accumulator(5)
        sm2 = Average2()
        inputs = [2,5,-9,100]
        expected_outputs = [(7, 1.0), (12, 3.5), (3, -2.0), (103, 45.5)]

        # preps the instance 
        p = Parallel(sm1, sm2)
        # action 
        outputs = p.transduce(inputs)

        # assert
        self.assertEqual(outputs, expected_outputs, "OUTPUT INCORRECT")

    def test_parallel_with_shared_invalid_data(self):
        """  
        Test two different SM Accumulator and UpDown
        the input will be mixed with valid for one SM and invalid to another
        
        Accumulator:
        sub class of SM which implementation is Accumulator State Machine
        fn(s,i) = s + i
        fo(s,i) = s + i
        startState : user defined

        error handling function:
        efn(s,i) = s
        efo(s,i) = None

        UpDown:
        class for Up Down counter State Machine subcalss of SM
        S = integers
        I = {u,d}
        O = integers
        startState : user defined
        fn(s,i) =
            s + 1 if i = u
            s - 1 if i = d
        
        fo(s,i) = fn(s,i)

        error handling function
        efn(s,i) = s (the state unchanged in error)
        efo(s,i) = None (the output is None in error)

        I want to verbose output since I want to test the states also
        """
        sm1 = Accumulator()
        sm2 = UpDown(10)
        p = Parallel(sm1, sm2)
        inputs = [1,'u', 5, 6,'u', 'd', 'd' ]
        expected_result = [(1, None), (None, 11), (6, None), (12, None), (None, 12), (None, 11), (None, 10)]
        # we expect printed output
        # print(f"In: {inp} Out: {o} Next State: {s}")
        should_print = \
            "Start state: (0, 10)\n" +\
            "In: 1 Out: (1, None) Next State: (1, 10)\n" +\
            "In: u Out: (None, 11) Next State: (1, 11)\n" +\
            "In: 5 Out: (6, None) Next State: (6, 11)\n" +\
            "In: 6 Out: (12, None) Next State: (12, 11)\n" +\
            "In: u Out: (None, 12) Next State: (12, 12)\n" +\
            "In: d Out: (None, 11) Next State: (12, 11)\n" +\
            "In: d Out: (None, 10) Next State: (12, 10)\n"
        
        # preps to catch the printed output:
        r = io.StringIO()
        sys.stdout = r
        
        # action:
        result = p.transduce(inputs, verbose=True)
        sys.stdout = sys.__stdout__
        printed_out = r.getvalue()

        # assert:
        self.assertEqual(result, expected_result, "THE OUTPUT INCORRECT")
        self.assertEqual(printed_out, should_print, "PRINTED OUT INCORRECT")

class TestParallel2(unittest.TestCase):
    """  
    Test cases for class Parallel2 State Machine
    In this case there will be one important function called splitValue
    I think splitValue required modes:
    if the inputs are serial, tuples and so on.
    """
    def proposed_test_combining_two_inputs(self):
        """  
        PROPOSED (PENDING DESIGN FOR FUTURE DEVS)
        : find a scenario that can be test the inputs when passed as __init__
        the inputs passed for arguments will be two separate list
        Then in the init it should be combined to form valid inputs for the SM.
        : find a way to know the input?? Maybe using transduce verbose?? IT IS ALWAYS GOOD FOR TEST
        """
        sm1 = Accumulator()
        inp_1 = [1,5,7,13,15]
        sm2  = UpDown(5)
        inp_2 = ['d', 'u', 'u']
        p2 = Parallel2(sm1, sm2)
        expected_print = \
            "Start state: (0, 5)\n" +\
            "In: (1, 'd') Out: (1, 4) Next State: (1, 4)\n" +\
            "In: (5, 'u') Out: (6, 5) Next State: (6, 5)\n" +\
            "In: (7, 'u') Out: (13, 6) Next State: (13, 6)\n" +\
            "In: (13, None) Out: (26, None) Next State: (26, 6)\n" +\
            "In: (15, None) Out: (41, None) Next State: (41, 6)\n" 
        must_result = [(1,4), (6,5), (13,6), (26, None), (41, None)]
        # preps to catch the printed output:
        r = io.StringIO()
        sys.stdout = r
        
        # action:
        result = p2.transduce(inp_1, inp_2, verbose=True)
        sys.stdout = sys.__stdout__
        printed_out = r.getvalue()

        # assert
        self.assertEqual(result, must_result, "output is wrong")
        self.assertEqual(printed_out, expected_print, "print out is wrong")


    def test_split_value_function_verify_correct_pair(self):
        """  
        split_value function will pass the input that was pair (tuple or list)
        """
        sm1 = Accumulator()
        
        sm2  = UpDown(5)
        
        inputs = [(1,'d'), (5, 'u'), (7, 'u'), (13, None), (15, None)]
        p2 = Parallel2(sm1, sm2)
        expected_print = \
            "Start state: (0, 5)\n" +\
            "In: (1, 'd') Out: (1, 4) Next State: (1, 4)\n" +\
            "In: (5, 'u') Out: (6, 5) Next State: (6, 5)\n" +\
            "In: (7, 'u') Out: (13, 6) Next State: (13, 6)\n" +\
            "In: (13, None) Out: (26, None) Next State: (26, 6)\n" +\
            "In: (15, None) Out: (41, None) Next State: (41, 6)\n" 
        must_result = [(1,4), (6,5), (13,6), (26, None), (41, None)]
        # preps to catch the printed output:
        r = io.StringIO()
        sys.stdout = r
        
        # action:
        result = p2.transduce(inputs, verbose=True)
        sys.stdout = sys.__stdout__
        printed_out = r.getvalue()

        # assert
        self.assertEqual(result, must_result, "output is wrong")
        self.assertEqual(printed_out, expected_print, "print out is wrong")
        

    def proposed_test_using_serial_inputs_transduce_correct_print_out(self):
        """  
        PORPOSED: PENDING FOR FUTURE DEVS
        This will use valid inputs but in series
        should be able to still separate them
        """
        sm1 = Accumulator()
        
        sm2  = UpDown(5)
        
        inputs = [1,'d', 5, 'u', 7, 'u', 13, None, 15, None]
        p2 = Parallel2(sm1, sm2)
        expected_print = \
            "Start state: (0, 5)\n" +\
            "In: (1, 'd') Out: (1, 4) Next State: (1, 4)\n" +\
            "In: (5, 'u') Out: (6, 5) Next State: (6, 5)\n" +\
            "In: (7, 'u') Out: (13, 6) Next State: (13, 6)\n" +\
            "In: (13, None) Out: (26, None) Next State: (26, 6)\n" +\
            "In: (15, None) Out: (41, None) Next State: (41, 6)\n" 
        must_result = [(1,4), (6,5), (13,6), (26, None), (41, None)]
        # preps to catch the printed output:
        r = io.StringIO()
        sys.stdout = r
        
        # action:
        result = p2.transduce(inputs, verbose=True)
        sys.stdout = sys.__stdout__
        printed_out = r.getvalue()

        # assert
        self.assertEqual(result, must_result, "output is wrong")
        self.assertEqual(printed_out, expected_print, "print out is wrong")
        
    
    def test_transduce_verbose_invalid_inputs_retains_state_returns_undefined(self):
        """  
        test transduce with invalid inputs for each or both of the state machine
        inputs to be valid through splitValue function if it is NOT 'undefined' 
        then it must be a tuple with len(tuple) == 2 (exactly 2 no more no less)
        """
        sm1 = Accumulator()
        
        sm2  = UpDown(5)
        
        inputs = [(1,'d'), (5, 'u'), 'undefined', ('undefined', None), (13,)]
        p2 = Parallel2(sm1, sm2)
        expected_print = \
            "Start state: (0, 5)\n" +\
            "In: (1, 'd') Out: (1, 4) Next State: (1, 4)\n" +\
            "In: (5, 'u') Out: (6, 5) Next State: (6, 5)\n" +\
            "In: undefined Out: ('undefined', 'undefined') Next State: (6, 5)\n" +\
            "In: ('undefined', None) Out: ('undefined', 'undefined') Next State: (6, 5)\n" +\
            "In: (13,) Out: ('undefined', 'undefined') Next State: (6, 5)\n" 
        must_result = [(1,4), (6,5), ('undefined', 'undefined'), ('undefined', 'undefined'), ('undefined', 'undefined')]
        # preps to catch the printed output:
        r = io.StringIO()
        sys.stdout = r
        
        # action:
        result = p2.transduce(inputs, verbose=True)
        sys.stdout = sys.__stdout__
        printed_out = r.getvalue()

        # assert
        self.assertEqual(result, must_result, "output is wrong")
        self.assertEqual(printed_out, expected_print, "print out is wrong")
        
class TestParallelAdd(unittest.TestCase):
    """  
    to test the ParallelAdd class.
    """
    def test_valid_inputs_returns_valid_outputs(self):
        sm1 = Accumulator(5)
        sm2 = Average2()
        inputs = [2,5,-9,100]
        expected_outputs = [8.0, 15.5, 1.0, 148.5]

        # preps the instance 
        p = ParallelAdd(sm1, sm2)
        # action 
        outputs = p.transduce(inputs)

        # assert
        self.assertEqual(outputs, expected_outputs, "OUTPUT INCORRECT")

    def test_invalid_inputs_returns_none_and_retain_state(self):
        """  
        test case when passing invalid inputs
        """
        """  
        Test two different SM Accumulator and UpDown
        the input will be mixed with valid for one SM and invalid to another
        
        Accumulator:
        sub class of SM which implementation is Accumulator State Machine
        fn(s,i) = s + i
        fo(s,i) = s + i
        startState : user defined

        error handling function:
        efn(s,i) = s
        efo(s,i) = None

        UpDown:
        class for Up Down counter State Machine subcalss of SM
        S = integers
        I = {u,d}
        O = integers
        startState : user defined
        fn(s,i) =
            s + 1 if i = u
            s - 1 if i = d
        
        fo(s,i) = fn(s,i)

        error handling function
        efn(s,i) = s (the state unchanged in error)
        efo(s,i) = None (the output is None in error)

        I want to verbose output since I want to test the states also
        """
        sm1 = Accumulator()
        sm2 = UpDown(10)
        p = ParallelAdd(sm1, sm2)
        inputs = [1,'u', 5, 6,'u', 'd', 'd' ]
        expected_result = [None, None, None, None, None, None, None]
        # we expect printed output
        # print(f"In: {inp} Out: {o} Next State: {s}")
        should_print = \
            "Start state: (0, 10)\n" +\
            "In: 1 Out: None Next State: (0, 10)\n" +\
            "In: u Out: None Next State: (0, 10)\n" +\
            "In: 5 Out: None Next State: (0, 10)\n" +\
            "In: 6 Out: None Next State: (0, 10)\n" +\
            "In: u Out: None Next State: (0, 10)\n" +\
            "In: d Out: None Next State: (0, 10)\n" +\
            "In: d Out: None Next State: (0, 10)\n"
        
        # preps to catch the printed output:
        r = io.StringIO()
        sys.stdout = r
        
        # action:
        result = p.transduce(inputs, verbose=True)
        sys.stdout = sys.__stdout__
        printed_out = r.getvalue()

        # assert:
        self.assertEqual(result, expected_result, "THE OUTPUT INCORRECT")
        self.assertEqual(printed_out, should_print, "PRINTED OUT INCORRECT")
        