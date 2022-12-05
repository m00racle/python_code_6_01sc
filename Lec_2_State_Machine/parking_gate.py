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
    
    
    def getNextValues(self, state, inp, fn=..., fo=..., efn=None, efo=None) -> tuple:
        try :
            gatePos, carIn, carOut = inp
            # detect violations
            if state == 'waiting' and carOut : raise RunOverViolation('ALERT! run off')
            if state == 'raising' and gatePos == 'bottom' and carOut : raise RunOverViolation('ALERT! run off')
            if state == 'raising' and gatePos == 'middle' and carOut : raise TooSoonViolation('ALERT! too soon')
            if state == 'lowering' and gatePos == 'middle' and carOut : raise TooSoonViolation('ALERT! too soon')

            # determine next state:
            if state == 'waiting' and carIn:
                nextState = 'raising'
            elif state == 'raising' and gatePos == 'top':
                nextState = 'raised'
            elif state == 'raised' and carOut:
                nextState = 'lowering'
            elif state == 'lowering' and gatePos == 'bottom' :
                nextState = 'waiting'
            else:
                nextState = state
            
            # determine the ouput:
            if nextState == 'raising' :
                output = 'lift'
            elif nextState == 'lowering' :
                output = 'drop'
            else :
                output = 'nop'
            
            return (nextState, output)
        except Exception as e:
            return(self.fnErr(state, inp, e), self.foErr(state, inp, e))

    def fnErr(self, state, inp, err):
        state = 'halt'
        return super().fnErr(state, inp, err)
        

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
