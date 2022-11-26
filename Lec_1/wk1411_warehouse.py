"""  
Problem Wk.1.4.11: Warehouse [Optional]
We'll be building a set of procedures to model a simple warehouse accounting system,
which maintains the inventory for a set of commodities, which we will represent by
strings, e.g. 'a', 'b', 'c'. So, the warehouse could have 10 units of 'a', 20 of 'b' and 0 of
'c'. 
"""

class Warehouse():
    def __init__(self, totals : dict) -> None:
        self.totals = totals
    
    def process(self, trans : list) -> None:
        if trans[0] == 'receive':
            if trans[1] in self.totals.keys():
                self.totals[trans[1]] += trans[2]
            else:
                self.totals[trans[1]] = trans[2]
        elif trans[0] == 'ship':
            if trans[1] in self.totals.keys():
                if self.totals[trans[1]] > trans[2]:
                    self.totals[trans[1]] -= trans[2]
                else: raise ValueError("insufficient available items to ship from warehouse")
            else: raise ValueError("unidentified commodity in the warehouse")
        else: raise ValueError("unidentified order given")

    def lookoup(self, item : str) -> int :
        if item in self.totals.keys() :
            return self.totals[item]
        else:
            return 0
    

def werehouseProcess(totals : dict, trans : list) -> dict:
    """  
    process the transaction
    """
    
    if trans[0] == 'receive':
        if trans[1] in totals.keys():
            totals[trans[1]] += trans[2]
        else:
            totals[trans[1]] = trans[2]
    elif trans[0] == 'ship':
        if trans[1] in totals.keys():
            if totals[trans[1]] > trans[2]:
                totals[trans[1]] -= trans[2]
    else: raise ValueError("order unidentified")

    return totals
