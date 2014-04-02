import re
from decimal import Decimal
from type_mod import operator, function


class reverse_polish_notation:

    """
    parse expression, converts it to reverse polish notation (RPN)
    and calculates RPN
    """

    def __init__(self, all_ops, all_funcs):
        """
        defines basic operators and functions
        """
        self.ops = {op.name: op for op in all_ops}
        self.fun = {f.name: f for f in all_funcs}

    def parse_ex(self, e):
        """
        convert incoming expression string to a list of args
        """
        result = '(' + e + ')'  # add brackets
        # replace unary minus/plus after [-+*/(] with the '(0-number)' string
        result = re.sub(r'(?<=[-+*/(])([+-]\d+)', r'(0\1)', result)
        # replace unary minus/plus before ( with the '0-(' string
        result = re.sub(r'(?<=\()([+-]\()', r'0\1', result)
        # search for all tokens in formated string
        result = re.findall(r'(\w+|\d+|[-()+*/^])', result)

        return result

    def get_rev_pol(self, args):
        """
        convert list of args to RPN
        """
        stack = []
        result = []

        while args:  # While there are input tokens left
            i = args[0]  # Read the next token from input.
            args = args[1:]

            if i.isdigit():  # If the token is a value
                result.append(Decimal(i))  # Push it into the result.
            elif i == '(':
                stack.append(i)  # Push it onto the stack.
            elif i in self.fun.keys():  # If the token is a function
                stack.append(i)  # Push it onto the stack.
            elif i == ')':  # If the token is a '('
                while stack[-1] != '(':
                    result.append(stack.pop())  # Push it into the result.
                stack.pop()  # Remove '('

                # If top token in the stack is a function
                if stack and stack[-1] in self.fun.keys():
                    result.append(stack.pop())
            elif i in self.ops.keys():  # Otherwise, the token is an operator
                while stack:
                    #  if the stack top token is an operator
                    if stack[-1] in self.ops.keys():
                        top = self.ops[stack[-1]]
                        cur = self.ops[i]

                        # It is a priori operator
                        if top.is_left() and cur <= top:
                            result.append(stack.pop())
                        # It is a posteriori operator
                        elif top.is_right() and cur < top:
                            result.append(stack.pop())
                        else:
                            break
                    else:
                        break
                stack.append(i)  # Push i onto the stack.

        while stack:
            # Push the top of the stack to the result.
            result.append(stack.pop())

        return result

    def calc_rev_pol(self, args):
        """
        calculate RPN with stack
        """
        stack = []

        while args:
            i = args[0]
            args = args[1:]

            if i in self.ops.keys():  # if token is an operator
                res = self.ops[i](stack.pop(), stack.pop())
                stack.append(res)
            elif i in self.fun.keys():  # if token is a function
                res = self.fun[i](stack)
                stack.append(res)
            else:
                stack.append(i)

        return stack[0]


if __name__ == '__main__':  # pragma: no cover
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

    pol_nat = reverse_polish_notation(all_ops, all_funcs)

    e = 'pi() * pluss(9, 1, 1) ^ 2 * 9 + 4 / (1 * 2)'
    r = pol_nat.get_rev_pol(pol_nat.parse_ex(e))
    r = pol_nat.calc_rev_pol(r)
    print(r)
