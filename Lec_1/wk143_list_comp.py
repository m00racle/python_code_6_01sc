"""  
This is the answer for Problem Wk.1.4.3: List Comprehensions

"""

def evenSquare(l: list) -> list:
    """  
    Given l a List of integers 
    Returns List of squae numbers from the l
    """
    result = []
    for x in l:
        if x % 2 == 0 : result.append(x)

    return result

def sumAbsProd(l1: list, l2: list) -> int:
    """  
    Given two list l1 and l2
    Returns int that is the sum of all list multiplications (in absolute form)
    """
    result = []
    for x in l1:
        for y in l2:
            result.append(abs(x*y))
    
    return sum(result)
