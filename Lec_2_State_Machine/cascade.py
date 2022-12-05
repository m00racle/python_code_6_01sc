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
    def __init__(self, incr, initVal=0) -> None:
        self.incr = incr
        super().__init__(initVal)
    
    def safeAdd(self, a, b):
        """  
        a : number (int or float)
        b : nubmer (int or float)
        return a + b if a and b are int or float
        """
        
        if isinstance(a,(int, float)) and isinstance(b, (int, float)) and not isinstance(a,bool) and not isinstance(b,bool):
            return a + b
        else:
            raise TypeError(None)
    
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        kwargs = {
            'fn' : lambda s, i : i + self.incr,
            'fo' : lambda s, i : self.safeAdd(inp, self.incr)
        }
        return super().getNextValues(state, inp, **kwargs)