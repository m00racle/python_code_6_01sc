from state_machine import SM

"""  
Conditional consist of State Machine Sub-classes:
1. Switch
2. Multiplex (Mux)
"""

class Switch(SM):
    """  
    Switch
    startState = (s1, s2)
    """
    def __init__(self, condition, sm1: SM, sm2: SM) -> None:
        """  
        GIVEN:
        condition: function = lambda function returns bool
        sm1 : SM = constituent SM
        sm2 : SM = constituent SM
        """
        self.sm1 = sm1
        self.sm2 = sm2
        self.condition = condition
        self.startState = (self.sm1.startState, self.sm2.startState)

    def getNextValues(self, state, inp, **kwargs) -> tuple:
        (s1, s2) = state
        try:
            if self.condition(inp):
                (ns1, o) = self.sm1.getNextValues(s1, inp)
                return ((ns1, s2), o)
            else:
                (ns2, o) = self.sm2.getNextValues(s2, inp)
                return ((s1, ns2), o)
        except Exception as e:
            return ((s1, s2), None)

class Multiplex(Switch):
    """  
    Multiplex (Mux)
    StartState = (s1, s2)
    """
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        (s1, s2) = state
        try:
            (ns1, o1) = self.sm1.getNextValues(s1, inp)
            (ns2, o2) = self.sm2.getNextValues(s2, inp)

            # decide which output:
            output = o1 if self.condition(inp) else o2
            return ((ns1, ns2), output)
        except Exception as e:
            return ((s1, s2), None)

class If(SM):
    """  
    Given:
    condition : function = lambda function returns bool
    sm1 : SM
    sm2 : SM
    """
    def __init__(self, condition, sm1: SM, sm2: SM, initVal=0) -> None:
        self.startState = ('start', None)
        self.condition = condition
        self.sm1 = sm1
        self.sm2 = sm2

    def getFirstRealState(self, inp):
        if self.condition(inp):
            return ('runningSM1', self.sm1.startState)
        else:
            return ('runningSM2', self.sm2.startState)

    def getNextValues(self, state, inp, **kwargs) -> tuple:
        # dissect the state
        (ifState, smState) = state
        # check what mode if state is 
        if ifState == 'start':
            (ifState, smState) = self.getFirstRealState(inp)
        # Then continue using the real smState but only their owns state machine
        if ifState == 'runningSM1':
            (newS, o) = self.sm1.getNextValues(smState, inp)
            return (('runningSM1',newS), o)
        else:
            (newS, o) = self.sm2.getNextValues(smState, inp)
            return (('runningSM2',newS), o)