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

        if not verbose : return [self.step(inp) for inp in inps]

        print(f"Start state: {self.state}")

        for inp in inps:
            (s, o) = self.getNextValues(self.state, inp)
            
            print(f"In: {inp} Out: {o} Next State: {s}")
            result.append(self.step(inp))
        
        return result

    def run(self, n = 10):
        """  
        step but no input is given
        """
        return self.transduce([None] * n)

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
    startState : user determined

    errror handling function:
    efo(s,i) = efn(s,i) = 0
    """
   
    def __init__(self, initVal=0) -> None:
        super().__init__(initVal)
        self.k = initVal
    
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


    # def getNextValues(self, state, inp, definp=0, fn = lambda s,i : None, fo = lambda s,i : None) -> tuple:
    #     try:
    #         fn = lambda s,i : i
    #         fo = lambda s,i : (s + i) / 2
    #         return super().getNextValues(state, inp, definp, fn, fo)
    #     except TypeError:
    #         fn = lambda s,i : 0
    #         fo = lambda s,i : 0
    #         return super().getNextValues(state, inp, definp, fn, fo)
    
    def getNextValues(self, state, inp, fn=lambda s,i : None, fo=lambda s,i : None, efn=None, efo=None)->tuple:
        fn = lambda s,i : i
        fo = lambda s,i : (s + i) / 2
        
        return super().getNextValues(state, inp, fn, fo, efn, efo)
    
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

    def getNextValues(self, state, inp, fn=lambda s,i : None, fo=lambda s,i : None, efn=None, efo=None)->tuple:
        efn = fn = lambda s,i : 1 if s==0 and i=='a' else 2 if s==1 and i=='b' else 0 if s==2 and i=='c' else 3
        efo = fo = lambda s,i : True if s==0 and i=='a' or s==1 and i=='b' or s==2 and i=='c' else False
        
        return super().getNextValues(state, inp, fn, fo, efn, efo)
    
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

    # : define and test getNextValues according to the new standard
    def getNextValues(self, state, inp, fn=lambda s,i : None, fo=lambda s,i : None, efn=None, efo=None)->tuple:
        fo = fn = lambda s,i : s + 1 if i == 'u' else s - 1 if i == 'd' else self.throw(RuntimeError(None))
        # NOTE: I use run time error to cover for both Type error like passing None of True False 
        # and wrong string 
        
        return super().getNextValues(state, inp, fn, fo, efn, efo)

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
    # TODO: define and test getNextValues according to the new standard
    def getNextValues(self, state, inp, fn=lambda s,i : None, fo=lambda s,i : None, efn=None, efo=None)->tuple:
        fn = lambda s,i : i
        fo = lambda s,i : s
        return super().getNextValues(state, inp, fn, fo, efn, efo)

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

    def getNextValues(self, state, inp, fn=lambda s,i : None, fo=lambda s,i : None, efn=None, efo=None)->tuple:
        """  
        get the next state and current output based on specification
        """
        fn = lambda s,i : (s[1], i) if type(i) is int or type(i) is float else self.throw(TypeError('invalid input'))
        fo = lambda s,i : s[0] + s[1] + i
        return super().getNextValues(state, inp, fn, fo, efn, efo)

    def foErr(self, s, i, e, msg=None):
        """  
        If the input is invalid then the ouput must returns error message
        error custom message must be put in args[0] (first argument in args*)
        of any type of Errors
        """
        msg = e.args[0]
        return super().foErr(s, i, e, msg)
