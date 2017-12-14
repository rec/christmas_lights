import functools
import numpy as np


def constant_maker(c):
    def f(begin, end, count):
        result = np.empty(count)
        result.fill(c)
        return result

    return f


def linear(begin, end, count):
    return np.linspace(begin, end, count, endpoint=False, dtype=float)


def power_maker(base=2):
    def f(begin, end, count):
        return linear(begin, end, count) ** base

    return f


def gamma_maker(base=2.5):
    def f(begin, end, count):
        return base ** linear(begin, end, count)

    return f


CURVES = {
    'zero': constant_maker(0),
    'one': constant_maker(1),
    'half': constant_maker(1 / 2),

    'linear': linear,

    'square': power_maker(2),
    'cube': power_maker(3),
    'six': power_maker(6),
    'sqrt': power_maker(0.5),

    'gamma0.5': gamma_maker(0.5),
    'gamma2': gamma_maker(2),
    'gamma2.5': gamma_maker(2),
    'gamma10': gamma_maker(10),
}
