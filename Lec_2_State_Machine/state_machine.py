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
            # NOTE: getNextValues() function must return (next state, output)
            print(f"In: {inp} Out: {o} Next State: {s}")
            result.append(self.step(inp))
        
        return result

    def run(self, n = 10):
        """  
        step but no input is given
        """
        return self.transduce([None] * n)

    def getNextValues(self, state, inp) -> tuple:
        """  
        returns : tuple -> (next state, output)
        this is supposed to be abstract function which must be defined in sub class
        for now let's just pass it
        NOTE: this is PURE FUNCTION don't change self.state from this function
        """
        pass


class Accumulator(SM):
    """  
    sub class of SM which implementation is Accumulator State Machine
    """
    
    def getNextValues(self, state, inp) -> tuple:
        """  
        PURE FUNCTION MUST NOT change self.state
        """
        # remember in given start of time the state is the same as previous output
        try: 
            return (state + inp, state + inp)
        except TypeError:
            # expect classes that do not give any
            return (state + 0, state + 0)
    
class Gain(SM):
    """  
    Gain State machine:
    n(s,i) = s
    o(s,i) = s * i
    startState : user determined
    """
    
    def getNextValues(self, state, inp) -> tuple:
        try:
            return(state, inp * state)
        except TypeError:
            return(state, 0 * state)
    
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
    