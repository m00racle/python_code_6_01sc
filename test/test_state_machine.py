import os, sys, unittest, io

# set the code and test dir
test_dir = os.path.dirname(__file__)
code_dir = os.path.normpath(test_dir + "/../Lec_2_State_Machine")

sys.path.append(code_dir)

import state_machine as sm

class TestAccumulator(unittest.TestCase):
    def setUp(self) -> None:
        self.a = sm.Accumulator()
        self.a.start()
        self.b = sm.Accumulator(100)
        self.b.start()

    def test_init_default_accumulator_will_start_state_at_zero(self):
        # setup
        s = self.a.step(0) 
        # this to ensure we know the initial start state
        self.assertEqual(s, 0)
    
    def test_init_not_default_will_set_start_state_as_args(self):
        self.assertEqual(self.b.step(0), 100)

    def test_step_returns_correct_output_and_states(self):
        self.assertEqual(self.b.step(10), 110, "OUTPUT IS WRONG")
        self.assertEqual(self.b.step(0), 110, "state is wrong")
    
    def test_transduces_inputs_returns_correct_output_list(self):
        """  
        update: this test also include invalid inputs that should returns None
        and retain previous state
        """
        inps = [100, -3, 4, None, 10]
        comp = [100, 97, 101, None, 111]
        self.assertEqual(self.a.transduce(inps), comp)
    
    def test_transduce_verbose_print_steps_and_return_list(self):
        """  
        update: this test also include invalid inputs that should returns None
        and retain previous state
        """
        # setup
        inps = [100, -3, 4, 'q', 10]
        comp = [100, 97, 101, None, 111]
        # this is to capture printed message
        capOut = io.StringIO() 
        sys.stdout = capOut
        printed = \
                "Start state: 0\n" + \
                "In: 100 Out: 100 Next State: 100\n" + \
                "In: -3 Out: 97 Next State: 97\n" + \
                "In: 4 Out: 101 Next State: 101\n" + \
                "In: q Out: None Next State: 101\n" + \
                "In: 10 Out: 111 Next State: 111\n"
        
        # action
        out = self.a.transduce(inps, verbose=True)
        sys.stdout = sys.__stdout__
        self.assertEqual(out, comp, "the output list is WRONG")
        self.assertEqual(capOut.getvalue(), printed)

    def test_run_5_returns_5_None_list(self):
        self.assertEqual(self.b.run(5), [None, None, None, None, None])
    
class TestGainClass(unittest.TestCase):
    def setUp(self) -> None:
        self.g = sm.Gain(3)
        self.g.start()

    def test_transduce_gain_returns_correct_list(self):
        self.assertEqual(self.g.transduce([1.1, -2, 100, 5]), [3.3000000000000003, -6, 300, 15])

    def test_transduce_verbose_outputs_correct_outputs_and_states(self):
        capOout = io.StringIO()
        sys.stdout = capOout
        printed = \
                "Start state: 0\n" + \
                "In: 1.1 Out: 3.3000000000000003 Next State: 3.3000000000000003\n" + \
                "In: -2 Out: -6 Next State: -6\n" + \
                "In: 100 Out: 300 Next State: 300\n" + \
                "In: 5 Out: 15 Next State: 15\n"
        out = self.g.transduce([1.1, -2, 100, 5], True)
        sys.stdout = sys.__stdout__
        self.assertEqual(out, [3.3000000000000003, -6, 300, 15], "returns output is wrong")
        self.assertEqual(capOout.getvalue(), printed, "the step by step outputs and states are WRONG")
    
    def test_run_with_no_input_gain_returns_all_zero(self):
        self.assertEqual(self.g.run(), [0,0,0,0,0,0,0,0,0,0])
    
    def test_state_after_whole_runs_and_transduce_remains_the_same(self):
        self.g.run()
        self.assertEqual(self.g.getState(), 0, "state after run() is wrong supposed to be 3")
        self.g.transduce([1.1, -2, 100, 5])
        self.assertEqual(self.g.getState(), 15, "state after transduce is wrong suppose to be 3")

