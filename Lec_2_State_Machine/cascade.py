"""  
Python 6-01sc Project
Cascade State Machine
"""
from state_machine import SM, Delay

class Cascade(SM):
    """  
    Class Cascade to cascading two state machines
    """
    def __init__(self, m1, m2) -> None:
        self.m1 = m1
        self.m2 = m2
        self.log = {}

    def transduce(self, inps, verbose=False):
        return self.m2.transduce(self.m1.transduce(inps))

class Increment(SM):
    """  
    Increment state machine:
    fn (s, i) = ?
    fo (s, i) = i + k (k is a constant)
    """