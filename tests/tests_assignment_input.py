import unittest
from profit_maximizer import CaseHandler 

class TestSuite(unittest.TestCase):
    """
    Test of the profit solver on the the example input to see if it terminates
    """

    def test_example_input(self):
        """
        Checks if the programs finishes for the example input
        """
        test_object = CaseHandler("./tests/inputs/input.txt", True) 
        test_object.content_handler()

if __name__ == '__main__':
    unittest.main()