class TestAverage2Class(unittest.TestCase):
    def setUp(self) -> None:
        self.a = sm.Average2()
        self.a.start()

    def test_average_transducer_returns_list_of_correct_output_and_last_input_becomes_last_state(self):
        """  
        update: error handling function will retain the last valid state which can be used to handle valid input later on
        """
        self.assertEqual(self.a.transduce([100, -3, 4, None, 10]), [50, 48.5, 0.5, None, 7], "output list wrong")
        self.assertEqual(self.a.getState(), 10, "final state is wrong")
    
    def test_empty_input_run_returns_all_zero_and_final_state_zero(self):
        self.assertEqual(self.a.run(3), [None,None,None], "the empty run returns wrong")
        self.assertEqual(self.a.getState(), 0, "final state is wrong")
    
class TestLanguageAcceptorClass(unittest.TestCase):
    def setUp(self) -> None:
        self.abc = sm.ABC()
        self.abc.start()
    
    def test_start_state_starts_from_zero(self):
        self.assertEqual(self.abc.getState(), 0)

    def test_transduce_all_same_input_reuturn_false_mostly_verbosely(self):
        # set
        capOut = io.StringIO()
        sys.stdout = capOut
        # action
        result = self.abc.transduce(['a', 'a', 'a'], verbose = True)
        sys.stdout = sys.__stdout__
        printed = "Start state: 0\nIn: a Out: True Next State: 1\nIn: a Out: False Next State: 3\nIn: a Out: False Next State: 3\n"
        # assert
        self.assertEqual(result, [True, False, False], "outputs are wrong")
        self.assertEqual(capOut.getvalue(), printed, "printed out WRONG")

    def test_transduce_changing_input_returns_and_print_proper_outputs(self):
        # set
        capOut = io.StringIO()
        sys.stdout = capOut
        # action
        result = self.abc.transduce(['a', 'b', 'c', 'a', 'c', 'a', 'b'], verbose = True)
        sys.stdout = sys.__stdout__
        printed = "Start state: 0\nIn: a Out: True Next State: 1\nIn: b Out: True Next State: 2\nIn: c Out: True Next State: 0\nIn: a Out: True Next State: 1\nIn: c Out: False Next State: 3\nIn: a Out: False Next State: 3\nIn: b Out: False Next State: 3\n"
        # assert
        self.assertEqual(result, [True, True, True, True, False, False, False], "outputs are wrong")
        self.assertEqual(capOut.getvalue(), printed, "printed out WRONG")

    def test_run_empty_inputs_return_false_and_state_3(self):
        self.assertEqual(self.abc.run(3), [False, False, False], "outputs WRONG")
        self.assertEqual(self.abc.getState(), 3, "Final state is wrong")
        
