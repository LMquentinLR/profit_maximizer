import unittest
from profit_maximizer import CaseHandler 

class TestSuite(unittest.TestCase):
    """
    Test cases on file handling by the object CaseHandler
    """

    def test_filename(self):
        """
        Checks the check filename method
        """
        cases = [
            (None, False),
            (123, False), 
            ("./test", False), 
            ("./test.py", False), 
            ("./test.txt", True)
            ]
        for case in cases:
            test_object = CaseHandler(case[0], True)
            self.assertEqual(test_object.check_filename(), case[1]) 

    def test_file_exists(self):
        """
        Checks the file exists method
        """
        cases = [
            (None, False),
            ("./test.txt", False),
            ("./tests/inputs/input.txt", True)
        ]
        for case in cases:
            test_object = CaseHandler(case[0], True)
            self.assertEqual(test_object.check_file_exists(), case[1])

    def test_file_non_empty(self):
        """
        Checks the non-empty file method
        """
        cases = [
            (None, False),
            ("./tests/inputs/input.txt", True),
            ("./tests/inputs/empty.txt", False)
        ]
        for case in cases:
            test_object = CaseHandler(case[0], True)
            self.assertEqual(test_object.check_file_nonempty(), case[1])

if __name__ == '__main__':
    unittest.main()