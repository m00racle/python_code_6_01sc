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

    def start(self):
        self.m1.start()
        self.m2.start()
    
    def step(self, inp):
        (s1, o1) = self.m1.getNextValues(self.m1.getState(), inp)
        self.m1.state = s1
        (s2, o2) = self.m2.getNextValues(self.m2.getState(), o1)
        self.m2.state = s2
        return o2