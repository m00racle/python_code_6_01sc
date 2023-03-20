
import os, sys, unittest

# set test directory
test_dir = os.path.dirname(__file__)
code_dir = os.path.normpath(test_dir + "/../Lec_2_State_Machine")

sys.path.append(code_dir)

from swLab02 import Delay2Machine, CommentsSM, FirstWord

class TestDelay2Machine(unittest.TestCase):
    """  
    test class Delay2Machine(SM) on Lec_2_State_Machine
    """
    def test_1_runTestDelay(self):
        outs = Delay2Machine(100, 10).transduce([1,0,2,0,0,3,0,0,0,4])
        self.assertEqual(outs, [100, 10, 1, 0, 2, 0, 0, 3, 0, 0])
    
    def test_2_runTestDelay(self):
        self.assertEqual(Delay2Machine(10, 100).transduce([0,0,0,0,0,0,1]), [10, 100, 0, 0, 0, 0, 0])

    def test_3_runTestDelay(self):
        self.assertEqual(Delay2Machine(-1, 0).transduce([1,2,-3,1,2,-3]), [-1, 0, 1, 2, -3, 1])

    def test_4_runTestDelay(self):
        # Test that self.state is not changed
        m = Delay2Machine(100,10)
        m.start()
        next_res = [m.getNextValues(m.state, i) for i in [-1,-2,-3,-4,-5,-6]]
        step_res = [m.step(i) for i in [1,0,2,0,0,3,0,0,0,4]]
        self.assertEqual(step_res, [100, 10, 1, 0, 2, 0, 0, 3, 0, 0])
        self.assertNotEqual(next_res, [100, 10, 1, 0, 2, 0, 0, 3, 0, 0])

class TestCommentsSM(unittest.TestCase):
    """  
    test class CommentsSM
    """
    def test_1_runTestComm(self):
        x1 = '''def f(x):  # func
           if x:   # test
            # comment
            return 'foo' '''

        test1 = [c for c in CommentsSM().transduce(x1) if not c==None]
        self.assertEqual(test1, ['#', ' ', 'f', 'u', 'n', 'c', '#', ' ', 't', 'e', 's', 't', '#', ' ', 'c', 'o', 'm', 'm', 'e', 'n', 't'])

    def test_2_runTestComm(self):
        x2 = '''#initial comment
        def f(x):  # func
            if x:   # test
                # comment
                return 'foo' '''
        
        test2 = [c for c in CommentsSM().transduce(x2) if not c==None]
        self.assertEqual(test2, ['#', 'i', 'n', 'i', 't', 'i', 'a', 'l', ' ', 'c', 'o', 'm', 'm', 'e', 'n', 't', '#', ' ', 'f', 'u', 'n', 'c', '#', ' ', 't', 'e', 's', 't', '#', ' ', 'c', 'o', 'm', 'm', 'e', 'n', 't'])

    def test_3_runTestComm(self):
        x2 = '''#initial comment
        def f(x):  # func
            if x:   # test
                # comment
                return 'foo' '''
        m = CommentsSM()
        m.start()
        dumm = [m.getNextValues(m.state, i) for i in ' #foo #bar']
        test3 = [c for c in [m.step(i) for i in x2] if not c==None]
        self.assertEqual(test3, ['#', 'i', 'n', 'i', 't', 'i', 'a', 'l', ' ', 'c', 'o', 'm', 'm', 'e', 'n', 't', '#', ' ', 'f', 'u', 'n', 'c', '#', ' ', 't', 'e', 's', 't', '#', ' ', 'c', 'o', 'm', 'm', 'e', 'n', 't'])

class TestFirstWord(unittest.TestCase):
    """  
    test class FirstWord
    """
    def test_1_runTestFW(self):
        test1 = 'hi\nho'
        res1 = FirstWord().transduce(test1)
        self.assertEqual(res1, ['h', 'i', None, 'h', 'o'])
    
    def test_2_runTestFW(self):
        test2 = '  hi\nho'

        res2 = FirstWord().transduce(test2)
        self.assertEqual(res2, [None, None, 'h', 'i', None, 'h', 'o'])
    
    def test_3_runTestFW(self):
        test3  = '\n\n hi \nho ho ho\n\n ha ha ha'

        res3 = FirstWord().transduce(test3)
        self.assertEqual(res3, [None, None, None, 'h', 'i', None, None, 'h', 'o', None, None, None, None, None, None, None, None, None, 'h', 'a', None, None, None, None, None, None])

    def test_4_runTestFW(self):
        test1 = test1 = 'hi\nho'

        m = FirstWord()
        m.start()
        dumm = [m.getNextValues(m.state, i) for i in '\nFoo ']
        res4 = [m.step(i) for i in test1]
        self.assertEqual(res4, ['h', 'i', None, 'h', 'o'])
