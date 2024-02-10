"""  
    Special file to test the import statement
"""

from state_machine import Accumulator

def test_run():
    acc = Accumulator(10)
    test_res = acc.transduce([1,2,3,4,5])
    print(f"test result: {test_res}")

if __name__ == '__main__':
    test_run()