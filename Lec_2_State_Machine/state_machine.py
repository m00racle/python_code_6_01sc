"""  
Super Class SM:
"""

# create super class (meant to be abstract) 
class SM:
    """  
    This SM class is intended as Abstract class
    Thus it is not meant to be instantiated to create and object
    Hence this will be used as blueprint to create another sub - class
    """
    def __init__(self, initVal = 0) -> None:
        """  
        initialize object type SM 
        must provides start state
        also provide dictionary type object called self.log
        """
        self.startState = initVal
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
    
    def step(self, inp):
        """  
        Change the instance state
        Returns the output 
        """
        (s, o) = self.getNextValues(self.state, inp)
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

            (s, o) = self.getNextValues(self.state, inp)
            
            if verbose : print(f"In: {inp} Out: {o} Next State: {s}")
            
            result.append(o)
            self.state = s
        
        return result

    def run(self, n = 10, verbose = False):
        """  
        step but no input is given
        """
        return self.transduce([None] * n, verbose)

    def getNextValues(self, state, inp, **kwargs)->tuple:
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
    

"""  *************************
Sub classes implementing SM: *
******************************
"""
class Accumulator(SM):
    """  
    sub class of SM which implementation is Accumulator State Machine
    fn(s,i) = s + i
    fo(s,i) = s + i
    startState : user defined

    error handling function:
    efn(s,i) = s
    efo(s,i) = None
    """
    
    def getNextValues(self, state, inp)->tuple:
        
        # get the kwargs directly
        return super().getNextValues(state, inp, fn = lambda s,i : s + i, fo = lambda s,i : s + i)
    
        
    
class Gain(SM):
    """  
    Gain State machine:
    fn(s,i) = k * i 
    fo(s,i) = k * i
    startState : 0

    errror handling function:
    efo(s,i) = efn(s,i) = 0
    """
   
    def __init__(self, k) -> None:
        super().__init__(0)
        self.k = k
    
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        kwargs = {
            'fn' : lambda s,i : self.k * i,
            'fo' : lambda s,i : self.k * i
        }
        return super().getNextValues(state, inp, **kwargs)

    def fnErr(self, state, inp, err):
        state = 0
        return super().fnErr(state, inp, err)
    
    def foErr(self, state, inp, err, msg=None):
        msg = 0
        return super().foErr(state, inp, err, msg)
    
class Average2(SM):
    """  
    Average2 SM:
    fn(s,i) = i
    fo(s,i) = (s + i) / 2
    startState = 0

    error handling functions:
    efn(s,i) = s
    efo(s, i) = None
    """

    def __init__(self) -> None:
        # the startState is always 0
        super().__init__(0)
    
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        kwargs = {
            'fn' : lambda s,i : i,
            'fo' : lambda s,i : (s + i) / 2
        }
        return super().getNextValues(state, inp, **kwargs)
    
class ABC(SM):
    """  
    class Language Acceptor
    S = {0, 1, 2, 3}
    I = {a, b, c}
    O = {True, False}
    n(s,i):
        if s == 0 and i == a : 1 
        if s == 1 and i == b : 2
        if s == 2 and i == c : 0
        else : 3
    
    o(s,i):
        if s == 0 and i == a : True 
        if s == 1 and i == b : True
        if s == 2 and i == c : True
        else : False

    o(s,i):
        if n(s,i) == 3 : False
        else : True
    """
    def __init__(self) -> None:
        super().__init__(0)

    def getNextValues(self, state, inp, **kwargs) -> tuple:
        kwargs = {
            'fn' : lambda s,i : 1 if s==0 and i=='a' else 2 if s==1 and i=='b' else 0 if s==2 and i=='c' else 3,
            'fo' : lambda s,i : True if s==0 and i=='a' or s==1 and i=='b' or s==2 and i=='c' else False,
            'efn' : 'fn',
            'efo' : 'fo'
        }
        return super().getNextValues(state, inp, **kwargs)
    
class UpDown(SM):
    """  
    class for Up Down counter State Machine subcalss of SM
    S = integers
    I = {u,d}
    O = integers
    startState : user defined
    fn(s,i) =
        s + 1 if i = u
        s - 1 if i = d
    
    fo(s,i) = fn(s,i)

    error handling function
    efn(s,i) = s (the state unchanged in error)
    efo(s,i) = None (the output is None in error)
    """

    #fo = fn = lambda s,i : s + 1 if i == 'u' else s - 1 if i == 'd' else self.throw(RuntimeError(None))
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        kwargs = {
            'fn' : lambda s,i : s + 1 if i == 'u' else s - 1 if i == 'd' else self.throw(RuntimeError(None)),
            'fo' : lambda s,i : s + 1 if i == 'u' else s - 1 if i == 'd' else self.throw(RuntimeError(None))
            # BUG: why this can't just use 'fo' : 'fn' ? While the ABC can?? maybe throw??
        }
        return super().getNextValues(state, inp, **kwargs)

