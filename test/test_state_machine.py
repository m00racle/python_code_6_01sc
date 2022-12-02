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
        inps = [100, -3, 4, -123, 10]
        comp = [100, 97, 101, -22, -12]
        self.assertEqual(self.a.transduce(inps), comp)
    
    def test_transduce_verbose_print_steps_and_return_list(self):
        # setup
        inps = [100, -3, 4, -123, 10]
        comp = [100, 97, 101, -22, -12]
        # this is to capture printed message
        capOut = io.StringIO() 
        sys.stdout = capOut
        printed = \
                "Start state: 0\n" + \
                "In: 100 Out: 100 Next State: 100\n" + \
                "In: -3 Out: 97 Next State: 97\n" + \
                "In: 4 Out: 101 Next State: 101\n" + \
                "In: -123 Out: -22 Next State: -22\n" + \
                "In: 10 Out: -12 Next State: -12\n"
        
        # action
        out = self.a.transduce(inps, verbose=True)
        sys.stdout = sys.__stdout__
        self.assertEqual(out, comp, "the output list is WRONG")
        self.assertEqual(capOut.getvalue(), printed)

    def test_run_5_returns_5_None_list(self):
        self.assertEqual(self.b.run(5), [100, 100, 100, 100, 100])
    
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
                "Start state: 3\n" + \
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
        self.assertEqual(self.a.transduce([100, -3, 4, -123, 10]), [50, 48.5, 0.5, -59.5, -56.5], "output list wrong")
        self.assertEqual(self.a.getState(), 10, "final state is wrong")
    
    def test_empty_input_run_returns_all_zero_and_final_state_zero(self):
        self.assertEqual(self.a.run(3), [0,0,0], "the empty run returns wrong")
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
        