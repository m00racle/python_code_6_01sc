"""  
ROBOT SM 
all state machine represent the robot controls
"""

from soar.robot.base import BaseRobot
from robot_PioneerMod import PioneerMod
import robot_io as io


class RobotSM:
    """  
    This SM class is intended as Abstract class
    Thus it is not meant to be instantiated to create and object
    Hence this will be used as blueprint to create another sub - class
    """
    def __init__(self, robot: PioneerMod, initVal = 'start') -> None:
        """  
        initialize object type SM 
        must provides start state
        also provide dictionary type object called self.log
        """
        self.startState = initVal
        self.robot = robot
        self.log = {}

    def start(self):
        """  
        REQUIRED when the State Machine want to be operational
        This function must be called each time State Machine is want to be started after instantiated
        as subclass object.
        Basically just put the startState at the current state.

        Can be handy if later on in the sub class they need a function to reset the State Machine.

        parameters: self

        returns : None
        """
        self.state = self.startState

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state
    
    def step(self, inp, verbose = False):
        """  
        Change the instance state
        Returns the output 
        """
        (s, o) = self.getNextValues(self.state, inp)
        if verbose : print(f"In: {inp} Out: {o} Next State: {s}")
        self.state = s
        return o

    def transduce(self, inps, verbose = False):
        """  
        given inps : list sequence of input
        returns list : of outputs for each time
        """
        # prepare the state to be startState:
        result = []
        self.start()
        
        if verbose : print(f"Start state: {self.state}")

        for inp in inps:
            if self.done(self.state) : break
            # if not done keep the step:
            result.append(self.step(inp, verbose))
        
        return result

    def run(self, n = 10, verbose = False):
        """  
        step but no input is given
        """
        return self.transduce([None] * n, verbose)

    def getNextValues(self, state, inp:io.SensorInput, **kwargs)->tuple:
        """  
        returns : tuple -> (next state, output)
        this is supposed to be abstract function which must be defined in sub class
        
        fn = n(s,i) -> programmer must provide function definition 
        fo = o(s,i) -> programmer must provide function definition
        NOTE: this is PURE FUNCTION don't change self.state from this function

        efn = n(s,i) custom function invoked when exception raised passing last valid state and input to return next state
        NOTE: retaining previous valid state will prepare the SM to handle the next valid input
        efo = o(s,i) custom function invoked when exception raised passing last valid state and input to return output
        """
        defs = {
            'fn' : lambda s,i : None,
            'fo' : lambda s,i : None,
            'efo' : None,
            'efn' : None,
        }

        for k in kwargs:
            if k in defs: defs[k] = kwargs[k]
        
        efn = defs['efn']
        efo = defs['efo']
        fn = defs['fn']
        fo = defs['fo']
        try:
            return(fn(state, inp), fo(state, inp))
        except Exception as e:
            # provide state and output when the input raise any exception (including TypeError)
            if efn is None and efo is None : return(self.fnErr(state, inp, e), self.foErr(state, inp, e))
            if efn is None : return (self.fnErr(state, inp, e), efo(state, inp, e))
            if efo is None : return (efn(state, inp, e), self.foErr(state, inp, e))
            
            return(efn(state, inp), efo(state, inp))
        
    def fnErr(self, state, inp, err):
        """  
        function next state error handler made if the sub class want more complicated error handling
        state : state (the previous valid state) retained
        inp : current input that raised exception
        err : thrown exception
        DEFAULT: return last valid state
        OVERRIDE this function if you want custom error handling
        NOTE: overrride the state with the state you desired if there is an error raised:
        """
        return state
    
    def foErr(self, state, inp, err, msg = None):
        """  
        function current output error handler made if sub class wnat more sophisticated error handling
        function output error handler
        state : state (the previous valid state) retained
        inp : current input which raised exception
        err : thrown exception
        OVERRIDE function for custom output error handling
        NOTE: for user defined exception will be caught with default except thus it return args[0]
        """
        self.log['ex_msg'] = err.args[0]
        try:
            raise err
        except TypeError:
            # change the msg value in override to pass custom returns for Type Error
            return msg
        except ValueError:
            # change the msg value in override to pass custom returns for Type Error
            return msg
        except:
            return err.args[0]
    
    def throw(self, excep):
        """  
        helper function to throw or raise exception from lambda function
        This is because lambda function in Python can't directly raise any exception.
        """
        raise excep

    def splitValue(self, v: any)-> tuple:
        """  
        helper function:
        basically verify that the inputs are in pair and defined
        """
        if v == 'undefined' or type(v) != tuple:
            return ('undefined', 'undefined')
        elif len(v) != 2:
            return ('undefined', 'undefined')
        else:
            return v

    def safeAdd(self, a, b):
        """  
        helper function to safely add inputs
        a : number (int or float)
        b : nubmer (int or float)
        return a + b if a and b are int or float
        """
        
        if isinstance(a,(int, float)) and isinstance(b, (int, float)) and not isinstance(a,bool) and not isinstance(b,bool):
            return a + b
        else:
            raise TypeError(None)

    def safeMul(self, a, b):
        """  
        Helper function to safely multiply inputs
        """

        if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) and not isinstance(b,bool):
            return a * b
        else:
            raise TypeError(None)
    
    def done(self, state) -> bool:
        """  
        Default function to terminante the sequence of SM process
        """
        return False