class TestUpDownClass(unittest.TestCase):
    """  
    tests for class UpDown(SM)
    """
    # : get all specification tested here
    def test_up_down_from_negative_start_returns_correct_list_sequence(self):
        # setup
        ud = sm.UpDown(-2)
        ud.start()
        self.assertEqual(ud.transduce(['u', 'u', 'u', 'd', 'd', 'u']), [-1, 0, 1, 0, -1, 0])

    def test_up_down_transduce_verbose_output_returns_correct_outputs(self):
        # set
        ud = sm.UpDown()
        ud.start()
        capOut = io.StringIO()
        sys.stdout = capOut
        # action
        result = ud.transduce(['u', 'u', 'u', 'd', 'd', 'u'], verbose = True)
        sys.stdout = sys.__stdout__
        printed = \
            "Start state: 0\n" +\
            "In: u Out: 1 Next State: 1\n"+\
            "In: u Out: 2 Next State: 2\n"+\
            "In: u Out: 3 Next State: 3\n"+\
            "In: d Out: 2 Next State: 2\n"+\
            "In: d Out: 1 Next State: 1\n"+\
            "In: u Out: 2 Next State: 2\n"
        # assert
        self.assertEqual(result, [1, 2, 3, 2, 1, 2], "output list is INCORRECT")
        self.assertEqual(capOut.getvalue(), printed, "printed output is incorrect")
    
    def test_Up_down_run_with_none_input_returns_constant_state(self):
        # set
        ud = sm.UpDown(1)
        ud.start()
        capOut = io.StringIO()
        sys.stdout = capOut
        # action
        result = ud.transduce([None, None, None, None, None, None], verbose = True)
        sys.stdout = sys.__stdout__
        printed = \
            "Start state: 1\n" +\
            "In: None Out: None Next State: 1\n"+\
            "In: None Out: None Next State: 1\n"+\
            "In: None Out: None Next State: 1\n"+\
            "In: None Out: None Next State: 1\n"+\
            "In: None Out: None Next State: 1\n"+\
            "In: None Out: None Next State: 1\n"
        # assert
        self.assertEqual(result, [None, None, None, None, None, None], "output list is INCORRECT")
        self.assertEqual(capOut.getvalue(), printed, "printed output is incorrect")

    def test_invalid_input_handled_type_error(self):
        """  
        when pass invalid input to the transducer thus to getNextValue 
        It should be handled instead raising type error exception
        thus it still should return output = None and state = state
        """
        # set
        ud = sm.UpDown()
        ud.start()
        capOut = io.StringIO()
        sys.stdout = capOut
        # action
        result = ud.transduce(['u', 'u', True, 'd', 'di', 'u'], verbose = True)
        sys.stdout = sys.__stdout__
        printed = \
            "Start state: 0\n" +\
            "In: u Out: 1 Next State: 1\n"+\
            "In: u Out: 2 Next State: 2\n"+\
            "In: True Out: None Next State: 2\n"+\
            "In: d Out: 1 Next State: 1\n"+\
            "In: di Out: None Next State: 1\n"+\
            "In: u Out: 2 Next State: 2\n"
        
        # assert
        self.assertEqual(result, [1, 2, None, 1, None, 2], "output list is INCORRECT")
        self.assertEqual(capOut.getvalue(), printed, "printed output is incorrect")

class TestDelayClass(unittest.TestCase):
    """  
    test for class Delay(SM)
    """
    # TODO: get all specs tested here for Delay State machine
    def test_given_any_start_state_any_input_step_woks(self):
        """  
        test start state any (in this case sting)
        make onw step pass different type as argument in this case int
        should return corect steps.
        """
        d = sm.Delay('s')
        d.start()
        self.assertEqual(d.step(2), 's', "check output failed")
        self.assertEqual(d.getState(), 2, "next state is incorrect")
    
    def test_transduce_verbose_any_start_any_inputs_return_correct_list_and_printed(self):
        """  
        test None as start state
        input various data type int, string, boolean
        should return correct list
        should print correct output in verbose
        """
        # setup
        d = sm.Delay(None)
        d.start()
        capOut = io.StringIO()
        sys.stdout = capOut

        # action
        result = d.transduce([3, 'sit', True, -0.5], True)
        sys.stdout = sys.__stdout__
        printed =\
            "Start state: None\n" +\
            "In: 3 Out: None Next State: 3\n" +\
            "In: sit Out: 3 Next State: sit\n" +\
            "In: True Out: sit Next State: True\n" +\
            "In: -0.5 Out: True Next State: -0.5\n"
        
        # assert
        self.assertEqual(result, [None, 3, 'sit', True], "output list is wrong")
        self.assertEqual(capOut.getvalue(), printed)

    def test_run_none_input(self):
        """  
        test start state integer
        then call run(4) function 
        should return list of int and None
        """
        # arrange
        d = sm.Delay(100)
        d.start()
        # action and assert
        self.assertEqual(d.run(4), [100, None, None, None], "run() output is wrong")

