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
            ("./tests/inputs/first_case.txt", [44])
        ]
        for case in cases:
            test_object = CaseHandler(case[0], True) 
            self.assertEqual(test_object.content_handler(), case[1])

if __name__ == '__main__':
    unittest.main()