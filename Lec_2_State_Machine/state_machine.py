"""  
All types of state machine classes
"""

# create super class (meant to be abstract) 
class SM:
    """  
    This SM class is intended as Abstract class
    Thus it is not meant to be instantiated to create and object
    Hence this will be used as blueprint to create another sub - class

    thus, many variables here are not defined yet which should be declared and defined in sub class

    In the sub-class you must define the startState variable
    also defince getNextValues(self, state, inp) function
    NOTE: getNextValues is a pure function it will not change the value of self.state (that's the job of self.step function)
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

        efn = n(s,i) when i = None and handled the raised TypeError
        efo = o(s,i) when i = None and handled the raised TypeError 
        """
        try:
            return(fn(state, inp), fo(state, inp))
        except TypeError:
            # provide empty input default value
            return(efn(state, inp), efo(state, inp))
    

class Accumulator(SM):
    """  
    sub class of SM which implementation is Accumulator State Machine
    n(s,i) = s + i
    o(s,i) = s + i
    startState : user defined
    """
    
    def getNextValues(self, state, inp, fn=lambda s, i: None, fo=lambda s, i: None, efn=lambda s, i: None, efo=lambda s, i: None):
        fo = fn = lambda s,i : s + i
        efo = efn = lambda s,i : s + 0
        
        return super().getNextValues(state, inp, fn, fo, efn, efo)
    
        
    
class Gain(SM):
    """  
    Gain State machine:
    n(s,i) = k * i 
    o(s,i) = k * i
    startState : user determined
    """
   
    def __init__(self, initVal=0) -> None:
        super().__init__(initVal)
        self.k = initVal
    
    def getNextValues(self, state, inp, fn=lambda s, i: None, fo=lambda s, i: None, efn=lambda s, i: None, efo=lambda s, i: None):
        # I put the constan self.k directly to the function
        # n(s,i) = k * i
        # o(s,i) = k * i
        fn = lambda s,i : self.k * i
        efn = lambda s,i : 0
        fo = fn
        efo = efn
        return super().getNextValues(state, inp, fn, fo, efn, efo)
    
class Average2(SM):
    """  
    Average2 SM:
    n(s,i) = i
    o(s,i) = (s + i) / 2
    startState = 0
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
        efo = efn = lambda s,i : 0
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
        fn = lambda s,i : 1 if s==0 and i=='a' else 2 if s==1 and i=='b' else 0 if s==2 and i=='c' else 3
        fo = lambda s,i : True if s==0 and i=='a' or s==1 and i=='b' or s==2 and i=='c' else False
        efn = lambda s,i : 3
        efo = lambda s,i : False
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
    """
    # TODO: define and test getNextValues according to the new standard
    def getNextValues(self, state, inp, definp=0, fn = lambda s,i : None, fo = lambda s,i : None) -> tuple:
        return super().getNextValues(state, inp, definp, fn, fo)

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
    def getNextValues(self, state, inp, definp=0, fn=None, fo=None) -> tuple:
        return super().getNextValues(state, inp, definp, fn, fo)