class TestSumLast3(unittest.TestCase):
    """  
    class for Sum Last 3 components
    Specification:
    S = number (int and float)
    I = number (int and float)
    O = number (int and float)
    StartState = (0,0)

    fn(s,i) = (s[1], i)
    fo(s,i) = s[0] + s[1] + i

    error function:
    efn(s,i) = s
    efo(s,i) = None
    """
    def test_transduce_verbose(self):
        """  
        test the state, input, and output as specified above
        """
        # arrange
        l = sm.SumLast3()
        l.start()
        capture = io.StringIO()
        sys.stdout = capture
        goal_result = [2, 3, 6, 8, 17, 15, 13, 4, 8]
        expected_print = \
            "Start state: (0, 0)\n" + \
            "In: 2 Out: 2 Next State: (0, 2)\n"+\
            "In: 1 Out: 3 Next State: (2, 1)\n"+\
            "In: 3 Out: 6 Next State: (1, 3)\n"+\
            "In: 4 Out: 8 Next State: (3, 4)\n"+\
            "In: 10 Out: 17 Next State: (4, 10)\n"+\
            "In: 1 Out: 15 Next State: (10, 1)\n"+\
            "In: 2 Out: 13 Next State: (1, 2)\n"+\
            "In: 1 Out: 4 Next State: (2, 1)\n"+\
            "In: 5 Out: 8 Next State: (1, 5)\n"
        
        # action
        result = l.transduce([2, 1, 3, 4, 10, 1, 2, 1, 5], verbose = True)
        sys.stdout = sys.__stdout__

        # assert:
        self.assertEqual(result, goal_result, "LIST OUTPUT INCORRECT")
        self.assertEqual(capture.getvalue(), expected_print, "PRINT OUTPUT INCORRECT")
        self.assertEqual(l.getState(), (1,5), "FINAL STATE INCORRECT")

    def test_transduce_verbose_with_invalid_inputs(self):
        """  
        test how to handle invalid inputs
        """
        # arrange
        l = sm.SumLast3()
        l.start()
        capture = io.StringIO()
        sys.stdout = capture
        goal_result = [2, 3, 'invalid input', 7, 15, 15, 'invalid input', 12, 'invalid input']
        expected_print = \
            "Start state: (0, 0)\n" + \
            "In: 2 Out: 2 Next State: (0, 2)\n"+\
            "In: 1 Out: 3 Next State: (2, 1)\n"+\
            "In: a Out: invalid input Next State: (2, 1)\n"+\
            "In: 4 Out: 7 Next State: (1, 4)\n"+\
            "In: 10 Out: 15 Next State: (4, 10)\n"+\
            "In: 1 Out: 15 Next State: (10, 1)\n"+\
            "In: None Out: invalid input Next State: (10, 1)\n"+\
            "In: 1 Out: 12 Next State: (1, 1)\n"+\
            "In: True Out: invalid input Next State: (1, 1)\n"
        
        # action
        result = l.transduce([2, 1, 'a', 4, 10, 1, None, 1, True], verbose = True)
        sys.stdout = sys.__stdout__

        # assert:
        self.assertEqual(result, goal_result, "LIST OUTPUT INCORRECT")
        self.assertEqual(capture.getvalue(), expected_print, "PRINT OUTPUT INCORRECT")
        self.assertEqual(l.getState(), (1,1), "FINAL STATE INCORRECT")

class TestNegationSM(unittest.TestCase):
    """  
    Test the negation state machine
    """

    def setUp(self) -> None:
        self.neg = sm.Negation()

    def test_transduce_normal(self):
        self.assertEqual(self.neg.transduce([True, True, True, False, False, False]), [False, False, False, True, True, True])

    def test_transduce_invalid(self):
        self.assertEqual(self.neg.run(5), [None, None, None, None, None])

    def test_transduce_invalid_int(self):
        self.assertEqual(self.neg.transduce([0,1,2,3,4]), [None, None, None, None, None])

    def test_transduce_verbose_with_invalid_inputs(self):
        """  
        test how to handle invalid inputs
        """
        # arrange
        capture = io.StringIO()
        sys.stdout = capture
        
        expected_print = \
            "Start state: 0\n" + \
            "In: 2 Out: None Next State: 0\n"+\
            "In: False Out: True Next State: True\n"+\
            "In: a Out: None Next State: True\n"+\
            "In: 4 Out: None Next State: True\n"+\
            "In: 10 Out: None Next State: True\n"+\
            "In: 1 Out: None Next State: True\n"+\
            "In: None Out: None Next State: True\n"+\
            "In: False Out: True Next State: True\n"+\
            "In: True Out: False Next State: False\n"
        
        # action
        result = self.neg.transduce([2, False, 'a', 4, 10, 1, None, False, True], verbose = True)
        sys.stdout = sys.__stdout__

        # assert:
        self.assertEqual(capture.getvalue(), expected_print, "PRINT OUTPUT INCORRECT")

