from state_machine import Delay, Increment, Negation
from cascade import Cascade
from feedback_sm import Feedback

def main()->None:
    """  
    main run platform for 6-01sc
    """
    inputs1 = [3.5, 4, True, 200, 3]
    foo1 = Cascade(Delay(100), Increment(1))
    foo2 = Cascade(Increment(1), Delay(100))
    print(f'\nExercise 4.3:')
    print(f'foo1 = {foo1.transduce(inputs1, verbose=True)}\n')
    print(f'foo2 = {foo2.transduce(inputs1, verbose=True)}')
    
    # exercise 4.5
    """  
    Draw state tables illustrating whether the following machines are differ
    ent, and if so, how:
    m1 = sm.Feedback(sm.Cascade(sm.Delay(1),Increment(1)))
    m2 = sm.Feedback(sm.Cascade(Increment(1), sm.Delay(1)))
    """
    m1 = Feedback(Cascade(Delay(1), Increment(1)))
    m2 = Feedback(Cascade(Increment(1), Delay(1)))
    print(f'\nExercise 4.5:')
    print(f'for m1:')
    print(f'm1 = {m1.run(verbose=True)}')
    print(f'for m2:')
    print(f'm2 = {m2.run(5, verbose=True)}')

if __name__ == '__main__':
    main()
"""  
Exercise 4.3:
Start state: 100
In: 3.5 Out: 100 Next State: 3.5
In: 4 Out: 3.5 Next State: 4
In: True Out: 4 Next State: True
In: 200 Out: True Next State: 200
In: 3 Out: 200 Next State: 3
Start state: 0
In: 100 Out: 101 Next State: 101
In: 3.5 Out: 4.5 Next State: 4.5
In: 4 Out: 5 Next State: 5
In: True Out: None Next State: 5
In: 200 Out: 201 Next State: 201
foo1 = [101, 4.5, 5, None, 201]

Start state: 0
In: 3.5 Out: 4.5 Next State: 4.5
In: 4 Out: 5 Next State: 5
In: True Out: None Next State: 5
In: 200 Out: 201 Next State: 201
In: 3 Out: 4 Next State: 4
Start state: 100
In: 4.5 Out: 100 Next State: 4.5
In: 5 Out: 4.5 Next State: 5
In: None Out: 5 Next State: None
In: 201 Out: None Next State: 201
In: 4 Out: 201 Next State: 4
foo2 = [100, 4.5, 5, None, 201]

Exercise 4.5:
for m1:
Start state: 1
In: None Out: 2 Next State: None
In: None Out: 3 Next State: None
In: None Out: 4 Next State: None
In: None Out: 5 Next State: None
In: None Out: 6 Next State: None
In: None Out: 7 Next State: None
In: None Out: 8 Next State: None
In: None Out: 9 Next State: None
In: None Out: 10 Next State: None
In: None Out: 11 Next State: None
m1 = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
for m2:
Start state: 0
In: None Out: 1 Next State: None
In: None Out: 2 Next State: None
In: None Out: 3 Next State: None
In: None Out: 4 Next State: None
In: None Out: 5 Next State: None
m2 = [1, 2, 3, 4, 5]
"""