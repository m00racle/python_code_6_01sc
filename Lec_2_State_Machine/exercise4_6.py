from state_machine import SM

class Exercise1b(SM):
    """  
    generate outputs every 3 steps read Exercise 4-6-1 B
    """

class Exercise1cHelper(SM):
    """  
    combine this class with sm.Repeat 
    to solve the Exercise 4-6-1 C
    """

# Exercise 4-6-2 
class CountingStateMachine(SM):
    """  
    states are always integers that start at 0 and increment by 1 on each transition
    """
    def __init__(self, initVal=0) -> None:
        self.startState = 0
    
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        return (state + 1, self.getOutput(state, inp))

class CountMod5(CountingStateMachine):
    """  
    class used to solve Exercise 4-6-2
    """
    def getOutput(self, state, inp):
        return state % 5

class AlternateZeros(CountingStateMachine):
    """  
    state machines for which, on even steps, the output is the same as the input, and on odd steps, the output is 0.
    """
    def getOutput(self, state, inp):
        if state % 2 != 0 : return 0
        return inp