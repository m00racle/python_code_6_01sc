from state_machine import SM

"""  
File for all Parallel classes
"""

class Parallel(SM):
    """  
    class parallel
    Having the same input flow but having two prallel output flow
    """
    def __init__(self, sm1 : SM, sm2 : SM) -> None:
        """  
        description: initialize the instance of Parallel type object

        Paramenter:
        sm1 : SM = State Machine type object 1
        sm2 : SM = State Machine type object 2

        Super:
        initVal : tuple = (sm1.startState, sm2.startState)
        """
        self.sm1 = sm1
        self.sm1.start()
        self.sm2 = sm2
        self.sm2.start()
        # set the initVal and sent it to super to create startState and log dict
        initVal = (sm1.getState(), sm2.getState())
        super().__init__(initVal)   

    def getNextValues(self, state, inp, **kwargs) -> tuple:
        """  
        description: get the next values (states, outputs) of the Parallel State Machine
        Fully override the SM getNextValue function (super) 
        pass the processing for each to sm1 and sm2 both are SM instances thus

        Error handling will also passed to each sm1 and sm2 to handle appropriately

        Parameters:
        state : (Any, Any) = current state of the Parallel SM 
        inp : Any = the current input to the Parallel SM

        Returns : tuple = ((sm1.nextState, sm2.nextState), (sm1.output, sm2.output))
        """
        (s1, s2) = state
        (next_s1, o1) = self.sm1.getNextValues(s1, inp)
        (next_s2, o2) = self.sm2.getNextValues(s2, inp)
        return ((next_s1, next_s2), (o1, o2))

class Parallel2(Parallel):
    """  
    Class Parallel with 2 inputs and 2 outputs
    S = {Any}
    I + {Anu}
    O = {Any}
    """

    def splitValue(self, v: any)-> tuple:
        """  
        basically verify that the inputs are in pair and defined
        """
        if v == 'undefined' or type(v) != tuple:
            return ('undefined', 'undefined')
        elif len(v) != 2:
            return ('undefined', 'undefined')
        else:
            return v

    
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        """  
        Returns the output and next state for each SM
        if the value is considered as undefined by the splitValue function then 
        for both SM: output: undefined , next state = current valid state (retained)
        """
        (s1,s2) = state
        (i1, i2) = self.splitValue(inp)
        if i1 == 'undefined' or i2 == 'undefined':
            res1 = (self.fnErr(s1, i1, RuntimeError('undefined')), self.foErr(s1, i1, RuntimeError('undefined')))
            res2 = (self.fnErr(s2, i2, RuntimeError('undefined')), self.foErr(s2, i2, RuntimeError('undefined')))
        else:
            res1 = self.sm1.getNextValues(s1, i1)
            res2 = self.sm2.getNextValues(s2, i2)
        
        (next_s1, o1) = res1
        (next_s2, o2) = res2
        return ((next_s1, next_s2), (o1, o2))

class ParallelAdd(Parallel):
    """  
    Similar to the class Parallel but only have single outcomes which is the sum of each SM outputs
    """
    