from state_machine import SM

class FreeGate(SM):
    """  
    Parking Gate State Machine

    """
    def __init__(self) -> None:
        """  
        free gate initial state always 'waiting'
        """
        super().__init__('waiting')

    def generateOuput(self, nextState, inp):
        # nextState = self.generateState(state, inp)
        if nextState == 'raising' :
            return 'lift'
        elif nextState == 'lowering' :
            return 'drop'
        else :
            return 'nop'
    
    def generateState(self, state, inp):
        gatePos, carIn, carOut = inp
        if state == 'waiting' and carIn:
            return 'raising'
        elif state == 'raising' and gatePos == 'top':
            return 'raised'
        elif state == 'raised' and carOut:
            return 'lowering'
        elif state == 'lowering' and gatePos == 'bottom' :
            return 'waiting'
        else:
            return state
    
    def getNextValues(self, state, inp, fn=..., fo=..., efn=None, efo=None) -> tuple:
        nextState = self.generateState(state, inp)
        fn = lambda s,i : nextState
        fo = lambda s,i : self.generateOuput(nextState, inp)
        return super().getNextValues(state, inp, fn, fo, efn, efo)