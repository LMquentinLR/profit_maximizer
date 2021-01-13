from contextlib import contextmanager
from profit_maximizer import CaseHandler 

import random as rd
import time
import unittest

@contextmanager
def timeit_context(name):
    """
    Timer function
    """
    startTime = time.time()
    yield
    elapsedTime = time.time() - startTime
    print(f"[{name}] finished in {int(elapsedTime * 1000)} ms")

class TestSuite(unittest.TestCase):
    """
    Class of test cases for time complexity/runtime
    """

    def generate_case(self, magnitude_order_machines):
        """
        Generates a test case in a .txt file with:
            - 10**<magnitude_order_machines> randomly generated machines
            - cash at hand randomly picked from 1 to 10**9
            - number of restructuring days randomly picked from 1 to 10**9
        inputs:
            <magnitude_order_machines> :: Int - magnitude order of the # of machines to be created
        output:
            <out> :: None
        """
        machine_number = rd.randint(0,10**magnitude_order_machines)
        cash_at_hand = rd.randint(0,10**9)
        restructuring_days = rd.randint(0,10**9)

        with open("./tests/inputs/generated_input.txt", "w+") as f:
            # Writes the context line
            f.write(" ".join(list(map(str, [machine_number, cash_at_hand, restructuring_days, "\n"]))))  
            # Writes <machine_number> randomly generated machines      
            for _ in range(machine_number):
                price = rd.randint(1, 10**9)
                resell = rd.randint(1, price)
                availability = rd.randint(1, restructuring_days)
                profit = rd.randint(1, restructuring_days)
                f.write(" ".join(list(map(str, [availability, price, resell, profit, "\n"]))))
            # Writes the case closing line
            f.write("0 0 0")

    def test_generated_input(self):
        """
        Checks how long the program runs given an order of magnitude up to 2 for the number of machines created
        and maximum number of machine acquisition 3  
        """
        for i in range(1, 4):
            with timeit_context(f"Running solver with max acquisitions of {i} machines"):
                self.generate_case(2)
                test_object = CaseHandler("./tests/inputs/generated_input.txt", True)
                test_object.content_handler(i)

if __name__ == '__main__':
    unittest.main()