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
    
class Feedback2(Feedback):
    """  
    sub class Feedback which include inp and feedback as input to the constituent sm
    """
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        (ignore, o) = self.sm.getNextValues(state, (inp, 'undefined'))
        (newS, ignore) = self.sm.getNextValues(state, (inp, o))
        return (newS, o)

class FeedbackAdd(Feedback):
    """  
    class Feedback which the feedback is added to the inp
    """
    def __init__(self, sm1: SM, sm2: SM) -> None:
        self.sm1 = sm1
        self.sm2 = sm2
        self.startState = sm1.startState

    def getNextValues(self, state, inp, **kwargs) -> tuple:
        try:
            (s1, o) = self.sm1.getNextValues(state, 'undefined')
            (s2, o2) = self.sm2.getNextValues(s1, o)
            (newS, ignore) = self.sm1.getNextValues(s2, self.safeAdd(inp, o2))
        except TypeError as e:
            return (state, e.args[0])
        return (newS, o)

class FeedbackSub(FeedbackAdd):
    """  
    class Feedback which the feedback subtract the new input
    """
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        try:
            (s1, o) = self.sm1.getNextValues(state, 'undefined')
            (s2, o2) = self.sm2.getNextValues(s1, o)
            (newS, ignore) = self.sm1.getNextValues(s2, self.safeAdd(inp, self.safeMul(-1, o2)))
        except TypeError as e:
            return (state, e.args[0])
        return (newS, o)