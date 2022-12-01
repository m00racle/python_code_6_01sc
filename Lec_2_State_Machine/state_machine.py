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
    def start(self):
        self.state = self.startState
    
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
        return self.transduce([None] * n)

class Accumulator(SM):
    """  
    sub class of SM which implementation is Accumulator State Machine
    """
    def __init__(self, initialValue = 0) -> None:
        self.startState = initialValue
    
    def getNextValues(self, state, inp) -> tuple:
        """  
        PURE FUNCTION MUST NOT change self.state
        """
        # remember in given start of time the state is the same as previous output
        if inp == None : inp = 0
        return (state + inp, state + inp)
    
    