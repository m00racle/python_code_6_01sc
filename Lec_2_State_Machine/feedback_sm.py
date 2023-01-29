from state_machine import SM

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
        self.startState = sm.startState

    def getNextValues(self, state, inp, **kwargs) -> tuple:
        (ignore, o) = self.sm.getNextValues(state, 'undefined')
        (newS, ignore) = self.sm.getNextValues(state, o)
        return (newS, o)