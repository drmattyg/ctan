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
        self.assertSetEqual(set(m.unmatched_me().keys()), set(m.mematch.keys()))
        self.assertListEqual(m.mematch['d'].prefs, [('B', 2), ('A', 1)])
        self.assertEqual(m.mematch['d'].next_proposal(m.mrmatch), 'B')
        self.assertTrue(m.can_match())
        m.solve()
        self.assertSetEqual(m.unmatched_mentees, {'a'})
        self.assertDictEqual(m.solution, {'A': {'c', 'b'}, 'B': {'d'}})

        # raise a's preference for B above d's
        mepref['a'][1] = ('B', 3)
        m2 = Matcher(mepref, capacity, dei)
        m2.solve()
        self.assertSetEqual(m2.unmatched_mentees, {'d'})
        self.assertDictEqual(m2.solution, {'A': {'c', 'b'}, 'B': {'a'}})

if __name__ == '__main__':
    unittest.main()