class Delay(SM):
    """  
    class for Delay State Machine subclass of SM
    S = Any
    I = Any
    O = Any
    startState : user defined

    fn(s,i) = i
    fo(s,i) = s
    """
    
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        kwargs = {
            'fn' : lambda s,i : i,
            'fo' : lambda s,i : s
        }
        return super().getNextValues(state, inp, **kwargs)

class SumLast3(SM):
    """  
    class for Sum Last 3 components
    Specification:
    S = number (int and float)
    I = number (int and float)
    O = number (int and float)
    StartState = (0,0)

    fn(s,i) = (s[1], i)
    fo(s,i) = s[0] + s[1] + i

    error function:
    efn(s,i) = s
    efo(s,i) = None
    """
    def __init__(self) -> None:
        """  
        the startState = (0,0)
        """
        super().__init__((0, 0))

    def getNextValues(self, state, inp, **kwargs) -> tuple:
        kwargs = {
            'fn' : lambda s,i : (s[1], i) if type(i) is int or type(i) is float else self.throw(TypeError('invalid input')), 
            'fo' : lambda s,i : s[0] + s[1] + i
        }
        return super().getNextValues(state, inp, **kwargs)

    def foErr(self, s, i, e, msg=None):
        """  
        If the input is invalid then the ouput must returns error message
        error custom message must be put in args[0] (first argument in args*)
        of any type of Errors
        """
        msg = e.args[0]
        return super().foErr(s, i, e, msg)

class Increment(SM):
    """  
    Increment state machine:
    fn (s, i) = ?
    fo (s, i) = i + k (k is a constant)
    """
    def __init__(self, incr, initVal=0) -> None:
        self.incr = incr
        super().__init__(initVal)
    
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        kwargs = {
            'fn' : lambda s, i : i + self.incr,
            'fo' : lambda s, i : self.safeAdd(inp, self.incr)
        }
        return super().getNextValues(state, inp, **kwargs)

class Negation(SM):
    """  
    Negation State Machine: 
    Pure function given boolean returns negation of the argument
    fn (s,i) = not(i)
    fo (s,i) = not(i)
    """
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        # check if inp is Boolean

        kwargs = {
            'fn' : lambda s, i : not i if isinstance(i, bool) else self.throw(TypeError(None)),
            'fo' : lambda s, i : not i
        }
        return super().getNextValues(state, inp, **kwargs)

class Adder(SM):
    """  
    Adder input tuple elements together simultaneously
    Pure function given a tuple safe add the elements
    fn(s,i) = s
    fo(s,i) = safeAdd(splitValue(i))
    """

    def getNextValues(self, state, inp, **kwargs) -> tuple:
        (i1, i2) = self.splitValue(inp)
        try:
            o = self.safeAdd(i1, i2)
        except TypeError as e:
            return (state, e.args[0])
        except:
            "other error raised"
        return (state, o)

class Wire(SM):
    """  
    Wire just pass trhought he input
    given state and input
    fn(s,i) = s
    fo(s,i) = i
    """
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        kwargs = {
            'fn' : lambda s, i : s,
            'fo' : lambda s, i : i
        }
        return super().getNextValues(state, inp, **kwargs)

class Fixed(SM):
    """  
    Fixed class always output constant number output
    given k at init as constant
    fn(s,i) = s
    fo(s,i) = k
    """
    def __init__(self, k, initVal=0) -> None:
        super().__init__(initVal)
        self.k = k

    def getNextValues(self, state, inp, **kwargs) -> tuple:
        kwargs = {
            'fn' : lambda s, i : s,
            'fo' : lambda s, i : self.k
        }
        return super().getNextValues(state, inp, **kwargs)

class Multiplier(SM):
    """  
    Given tuple of inputs
    Returns safe mul of the inputs
    """
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        (i1, i2) = self.splitValue(inp)

        try:
            o = self.safeMul(i1, i2)
        except TypeError as e:
            return (state, e.args[0])
        except:
            "other error raised"
        
        return (state, o)

