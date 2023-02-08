"""  
the plant and controller
used to model a robot controller and simulate the world 
"""

from state_machine import SM

class WallController(SM):
    """  
    State Machine: Wall Controller
    subclass of State Machine SM
    """
    def __init__(self, k: float, dDesired: float, initVal=0) -> None:
        self.k = k
        self.dDesired = dDesired
        super().__init__(initVal)
    
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        # use try - except since safe mul and safe add uses raise Type error to handle invalid inputs
        try:
            result = self.safeMul(self.k, self.safeAdd(self.dDesired, self.safeMul(-1, inp)))
        except TypeError as te:
            result = te.args[0]
            return (result, result)
        return (result, result)

class WallWorld(SM):
    """  
    State Machine : Wall World simulate the external world interact with the robot
    subclass of State Machine SM
    """
    # let's start with easy step
    def __init__(self, deltaT: float, initVal=0) -> None:
        self.deltaT = deltaT
        super().__init__(initVal)

    def getNextValues(self, state, inp, **kwargs) -> tuple:
        try:
            nextState = state - self.deltaT * inp
        except TypeError as te:
            # when having inp as None or undefined it will result None
            # this need still shift the state to none
            # and current state still need to go as output.
            return (te.args[0], state)
        
        return (nextState, state)