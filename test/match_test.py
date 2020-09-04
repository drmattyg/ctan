import unittest
from match import *

class TestMatch(unittest.TestCase):
    def test_matcher(self):
        # mentees: a, b, c, d
        # mentors: A, B
        mepref = {'a': [('A', 3), ('B', 2)],
                  'b': [('A', 1)],
                  'c': [('A', 3), ('B', 1)],
                  'd': [('A', 1), ('B', 2)]}
        capacity = {'A': 2, 'B': 1, }
        dei = {'a': 1, 'b': 2, 'c': 3, 'd': 1}

        m = Matcher(mepref, capacity, dei)


if __name__ == '__main__':
    unittest.main()
