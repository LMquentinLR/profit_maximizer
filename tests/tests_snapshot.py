import unittest
from profit_maximizer import CaseHandler 

class TestSuite(unittest.TestCase):
    """
    Test of the profit solver on the first case of the example input
    """

    def test_first_case(self):
        """
        Checks if the programs outputs the right profit for case 1 of
        the example input
        """
        cases = [
            "./tests/inputs/snapshot.txt",
        ]
        for case in cases:
            test_object = CaseHandler(case, True) 
            test_object.content_handler()

if __name__ == '__main__':
    unittest.main()