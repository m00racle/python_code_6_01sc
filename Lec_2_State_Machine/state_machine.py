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

    def getNextValues(self, state, inp, definp = 0, fs = None, fo = None) -> tuple:
        """  
        returns : tuple -> (next state, output)
        this is supposed to be abstract function which must be defined in sub class
        for now let's just pass it
        definp is the default value when the input is None
        fs = n(s,i) -> programmer must provide function definition 
        fo = o(s,i) -> programmer must provide function definition
        NOTE: this is PURE FUNCTION don't change self.state from this function
        """
        try:
            return(fs(state, inp), fo(state, inp))
        except TypeError:
            # provide empty input default value
            return(fs(state, definp), fo(state, definp))
    

class Accumulator(SM):
    """  
    sub class of SM which implementation is Accumulator State Machine
    n(s,i) = s + i
    o(s,i) = s + i
    startState : user defined
    """
    
    def getNextValues(self, state, inp, definp=0, fs=None, fo=None) -> tuple:
        fs = lambda s,i : s + i
        fo = fs
        return super().getNextValues(state, inp, definp, fs, fo)
    
        
    
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
    
    def getNextValues(self, state, inp, definp=0, fs=None, fo=None) -> tuple:
        # I put the constan self.k directly to the function
        # n(s,i) = k * i
        # o(s,i) = k * i
        fs = lambda s,i : self.k * i
        fo = fs
        return super().getNextValues(state, inp, definp, fs, fo)
    
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


    def getNextValues(self, state, inp) -> tuple:
        try:
            return (inp, (state + inp)/2)
        except TypeError:
            return (0, 0)
    
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
        if n(s,i) == 3 : False
        else : True
    """
    def __init__(self) -> None:
        super().__init__(0)

    def getNextValues(self, state, inp) -> tuple:
        try:
            if state == 0 and inp == 'a' : return (1, True)
            elif state == 1 and inp == 'b' : return (2, True)
            elif state == 2 and inp == 'c' : return (0, True)
            else : return (3, False)
        except TypeError:
            return (3, False)
    