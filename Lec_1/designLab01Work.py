#
# File:   designLab01Work.py
# Author: 6.01 Staff
# Date:   02-Sep-11
#
# Below are templates for your answers to three parts of Design Lab 1

#-----------------------------------------------------------------------------
import cmath
# choose this if you wish to process complex number.

def fib(n):
    # Delete the pass statement below and insert your own code
    # for safety unable to process negative arguments
    if n < 0 : raise ValueError("argument cannot be negative")
    if n == 0 : return 0
    if n == 1 : return 1
    else : return fib(n-1) + fib(n-2)

#-----------------------------------------------------------------------------

class V2(object):
    # Delete the pass statement below and insert your own code
    def __init__(self, x : float, y : float) -> None:
        self.x = float(x)
        self.y = float(y)

    def getX(self) -> float:
        return self.x

    def getY(self) -> float:
        return self.y

    def __str__(self):
       
        return 'V2[' + str(self.x) + ", " + str(self.y) + ']'

    def add(self, v):
        return V2(self.x + v.getX(), self.y + v.getY())

    def mul(self, v):
        return V2(self.x * v, self.y * v)

    def __add__(self, v):
        return self.add(v)

    def __mul__(self, v):
        return self.mul(v)

    
    
#-----------------------------------------------------------------------------

class Polynomial:
    # Delete the pass statement below and insert your own code
    def __init__(self, coeffs : list) -> None:
        self.order = len(coeffs) - 1
        self.coeffs = coeffs
    
    def __str__(self) -> str:
        text = ''
        order = self.order
        for coeff in self.coeffs:
            if coeff == 0: continue
            if order != self.order and coeff > 0 : text += '+ '
            if order > 1 : 
                text += f'{float(coeff):.3f}' + ' z**' + str(order) + ' '
            elif order == 1:
                text += f'{float(coeff):.3f}' + ' z '
            else:
                text += f'{float(coeff):.3f}'
            
            order -= 1
        return text

    def getReps(self) -> str:
        result = ""
        for i in range(len(self.coeffs)):
            if i == 0 : result += str(self.coeffs[0])
            else : result += (" " + str(self.coeffs[i]))
        return result
    
    def getCoeffs(self) -> list:
        return self.coeffs

    def getOrder(self) -> int:
        return self.order
    
    def add(self, p2 ) :
        co_ex = []
        coeffs1 = self.coeffs.copy()
        coeffs2 = p2.coeffs.copy()
        # I need to copy the coeffs to maintain the original list while I preseve this :

        while len(coeffs1) > 0 and len(coeffs2) > 0:
            co_ex.insert(0, coeffs1[-1] + coeffs2[-1])
            coeffs2.pop()
            coeffs1.pop()
        
        # check which coeffs is still has element in it :
        # NOTE: the coeefs here list added to list thus use operator + instead of extend
        if len(coeffs1) > 0 : return Polynomial(coeffs1 + co_ex)
        return Polynomial(coeffs2 + co_ex)

    def mul(self, p2):
        new_list = []
        coeffs1 = list(reversed(self.coeffs))
        coeffs2 = list(reversed(p2.getCoeffs()))
        # prepare the new list filled with all zero with length to occupy the new order after mul
        for i in range(self.order + p2.getOrder() + 1): new_list.append(0)

        for j in range(len(coeffs1)):
            for k in range(len(coeffs2)):
                new_list[j + k] += coeffs1[j] * coeffs2[k]

        new_list.reverse()
        return Polynomial(new_list)

    def roots(self):
        result = []
        if self.order == 1:
            return [-self.coeffs[1] / self.coeffs[0]]
        elif self.order == 2:
            a = self.coeffs[0]
            b = self.coeffs[1]
            c = self.coeffs[2]
            return [(-b + cmath.sqrt(b**2 - 4*a*c))/(2*a), (-b - cmath.sqrt(b**2 - 4*a*c))/(2*a)]

        raise ValueError("Order too high to solve for roots")

    def __add__(self, po):
        return self.add(po)

    def __mul__(self, p2):
        return self.mul(p2)

    def __call__(self, x) -> float:
        """  
        return the result of function when passed an argument x
        """
        result = 0.0
        order = self.order
        for coeff in self.coeffs:
            result += float(coeff) * float(x) ** (order)
            order -= 1
        return result

def runPoly():
    p1 = Polynomial([1,2,3])
    p2 = Polynomial([100,200])
    print(p1.add(p2))

if __name__ == '__main__':
    runPoly()