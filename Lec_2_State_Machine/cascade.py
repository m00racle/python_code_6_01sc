"""  
Python 6-01sc Project
Cascade State Machine
"""
from state_machine import SM

class Cascade(SM):
    """  
    Class Cascade to cascading two state machines
    """
    def __init__(self, m1 : SM, m2: SM) -> None:
        self.m1 = m1
        self.m2 = m2
        self.log = {}
        self.startState = (m1.startState, m2.startState)

    def getNextValues(self, state, inp, **kwargs) -> tuple:
        (s1, s2) = state
        (next_s1, o1) = self.m1.getNextValues(s1, inp)
        (next_s2, o2) = self.m2.getNextValues(s2, o1)
        return ((next_s1, next_s2), o2)