from functools import reduce

import operator

def pprod(iterable, start = 1):
    return reduce(operator.mul, iterable, start)

def ssum(iterable, start = 0):
    return sum(iterable, start)

def ffact(num):
    return pprod([i + 1 for i in range(num)])
