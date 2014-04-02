import inspect


class operator:

    """
    basic operator class
    """

    def __init__(self, name, priority, func, pos='left'):
        self.name = name
        self.priority = priority
        self.pos = pos
        self.func = func

    def is_left(self):
        # is a priori operator
        return self.pos.lower() == 'left'

    def is_right(self):
        # is a posteriori operator
        return self.pos.lower() == 'right'

    def __gt__(self, other):
        return self.priority > other.priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __ge__(self, other):
        return self.priority >= other.priority

    def __le__(self, other):
        return self.priority <= other.priority

    def __eq__(self, other):
        return self.priority == other.priority

    def __call__(self, *args, **kargs):
        return self.func(*args, **kargs)


class function:

    """
    basic function class
    """

    def __init__(self, name, func):
        self.name = name
        self.func = func

    def __call__(self, stack=[]):
        # calculates the number of params in lambda expression
        args_count_left \
            = len(inspect.getargspec(self.func).args)

        args = []
        while args_count_left:
            #  pops values from stack to args
            args_count_left -= 1
            args.append(stack.pop())

        return self.func(*args)