class TestAdderSM(unittest.TestCase):
    """  
    Testing Adder State Machine
    """

    def setUp(self) -> None:
        self.adder = sm.Adder()

    def test_passing_non_tuple_argument_to_adder(self):
        self.assertEqual(self.adder.transduce([1,2,3,4]), [None, None, None, None])

    def test_passing_undefined_return_none(self):
        self.assertEqual(self.adder.transduce(['undefined', ('undefined', 1), (2, 'undefined'), ('undefined', 'undefined')]), [None, None, None, None])

    def test_passing_valid_tuple_argument_return_safe_add(self):
        self.assertEqual(self.adder.transduce([(2,1), (45,55)]), [3, 100])

class TestWireSM(unittest.TestCase):
    """  
    testing the Wire class
    """
    def test_wire_pass_trhough_inp_and_state(self):
        # settings
        fed = [2.2, 'a', 0, True, None]
        wire = sm.Wire()
        # this is to capture printed message
        capOut = io.StringIO() 
        sys.stdout = capOut
        printed = \
                "Start state: 0\n" + \
                "In: 2.2 Out: 2.2 Next State: 0\n" + \
                "In: a Out: a Next State: 0\n" + \
                "In: 0 Out: 0 Next State: 0\n" + \
                "In: True Out: True Next State: 0\n" + \
                "In: None Out: None Next State: 0\n"
        
        # action
        out = wire.transduce(fed, verbose=True)
        sys.stdout = sys.__stdout__
        # Assert
        self.assertEqual(out, fed, "pass through FAILED")
        self.assertEqual(capOut.getvalue(), printed)

class TestFixedClass(unittest.TestCase):
    """  
    testing the fixed class
    """
    def test_all_outputs_are_fixed(self):
        f = sm.Fixed(2)
        self.assertEqual(f.run(5), [2,2,2,2,2])

class TestMultiplierClass(unittest.TestCase):
    """  
    Testing Multiplier class
    """
    def setUp(self) -> None:
        self.m = sm.Multiplier()

    def test_valid_inputs_tuple(self):
        input = [(1,1.5), (-2.3, 4), (0, 200), (-3, -3), (4, -3)]
        output = [1.5, -9.2, 0, 9, -12]
        # assert
        self.assertEqual(self.m.transduce(input), output)
    
    def test_invalid_inputs_returns_None(self):
        input = [2, (None, 'a'), (2, 'undefined'), 'undefined']
        # assert
        self.assertEqual(self.m.transduce(input), [None, None, None, None])

class TestConsumeFiveValuesClass(unittest.TestCase):
    """  
    test ConcumeFiveValues class 
    but the main focus is to test the def done function
    """
    def setUp(self) -> None:
        self.smf = sm.ConsumeFiveValues()
        self.inputs = [i for i in range(1,11)]
    
    def test_transduce_non_verbose_scenario(self):
        self.assertEqual(self.smf.transduce(self.inputs), [None]*4 + [15])

    def test_transduce_verbose_mode_scenario(self):
        capture = io.StringIO()
        sys.stdout = capture
        expected_printout = \
            "Start state: (0, 0)\n"+\
            "In: 1 Out: None Next State: (1, 1)\n"+\
            "In: 2 Out: None Next State: (2, 3)\n"+\
            "In: 3 Out: None Next State: (3, 6)\n"+\
            "In: 4 Out: None Next State: (4, 10)\n"+\
            "In: 5 Out: 15 Next State: (5, 15)\n"
        # action
        self.smf.transduce(self.inputs, verbose=True)
        sys.stdout = sys.__stdout__
        # assert
        self.assertEqual(capture.getvalue(), expected_printout)

