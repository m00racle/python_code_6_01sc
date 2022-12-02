"""  
All types of state machine classes
"""

# create super class (meant to be abstract) 
class SM:
    """  
    This SM class is intended as Abstract class
    Thus it is not meant to be instantiated to create and object
    Hence this will be used as blueprint to create another sub - class
    """
    def __init__(self, initVal = 0) -> None:
        self.startState = initVal

    def start(self):
        self.state = self.startState

    def getState(self):
        return self.state
    
    def step(self, inp):
        """  
        find the next state and returns output for each time given inp : input
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

    def getNextValues(self, state, inp, fn=lambda s,i : None, fo=lambda s,i : None, efn=lambda s,i : None, efo=lambda s,i : None):
        """  
        returns : tuple -> (next state, output)
        this is supposed to be abstract function which must be defined in sub class
        
        fn = n(s,i) -> programmer must provide function definition 
        fo = o(s,i) -> programmer must provide function definition
        NOTE: this is PURE FUNCTION don't change self.state from this function

        efn = n(s,i) when i = None and handled the raised Exception (including typeError)
        efo = o(s,i) when i = None and handled the raised Exception (including typeError) 
        """
        try:
            return(fn(state, inp), fo(state, inp))
        except Exception:
            # provide state and output when the input raise any exception (including TypeError)
            return(efn(state, inp), efo(state, inp))
    

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
    
    def getNextValues(self, state, inp, fn=lambda s, i: None, fo=lambda s, i: None, efn=lambda s, i: None, efo=lambda s, i: None):
        fo = fn = lambda s,i : s + i
        efn = lambda s,i : s
        
        return super().getNextValues(state, inp, fn, fo, efn, efo)
    
        
    
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
    
    def getNextValues(self, state, inp, fn=lambda s, i: None, fo=lambda s, i: None, efn=lambda s, i: None, efo=lambda s, i: None):
        # I put the constan self.k directly to the function
        # n(s,i) = k * i
        # o(s,i) = k * i
        fo = fn = lambda s,i : self.k * i
        efo = efn = lambda s,i : 0
        
        return super().getNextValues(state, inp, fn, fo, efn, efo)
    
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
    
    def getNextValues(self, state, inp, fn=lambda s, i: None, fo=lambda s, i: None, efn=lambda s, i: None, efo=lambda s, i: None):
        fn = lambda s,i : i
        fo = lambda s,i : (s + i) / 2
        efn = lambda s,i : s
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

    def getNextValues(self, state, inp, fn=lambda s, i: None, fo=lambda s, i: None, efn=lambda s, i: None, efo=lambda s, i: None):
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
    def getNextValues(self, state, inp, fn=lambda s, i: None, fo=lambda s, i: None, efn=lambda s, i: None, efo=lambda s, i: None):
        fo = fn = lambda s,i : s + 1 if i == 'u' else s - 1 if i == 'd' else self.throw(ValueError("unidentified input value"))
        efn = lambda s,i : s
        return super().getNextValues(state, inp, fn, fo, efn, efo)

    def throw(self, excep):
        """  
        helper function to throw or raise exception from lambda function
        This is because lambda function in Python can't directly raise any exception.
        """
        raise excep

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
    def getNextValues(self, state, inp, fn=lambda s, i: None, fo=lambda s, i: None, efn=lambda s, i: None, efo=lambda s, i: None):
        fn = lambda s,i : i
        efn = fo = lambda s,i : s
        return super().getNextValues(state, inp, fn, fo, efn, efo)
