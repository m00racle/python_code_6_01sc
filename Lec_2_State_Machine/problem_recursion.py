""" 
    this is specific for Problem Wk. 2.3.4 and 2.3.5
"""

def add(a,b):
    """  
        recursion for addition
        a = any number
        b = positive integer
        return any number = a + b
    """
    if b == 0: return a
    else: return add(a, b-1) + 1

def sub(a,b):
    """  
        recursion for subtraction
        a = any number
        b = positive integer
        return any number = a - b
    """
    if b == 0: return a
    else : return sub(a, b-1) - 1

def slowMod(a,b):
    """  
        combination of using add and sub function to calculate mod
        a = positive integer
        b = positive integer
        return integer = a % b
    """
    if b > a : return a
    count = b
    while count <= a:
        check = add(count,b)
        if check > a : break
        count = check
    
    return sub(a, count)

# run main
print(f"add(5,2) = {add(5,2)}")
print(f"add(-5,2) = {add(-5,2)}")
print(f"add(5.5,2) = {add(5.5,2)}")
print(f"sub(5,2) = {sub(5,2)}")
print(f"sub(-5,2) = {sub(-5,2)}")
print(f"sub(5.5,2) = {sub(5.5,2)}")
print(f"slowMod(5,2) = {slowMod(5,2)}")
print(f"slowMod(6,2) = {slowMod(6,2)}")
print(f"slowMod(8,3) = {slowMod(8,3)}")
print(f"slowMod(4,6) = {slowMod(4,6)}")
print(f"slowMod(9,9) = {slowMod(9,9)}")