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
        self.startState = self.m1.startState
        self.m1.start()
        self.m2.start()

    def getNextValues(self, state, inp, **kwargs) -> tuple:
        currentState = state
        o = self.m2.step(self.m1.step(inp))
        return (o, o)