class TestRepeatClass(unittest.TestCase):
    """  
    Test case scenarion for Repeat SM
    """
    def setUp(self) -> None:
        self.ch = sm.CharTSM('a')
    
    def test_charTSM_class_verbose(self):
        capout = io.StringIO()
        sys.stdout = capout
        expected_out = \
            "Start state: False\n"+\
            "In: None Out: a Next State: True\n"
        # action
        result = self.ch.run(verbose=True)
        # give back the stdout to the default
        sys.stdout = sys.__stdout__
        # assert
        self.assertEqual(result, ['a'], "result is WORNG")
        self.assertEqual(capout.getvalue(), expected_out, "Print out is WRONG")

    def test_repeat_class_to_charTSM_non_verbose(self):
        rep = sm.Repeat(self.ch, 4)
        self.assertEqual(rep.run(), ['a', 'a', 'a', 'a'])

    def test_repeat_class_to_charTSM_verbose_scenario(self):
        scanout = io.StringIO()
        sys.stdout = scanout
        expected_out = \
            "Start state: (0, False)\n"+\
            "In: None Out: a Next State: (1, False)\n"+\
            "In: None Out: a Next State: (2, False)\n"+\
            "In: None Out: a Next State: (3, False)\n"+\
            "In: None Out: a Next State: (4, False)\n"
        
        # action
        sm.Repeat(sm.CharTSM('a'), 4).run(verbose=True)
        sys.stdout = sys.__stdout__
        self.assertEqual(scanout.getvalue(), expected_out)

    def test_counter_only_incremented_when_constituent_is_done(self):
        cap = io.StringIO()
        # handouver stdout to cap
        sys.stdout = cap
        expected_out = \
            "Start state: (0, (0, 0))\n"+\
            "In: 0 Out: None Next State: (0, (1, 0))\n"+\
            "In: 1 Out: None Next State: (0, (2, 1))\n"+\
            "In: 2 Out: None Next State: (0, (3, 3))\n"+\
            "In: 3 Out: None Next State: (0, (4, 6))\n"+\
            "In: 4 Out: 10 Next State: (1, (0, 0))\n"+\
            "In: 5 Out: None Next State: (1, (1, 5))\n"+\
            "In: 6 Out: None Next State: (1, (2, 11))\n"+\
            "In: 7 Out: None Next State: (1, (3, 18))\n"+\
            "In: 8 Out: None Next State: (1, (4, 26))\n"+\
            "In: 9 Out: 35 Next State: (2, (0, 0))\n"+\
            "In: 10 Out: None Next State: (2, (1, 10))\n"+\
            "In: 11 Out: None Next State: (2, (2, 21))\n"+\
            "In: 12 Out: None Next State: (2, (3, 33))\n"+\
            "In: 13 Out: None Next State: (2, (4, 46))\n"+\
            "In: 14 Out: 60 Next State: (3, (0, 0))\n"
        # action
        result = sm.Repeat(sm.ConsumeFiveValues(), 3).transduce(range(100), verbose=True)
        # handover back the sys stdout to default __stdout__
        sys.stdout = sys.__stdout__
        # assert
        self.assertEqual(result,\
             [None, None, None, None, 10, None, None, None, None, 35, None, None, None, None, 60],\
                "Result is wrong")
        self.assertEqual(cap.getvalue(), expected_out, "PRINT OUT is wrong")

