"""  
    Problem Wk.3.1.1: Simulating Cascade

Run result for Problem number 1:
Start state: (1, 2)

sm1 input: 3
sm1 state: 1
sm1 output: 1
sm2 input: 1
sm2 state: 2
sm2 output: 2
In: 3 Out: 2 Next State: (3, 1)

sm1 input: 5
sm1 state: 3
sm1 output: 3
sm2 input: 3
sm2 state: 1
sm2 output: 1
In: 5 Out: 1 Next State: (5, 3)

sm1 input: 7
sm1 state: 5
sm1 output: 5
sm2 input: 5
sm2 state: 3
sm2 output: 3
In: 7 Out: 3 Next State: (7, 5)

sm1 input: 9
sm1 state: 7
sm1 output: 7
sm2 input: 7
sm2 state: 5
sm2 output: 5
In: 9 Out: 5 Next State: (9, 7)

Run result for Problem number 2:
Start state: (1, 0)

sm1 input: 3
sm1 state: 1
sm1 output: 1
sm2 input: 1
sm2 state: 0
sm2 output: 4
In: 3 Out: 4 Next State: (3, 4)

sm1 input: 5
sm1 state: 3
sm1 output: 3
sm2 input: 3
sm2 state: 4
sm2 output: 6
In: 5 Out: 6 Next State: (5, 6)

sm1 input: 7
sm1 state: 5
sm1 output: 5
sm2 input: 5
sm2 state: 6
sm2 output: 8
In: 7 Out: 8 Next State: (7, 8)

sm1 input: 9
sm1 state: 7
sm1 output: 7
sm2 input: 7
sm2 state: 8
sm2 output: 10
In: 9 Out: 10 Next State: (9, 10)

"""

import os, sys
# setup the path
current_path = os.path.dirname(__file__)
package_path = os.path.normpath(current_path + '/../Lec_2_State_Machine')

sys.path.append(package_path)

from state_machine import Delay, Increment
from cascade import Cascade

def problem_1():
    sm1 = Delay(1)
    sm2 = Delay(2)
    c = Cascade(sm1, sm2, smVerbose=True)
    c.transduce([3,5,7,9], verbose=True)

def problem_2():
    sm1 = Delay(1)
    sm2 = Increment(3)
    c = Cascade(sm1, sm2, smVerbose=True)
    c.transduce([3,5,7,9], verbose=True)


if __name__ == '__main__':
    print("\nRun result for Problem number 1:")
    problem_1()
    print("\nRun result for Problem number 2:")
    problem_2()