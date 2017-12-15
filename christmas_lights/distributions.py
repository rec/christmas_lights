import math, random


# http://preshing.com/20111007/how-to-generate-random-timings-for-a-poisson-process/
def poisson(rate=1):
    return lambda: -math.log(1.0 - random.random()) / rate


def linear(begin=0, end=1):
    return lambda: random.uniform(begin, end)


def _make(function, inverse):
    def distribution(begin, end):
        b, e = function(begin), function(end)
        return lambda: inverse(random.uniform(b, e))

    return distribution


log = make(math.log, math.exp)
exp = make(math.exp, math.log)
sqr = make(lambda x: x * x, math.sqrt)
sqrt = make(math.sqrt, lambda x: x * x)