class TestSequenceClass(unittest.TestCase):
    """  
    test for the sequence class
    """
    def test_basic_sequence_3_charTSM_verbose(self):
        # preps
        m = sm.Sequence([sm.CharTSM('a'), sm.CharTSM('b'), sm.CharTSM('c')])
        scanner = io.StringIO()
        sys.stdout = scanner
        expected_output = \
            "Start state: (0, False)\n"+\
            "In: None Out: a Next State: (1, False)\n"+\
            "In: None Out: b Next State: (2, False)\n"+\
            "In: None Out: c Next State: (2, True)\n"
        action = m.run(verbose=True)
        # return the stdout to its default methods
        sys.stdout = sys.__stdout__
        self.assertEqual(action, ['a', 'b', 'c'], 'ACTION result is wrong')
        self.assertEqual(scanner.getvalue(), expected_output, "verbose scanner is wrong")

    def test_hello_word_string_to_list_of_chars(self):
        hello = 'Hello World'
        m = sm.Sequence([sm.CharTSM(c) for c in hello])
        action = m.run(11) #run(11) because Hello World consist of 11 chars including the white space!
        self.assertEqual(action, ['H','e','l','l','o',' ','W','o','r','l','d'])

    def test_sequence_transduce_of_char_and_consume_five_values_classes(self):
        m = sm.Sequence([sm.CharTSM('a'), sm.ConsumeFiveValues(), sm.CharTSM('b')])
        action = m.transduce(range(100))
        self.assertEqual(action, ['a', None, None, None, None, 15, 'b'])

    def test_repeat_sequence_run_verbose(self):
        m = sm.Repeat(sm.Sequence([sm.CharTSM(c) for c in 'abc']), 3)
        clipper = io.StringIO()
        sys.stdout = clipper
        expected_printed = \
            "Start state: (0, (0, False))\n"+\
            "In: None Out: a Next State: (0, (1, False))\n"+\
            "In: None Out: b Next State: (0, (2, False))\n"+\
            "In: None Out: c Next State: (1, (0, False))\n"+\
            "In: None Out: a Next State: (1, (1, False))\n"+\
            "In: None Out: b Next State: (1, (2, False))\n"+\
            "In: None Out: c Next State: (2, (0, False))\n"+\
            "In: None Out: a Next State: (2, (1, False))\n"+\
            "In: None Out: b Next State: (2, (2, False))\n"+\
            "In: None Out: c Next State: (3, (0, False))\n"
        action = m.run(verbose = True)
        sys.stdout = sys.__stdout__
        self.assertEqual(action, ['a','b','c','a','b','c','a','b','c'], "the ACTION is wrong")
        self.assertEqual(clipper.getvalue(), expected_printed, "PRINT OUT is wrong")

