"""  
Problem Wk.3.3.1: Map
link to page: https://ocw.mit.edu/courses/6-01sc-introduction-to-electrical-engineering-and-computer-science-i-spring-2011/resources/mit6_01scs11_3_3_1/

Part 1: mapList

Define a procedure mapList that takes two arguments, a procedure of one argument
and a list. It returns the list of the results of applying the procedure to each of the
elements of the list.
>>> def sq(x): return x*x
>>> mapList(sq, [1,2,3,4])
[1, 4, 9, 16]
You must use a list comprehension.
"""

def sq(x:int) -> int: return x*x

def mapList(fn, input_list:list)-> list:
    """  
    given:
    fn : function = python method will be implemented to element of input_list
    input_list: list = list of integer

    return : list of int = list of function output implemented on element of input list
    """
    return [fn(x) for x in input_list]

# test Part 1: mapList
print(f"Test Part1:\nmapList(sq, [1,2,3,4]) : {mapList(sq, [1,2,3,4])}")

"""  
Part 2: sumAbs

Use mapList to define a procedure called sumAbs that given a list of numbers, returns the
sum of the absolute values of the numbers.
Your procedure must use mapList. You should be aware of the sum and abs built in
functions in Python
"""

def sumAbs(input_list:list) -> int:
    """  
    given:
    input_list : list = list of int

    return : int = sum of absolute value on elements in the mapList of input_list
    """
    return sum([abs(x) for x in mapList(sq, input_list)])

# test Part2:
print(f"Test Part 2:\nsumAbs([1,2,3,4]): {sumAbs([1,2,3,4])}")
print(f"Test Part 2:\nsumAbs([1,-2,3,-4]): {sumAbs([1,-2,3,-4])}")

"""  
Part 3: mapSquare

Define a procedure mapSquare that takes two arguments, a procedure of two arguments
and a list. It returns a list of lists of all the results of applying the procedure to all
combinations of the values in the list.
>>> def diff(x, y): return x - y
>>> mapSquare(diff, [1,2,3])
[[0, -1, -2], [1, 0, -1], [2, 1, 0]]
Note that this list is:
[[1-1, 1-2, 1-3], [2-1, 2-2, 2-3], [3-1, 3-2, 3-3]]
You must use a list comprehension. Hint: Think about using nested list
comprehensions.
"""

def diff(x:int, y:int)-> int: return x-y

def mapSquare(procedure, input_list:list)-> list:
    """  
    Given:
    procedure: function = defined function implemented to the list element
    input_list: list = list of integer

    return: nested list = all possible operation combination on the input list elements
    """
    return [[diff(input_list[i], y) for y in input_list] for i in range(len(input_list))]

# test Part 3
print(f"Test Part 3:\nmapSquare(diff, [1,2,3]): {mapSquare(diff, [1,2,3])}")
