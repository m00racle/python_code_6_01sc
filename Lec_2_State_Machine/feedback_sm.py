from state_machine import SM, Increment, Delay
from cascade import Cascade

"""  
Feedback Combinator
"""

class Feedback(SM):
    """  
    class Feedback inherit SM class
    This is the model for feedback state machine
    """
    def __init__(self, sm : SM) -> None:
        self.sm = sm
        # self.startState = 0

    def getNextValues(self, state, inp, **kwargs) -> tuple:
        (ignore, o) = self.sm.getNextValues(state, 'undefined')
        (newS, ignore) = self.sm.getNextValues(state, o)
        return (newS, o)

    def transduce(self, inps, verbose=False):
        return self.sm.transduce(inps, verbose)
    