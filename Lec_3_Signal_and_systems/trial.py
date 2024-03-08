"""  
    Special file to test the import statement
"""

import os, sys
# setup the path
current_path = os.path.dirname(__file__)
package_path = os.path.normpath(current_path + '/../Lec_2_State_Machine')

sys.path.append(package_path)

# import all packages needed:
from state_machine import Accumulator

def test_run():
    acc = Accumulator(10)
    test_res = acc.transduce([1,2,3,4,5])
    print(f"test result: {test_res}")

if __name__ == '__main__':
    test_run()