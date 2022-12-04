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
         # detect run over (the most bold one:  just straight runover gate)
        if state == 'waiting' and carOut:
            raise RunOverViolation('Run Over')
        if state == 'waiting' and carIn:
            return 'raising'
        elif state == 'raising' and gatePos == 'top':
            return 'raised'
        # detect run over:
        elif state == 'raising' and gatePos == 'bottom' and carOut: 
            raise RunOverViolation("Run Over")
        # detect too soon violation:
        elif state == 'raising' and gatePos == 'middle' and carOut:
            raise TooSoonViolation('Too Soon')
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

class RunOverViolation(Exception):
    """  
    Custom Exception for Car that RunOver the gate
    """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class TooSoonViolation(Exception):
    """  
    Custom Exception for Car that exit too soon that hit the gate
    """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
