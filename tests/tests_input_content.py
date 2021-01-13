import unittest
from profit_maximizer import CaseHandler 

class TestSuite(unittest.TestCase):
    """
    Test cases on input handling by the CaseHandler object
    """

    def test_line_to_parse(self):
        """
        Checks the line parser method of CaseHandler
        """
        cases = [
            ("6 12 1 3\n", [6, 12, 1, 3]),
            ("6 12 a 3\n", []),
            ("6 10 20\n", [6, 10, 20]),
            ("6 12", []),
            ("6 12 1 3 14\n", []),
            ("\n", []),
            ("", [])
        ]
        test_object = CaseHandler("", True)
        for case in cases:
            self.assertEqual(test_object.line_parser(case[0]), case[1])

    def test_caching(self):
        """
        Checks the data caching method of CaseHandler
        """
        cases = [
            [
                "./tests/inputs/input.txt", 
                True,
                8,
                [6,10,20], 
                [[6,12,1,3],[1,9,1,2],[3,2,1,2],[8,20,5,4],[4,11,7,4],[2,10,9,1]]
            ],
            [
                "./tests/inputs/wrong_input_1.txt",
                True,
                8,
                [6,10,3],
                [[1,9,1,2],[3,2,1,2],[2,10,9,1]]
            ],
            ["./tests/inputs/wrong_input_2.txt", True, 2, [], []],
            ["./tests/inputs/wrong_input_3.txt", True, 8, [], []],
            ["./tests/inputs/end.txt", False, 1, [], []],
            ["./tests/inputs/empty.txt", False, 1, [], []],

        ]
        for case in cases:
            test_object = CaseHandler(case[0], True)
            self.assertEqual(test_object.case_caching(1), (case[1], case[2], case[3], case[4]))

if __name__ == '__main__':
    unittest.main()