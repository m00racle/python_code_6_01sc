"""  
Python 6-01sc Project
Cascade State Machine
"""
from state_machine import SM

class Cascade(SM):
    """  
    Class Cascade to cascading two state machines
    """
    def __init__(self, m1 : SM, m2: SM, smVerbose = False, cascadeName = None) -> None:
        self.m1 = m1
        self.m2 = m2
        self.log = {}
        self.startState = (m1.startState, m2.startState)
        self.smVerbose = smVerbose
        self.cascadeName = cascadeName

    def getNextValues(self, state, inp, **kwargs) -> tuple:
        (s1, s2) = state
        (next_s1, o1) = self.m1.getNextValues(s1, inp)
        (next_s2, o2) = self.m2.getNextValues(s2, o1)
        if self.smVerbose:
            name = "Cascade" if not self.cascadeName else self.cascadeName
            print(f"\n{name} sm1 input: {inp}")
            print(f"{name} sm1 state: {s1}")
            print(f"{name} sm1 output: {o1}")
            print(f"{name} sm2 input: {o1}")
            print(f"{name} sm2 state: {s2}")
            print(f"{name} sm2 output: {o2}")

        return ((next_s1, next_s2), o2)