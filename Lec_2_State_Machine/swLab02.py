"""  
this is file for the 
Software Lab 02
"""
from state_machine import SM

class Delay2Machine(SM):
    """  
    class 2 times delay
    """
    def __init__(self, val0: int, val1: int) -> None:
        self.startState = (val0, val1)
    
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        (s0, s1) = state
        return ((s1, inp), s0)

class CommentsSM(SM):
    """  
    Class CommentsSM
    """
    def __init__(self) -> None:
        self.startState = False

    def getNextValues(self, state, inp, **kwargs) -> tuple:
        cond = state
        if inp == '#': cond = True
        if inp == '\n': cond = False
        o = inp if cond else None
        return (cond, o)

class FirstWord(SM):
    """  
    class FirstWord
    """
    def __init__(self) -> None:
        self.startState = 'start'
    
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        cond = state
        if inp == '\n':
            cond = 'start'
        if cond == 'start' and inp.isalpha() :
            cond = 'pick'
        if cond == 'pick' and not inp.isalpha():
            cond = 'end'
        o = inp if cond == 'pick' else None
        return (cond, o)