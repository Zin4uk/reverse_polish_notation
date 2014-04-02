import unittest
from type_mod import operator, function


class type_mod_tester(unittest.TestCase):

    def setUp(self):  # called for each test - test fixture
        self.add = operator('+', 0, (lambda y, x: x + y))
        self.sub = operator('-', 0, (lambda y, x: x - y))
        self.mul = operator('*', 1, (lambda y, x: x * y))
        self.div = operator('/', 1, (lambda y, x: x / y))
        self.powr = operator('^', 2, (lambda y, x: pow(x, y)), pos='right')

        self.pluss = function('pluss', (lambda y, x, z: x + y + z))
        self.pi = function('pi', (lambda: 3.14))

    def test_operators_equal(self):
        self.assertTrue(self.add == self.sub)
        self.assertTrue(self.sub < self.mul)
        self.assertTrue(self.mul == self.div)
        self.assertTrue(self.add < self.powr)
        self.assertTrue(self.mul < self.powr)
        self.assertTrue(self.powr == self.powr)
        self.assertTrue(self.powr <= self.powr)

    def test_calc_operations(self):
        cases = [
            [5, 5],
            [15000, 9999],
            [-1111, -888],
            [1, 0],
            [1, -1],
            [-9999, -9999],
        ]

        for case in cases:
            self.assertEqual(self.add(*case), sum(case))
            self.assertEqual(self.sub(*case), case[1] - case[0])
            self.assertEqual(self.mul(*case), case[1] * case[0])
            self.assertEqual(self.div(*case), case[1] / case[0])
            self.assertEqual(self.powr(*case), pow(case[1], case[0]))

    def test_call_func_calc(self):
        self.assertEqual(self.pluss([1, 2, 3]), 6)
        self.assertEqual(self.pluss([1100000, 2, 3]), 1100005)
        self.assertEqual(self.pi([]), 3.14)
        self.assertEqual(self.pi(), 3.14)

    def test_call_func_with_low_stack(self):
        with self.assertRaises(IndexError):
            self.pluss([1, 2])

    def test_call_func_with_bigger_stack(self):
        self.assertEqual(self.pluss([1, 2, 3, 4]), 2 + 3 + 4)
        self.assertEqual(self.pluss(list(range(104))), 101 + 102 + 103)
        self.assertEqual(self.pi([1, 2, 3, 4]), 3.14)


if __name__ == '__main__':
    unittest.main()
