"""
This includes the tests for the User Object
"""


import unittest

class SampleTest(unittest.TestCase):
    """
    A sample test to check that TravisCI is working
    """
    def test_2_is_2(self):
        """2 is equal to 2"""
        self.assertEqual(2, 2)


if __name__ == '__main__':
    unittest.main()
    