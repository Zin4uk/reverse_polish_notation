import unittest
from reverse_polish_notation import reverse_polish_notation
from type_mod import operator, function
from decimal import Decimal


class reverse_pol_notation_tester(unittest.TestCase):

    def setUp(self):  # called for each test - test fixture
        all_ops = [
            operator('+', 0, (lambda y, x: x + y)),
            operator('-', 0, (lambda y, x: x - y)),
            operator('*', 1, (lambda y, x: x * y)),
            operator('/', 1, (lambda y, x: x / y)),
            operator('^', 2, (lambda y, x: pow(x, y)), pos='right'),
        ]

        all_funcs = [
            function('pluss', (lambda y, x, z: x + y + z)),
            function('pi', (lambda: Decimal(3.14))),
        ]

        self.subj = reverse_polish_notation(all_ops, all_funcs)

        self.cases = [
            ['0-((-8/(-2))+123)-111', '0 0 8 - 0 2 - / 123 + - 111 -', -238],
            ['1-(999-(-888-(-777-(-666-(-555-(-123456789+(0-(0-'
             + '(-8/-2)+123)-111)-0)-0)+999)/1)*1)+333)',
             '1 999 0 888 - 0 777 - 0 666 - 0 555 - 0 123456789 - 0 0 0 8'
             + ' - 0 2 - / - 123 + - 111 - + 0 - - 0 - - 999 + 1 / - 1 *'
             + ' - - 333 + -', -123457573],
            ['-(-(-(-(-(-(-(-(-(-8/-2)))))))))',
             '0 0 0 0 0 0 0 0 0 0 8 - 0 2 - / - - - - - - - - -', -4],
            ['-1', '0 1 -', -1]
        ]

    def test_exp_parse(self):
        eq = [
            ['(', '0', '-', '(', '(', '(', '0', '-', '8', ')', '/', '(', '(',
             '0', '-', '2', ')', ')', ')', '+',
             '123', ')', '-', '111', ')'],
            ['(', '1', '-', '(', '999', '-', '(', '(', '0', '-', '888', ')',
             '-', '(', '(', '0', '-', '777', ')', '-', '(', '(', '0', '-',
             '666', ')', '-', '(', '(', '0', '-', '555', ')', '-',
             '(', '(', '0', '-', '123456789', ')', '+',
             '(', '0', '-', '(', '0', '-', '(', '(', '0', '-', '8', ')', '/',
             '(', '0', '-', '2', ')', ')', '+', '123', ')', '-', '111', ')',
             '-', '0', ')', '-', '0', ')', '+', '999', ')', '/', '1', ')',
             '*', '1', ')', '+', '333', ')', ')'],
            ['(', '0', '-', '(', '0', '-', '(', '0', '-', '(', '0', '-', '(',
             '0', '-', '(', '0', '-', '(', '0', '-', '(', '0', '-', '(', '0',
             '-', '(', '(', '0', '-', '8', ')', '/', '(', '0', '-', '2', ')',
             ')', ')', ')', ')', ')', ')', ')', ')', ')', ')'],
            ['(', '(', '0', '-', '1', ')', ')'],
        ]

        for i, case in enumerate(self.cases):
            self.assertListEqual(self.subj.parse_ex(case[0]), eq[i])

    # @unittest.skip("wip")
    def test_get_rev_pol(self):
        for case in self.cases:
            exp = self.subj.parse_ex(case[0])
            self.assertEqual(
                ' '.join(map(str, self.subj.get_rev_pol(exp))), case[1])

    # @unittest.skip("wip")
    def test_pol_not_calc(self):
        for case in self.cases:
            stack = [
                float(t) if t.isdigit() else t for t in case[1].split(' ')]
            self.assertEqual(self.subj.calc_rev_pol(stack), case[2])

    def test_calc_with_func(self):
        ex = 'pi() * pluss(9, 1, 1) ^ 2 * 9 + 4 / (1 * 2)'
        r = self.subj.get_rev_pol(self.subj.parse_ex(ex))
        r = self.subj.calc_rev_pol(r)
        self.assertEqual(r, Decimal('3421.460000000000135411681867'))

if __name__ == '__main__':
    unittest.main()
