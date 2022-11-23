"""  
Problem Wk.1.3.5: Polynomial Representations
"""

import designLab01Work as lab

def part1():
    print("1. Enter the sequence of coefficients for the polynomial 3x**3 + 2x - 4")
    print(f'"answer: {lab.Polynomial([3, 0, 2, 4]).getReps()}')
    
    print("\n2. Enter the sequence of coefficients for the polynomial 2x + 7:")
    print(f'"answer: {lab.Polynomial([2, 7]).getReps()}')

    print("\n3. Enter the sequence of coefficients for the polynomial that is the sum of the two polynomials above (3x**3 + 2x - 4) + (2x + 7):")
    print((lab.Polynomial([3,0,2,4]) + lab.Polynomial([2,7])).getReps())
    print(f"prove: {lab.Polynomial([3,0,2,4]) + lab.Polynomial([2,7])}")

    print("\n4. Enter the sequence of coefficients for the polynomial that is the sum of the two polynomials above (3x**3 + 2x - 4) * (2x + 7):")
    print((lab.Polynomial([3,0,2,4]) * lab.Polynomial([2,7])).getReps())
    print(f"prove: {lab.Polynomial([3,0,2,4]) * lab.Polynomial([2,7])}")

    print("\n5. Enter the sequence of coefficients for the polynomial that is the sum of the two polynomials above (3x**3 + 2x - 4) + (2x):")
    print((lab.Polynomial([3,0,2,4]) * lab.Polynomial([2,0])).getReps())
    print(f"prove: {lab.Polynomial([3,0,2,4]) * lab.Polynomial([2,0])}")

    print("\n6. Enter the sequence of coefficients for the polynomial that is the sum of the two polynomials above (3x**3 + 2x - 4) + (7):")
    print((lab.Polynomial([3,0,2,4]) * lab.Polynomial([7])).getReps())
    print(f"prove: {lab.Polynomial([3,0,2,4]) * lab.Polynomial([7])}")

    print("\n Enter the sequence of coefficients for the polynomial that is the sum of the previous two resulting polynomials. ")
    print((lab.Polynomial([3,0,2,4]) * lab.Polynomial([2,0]) + lab.Polynomial([3,0,2,4]) * lab.Polynomial([7])).getReps())
    print(f"prove: {(lab.Polynomial([3,0,2,4]) * lab.Polynomial([2,0])) + (lab.Polynomial([3,0,2,4]) * lab.Polynomial([7]))}")


if __name__ == '__main__':
    part1()