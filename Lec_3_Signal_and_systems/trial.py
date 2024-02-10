"""  
    Special file to test the import statement
"""

import state_machine as sm

def test_run():
    acc = sm.Accumulator()
    test_res = acc.transduce([1,2,3,4,5])
    print(f"test result: {test_res}")

if __name__ == '__main__':
    test_run()