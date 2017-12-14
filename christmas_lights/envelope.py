import functools
import numpy as np


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
    'linear': linear,

    'square': power_maker(2),
    'cube': power_maker(3),
    'sqrt': power_maker(0.5),

    'gamma2': gamma_maker(2),
    'gamma2.5': gamma_maker(2),
    'gamma10': gamma_maker(10),
}