class ConsumeFiveValues(SM):
    """  
    iniVal = (count = 0, total = 0)
    fn : s, i = (count + 1, total + inp)
    fo : s, i = total + inp if count == 4 else None

    -- if count is already 5 then break
    """
    def __init__(self, initVal=(0, 0)) -> None:
        super().__init__(initVal)
    
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        (count, total) = state
        if count == 4:
            return ((count + 1, total + inp), total + inp)
        else:
            return ((count + 1, total + inp), None)
    
    def done(self, state) -> bool:
        # check if the count (part of state) is 5,
        # if yes the transduce is done
        (count, total) = state
        return count == 5

class Repeat(SM):
    """  
    Given:
    sm : SM = constituent state machine
    n : int = how many times it should repeat (DEFAULT = None)
    WARNING: left the n in Default value (None) can result infinite loop
    state type = (count, sm state)
    """
    def __init__(self, sm: SM, n: int = None) -> None:
        """  
        full override of the init
        """
        self.sm = sm
        self.n = n
        self.startState = (0, self.sm.startState)
    
    def advanceIfDone(self, counter, smState)->tuple:
        """  
        add counter when sm is done
        reset the sm state to sm.startState
        return (counter, state)
        """
        while self.sm.done(smState) and not self.done((counter, smState)):
            # while repeat is not done even as the constituen sm is done:
            counter += 1
            # reset the constituent sm back to its startState
            smState = self.sm.startState
        return (counter, smState)
    
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        (counter, smState) = state
        (smState, o) = self.sm.getNextValues(smState, inp)
        (counter, smState) = self.advanceIfDone(counter, smState)
        return ((counter, smState), o)

    def done(self, state) -> bool:
        (counter, smState) = state
        return counter == self.n


class CharTSM(SM):
    """  
    Simple subclass of SM used to test Repeat class
    Given:
    c: str = character 
    state = boolean
    """
    def __init__(self, c:str, initVal=False) -> None:
        super().__init__(initVal)
        self.c = c

    def getNextValues(self, state, inp, **kwargs) -> tuple:
        return (True, self.c)
    
    def done(self, state) -> bool:
        return state

class Sequence(SM):
    """  
    Run all SMs in the list sequentially one by one after one is done before the other
    untill all SMs in the list is done.
    given:
    smList: list = list of SM to run sequentially

    startState = (counter, smList[0].startState)
    """
    def __init__(self, smList: list) -> None:
        self.smList = smList
        self.startState = (0, self.smList[0].startState)
        # set the counter limit to the length of the smList
        self.n = len(smList)

    def advancedIfDone(self, counter, smState):
        while self.smList[counter].done(smState) and counter + 1 < self.n:
            counter += 1
            smState = self.smList[counter].startState
        return (counter, smState)

    def getNextValues(self, state, inp, **kwargs) -> tuple:
        (counter, smState) = state
        (smState, o) = self.smList[counter].getNextValues(smState, inp)
        (counter, smState) = self.advancedIfDone(counter, smState)
        return ((counter, smState), o)
    
    def done(self, state) -> bool:
        (counter, smState) = state
        return self.smList[counter].done(smState)

class RepeatUntil(SM):
    """  
    class RepeatUntil 
    Given: 
    condition: function = function to return boolean to define the limit is achieved
    sm: SM = constituent state machine object

    fn : s,i : (conditionTrue, smState)
    fo : s,i : o
    init state = (False, self.sm.startState)

    condition : done when condition is met AND constituent SM is done (MUST BE BOTH)
    """
    def __init__(self, condition, sm:SM) -> None:
        self.sm = sm # constituent SM
        self.condition = condition # function when done is met.
        self.startState = (False, self.sm.startState)

    def advancedIfDone(self, condTrue, smState):
        # repeat if cond is not true
        if not self.done((condTrue, smState)):
            smState = self.sm.startState
        return (condTrue, smState)
    
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        (condTrue, smState) = state
        (smState, o) = self.sm.getNextValues(smState, inp)
        condTrue = self.condition(inp)
        # repeat if necessary
        (condTrue, smState) = self.advancedIfDone(condTrue, smState)
        return ((condTrue, smState), o)
    
    def done(self, state) -> bool:
        (condTrue, smState) = state
        return self.sm.done(smState) and condTrue


class Until(RepeatUntil):
    """  
    class RepeatUntil subclass of Until subclass of SM
    Given:
    condition: function = function to return boolean define the limit is achieved
    sm : SM = constitiuent state machine

    fn : s,i : (conditionTrue, smState)
    fo : s,i : o
    init state = (False, self.sm.startState)

    condition : done when condition is met OR constituent SM is done (which one is first)
    """
    # TODO: done function override