class TestUntilAndRepeatUntilClasses(unittest.TestCase):
    """  
    This test two class types : Until and RepeatUntil
    NOTE: for practicality the condition functions for all these cases will be in lambda function
    """
    
    def test_repeat_until_verbose_with_lambda_larger_than_10(self):
        m = sm.RepeatUntil(lambda x : x > 10, sm.ConsumeFiveValues())
        clipout = io.StringIO()
        sys.stdout = clipout
        expected_printout = \
            "Start state: (False, (0, 0))\n"+\
            "In: 0 Out: None Next State: (False, (1, 0))\n"+\
            "In: 1 Out: None Next State: (False, (2, 1))\n"+\
            "In: 2 Out: None Next State: (False, (3, 3))\n"+\
            "In: 3 Out: None Next State: (False, (4, 6))\n"+\
            "In: 4 Out: 10 Next State: (False, (0, 0))\n"+\
            "In: 5 Out: None Next State: (False, (1, 5))\n"+\
            "In: 6 Out: None Next State: (False, (2, 11))\n"+\
            "In: 7 Out: None Next State: (False, (3, 18))\n"+\
            "In: 8 Out: None Next State: (False, (4, 26))\n"+\
            "In: 9 Out: 35 Next State: (False, (0, 0))\n"+\
            "In: 10 Out: None Next State: (False, (1, 10))\n"+\
            "In: 11 Out: None Next State: (True, (2, 21))\n"+\
            "In: 12 Out: None Next State: (True, (3, 33))\n"+\
            "In: 13 Out: None Next State: (True, (4, 46))\n"+\
            "In: 14 Out: 60 Next State: (True, (5, 60))\n"
        action = m.transduce(range(20), verbose=True)
        # action pass 0 to 20 as inputs to transduce of consumeFiveVaues class
        sys.stdout = sys.__stdout__ # return the control of standard output to default
        self.assertEqual(action, [None, None, None, None, 10, None, None, None, None, 35, None, None, None, None, 60], "RESULT is WRONG")
        self.assertEqual(clipout.getvalue(), expected_printout, "PRINT OUT is wrong")

    def test_until_verbose_with_lambda_done_because_constituent_sm_not_condition(self):
        m = sm.Until(lambda x : x > 10, sm.ConsumeFiveValues())
        clipout = io.StringIO()
        sys.stdout = clipout
        expected_printout = \
            "Start state: (False, (0, 0))\n"+\
            "In: 0 Out: None Next State: (False, (1, 0))\n"+\
            "In: 1 Out: None Next State: (False, (2, 1))\n"+\
            "In: 2 Out: None Next State: (False, (3, 3))\n"+\
            "In: 3 Out: None Next State: (False, (4, 6))\n"+\
            "In: 4 Out: 10 Next State: (False, (5, 10))\n"
        action = m.transduce(range(20), verbose=True)
        sys.stdout = sys.__stdout__
        self.assertEqual(action, [None, None, None, None, 10], "RESULT is WRONG")
        self.assertEqual(clipout.getvalue(), expected_printout, "PRINT OUT is wrong")

    def test_until_verbose_with_lambda_done_because_condition_not_constituent_sm(self):
        m = sm.Until(lambda x : x >= 2, sm.ConsumeFiveValues())
        clipout = io.StringIO()
        sys.stdout = clipout
        expected_printout = \
            "Start state: (False, (0, 0))\n"+\
            "In: 0 Out: None Next State: (False, (1, 0))\n"+\
            "In: 1 Out: None Next State: (False, (2, 1))\n"+\
            "In: 2 Out: None Next State: (True, (3, 3))\n"
        action = m.transduce(range(20), verbose=True)
        sys.stdout = sys.__stdout__
        self.assertEqual(action, [None]*3, "RESULT is WRONG")
        self.assertEqual(clipout.getvalue(), expected_printout, "PRINT OUT is wrong")

    def test_until_using_repeat_constituent_sm_verbose(self):
        m = sm.Until(lambda x : x > 10, sm.Repeat(sm.ConsumeFiveValues()))
        # NOTE: sm.Repeat without n (n= None) will repeat forever! Make sure lambda from sm.Until is VALID
        #       TO PREVENT INFINITE LOOP
        expected_printout = \
            "Start state: (False, (0, (0, 0)))\n"+\
            "In: 0 Out: None Next State: (False, (0, (1, 0)))\n"+\
            "In: 1 Out: None Next State: (False, (0, (2, 1)))\n"+\
            "In: 2 Out: None Next State: (False, (0, (3, 3)))\n"+\
            "In: 3 Out: None Next State: (False, (0, (4, 6)))\n"+\
            "In: 4 Out: 10 Next State: (False, (1, (0, 0)))\n"+\
            "In: 5 Out: None Next State: (False, (1, (1, 5)))\n"+\
            "In: 6 Out: None Next State: (False, (1, (2, 11)))\n"+\
            "In: 7 Out: None Next State: (False, (1, (3, 18)))\n"+\
            "In: 8 Out: None Next State: (False, (1, (4, 26)))\n"+\
            "In: 9 Out: 35 Next State: (False, (2, (0, 0)))\n"+\
            "In: 10 Out: None Next State: (False, (2, (1, 10)))\n"+\
            "In: 11 Out: None Next State: (True, (2, (2, 21)))\n"
        clipout = io.StringIO()
        sys.stdout = clipout
        action = m.transduce(range(20), verbose=True)
        sys.stdout = sys.__stdout__
        self.assertEqual(action, [None]*4 + [10] + [None]*4 +[35] + [None]*2, "RESULT is wrong")
        self.assertEqual(clipout.getvalue(), expected_printout, "PRINT OUT is wrong")

if __name__ == '__main__':
    unittest.main()