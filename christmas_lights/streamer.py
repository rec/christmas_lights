import numpy as np
import copy
import random
from bibliopixel.animation import BaseAnimation
from . import hamiltonian


def perturb(c, variance, bounds):
    if not variance:
        return c

    delta = random.uniform(-1, 1) * variance
    out = (c - delta < bounds[0]) if (delta < 0) else (c + delta >= bounds[1])
    return c - delta if out else c + delta


def percent_perturb(c, variance, bounds):
    if not variance:
        return c

    delta = random.uniform(-0.01, 0.01) * variance
    ratio = 1 + delta if delta >= 0 else 1 / (1 - delta)
    product = ratio * c

    out = (product < bounds[0]) if (delta < 0) else (product >= bounds[1])
    return c / delta if out else c * delta


class Streamer(BaseAnimation):
    def __init__(
            self, *args, speed=10, speed_variance=0, pre_fill=False, **kwds):
        super().__init__(*args, **kwds)
        try:
            self.speed_bounds = tuple(speed)
        except:
            self.speed_bounds = speed, speed

        self.speed = self.speed_bounds[0]
        self.speed_variance = speed_variance
        self.pre_fill = pre_fill
        assert not speed_variance or len(speed)
        self.total_pixels = 0

    def pre_run(self):
        if self.pre_fill:
            self.cache = np.empty((1 + len(self.color_list), 3))
            for i, c in enumerate(self.cache):
                self.cache[i] = self.get_color(i)
        else:
            self.cache = np.zeros((1 + len(self.color_list), 3))
        self.cache_offset = 0

    def step(self, amt=1):
        self.total_pixels += self.speed / self.runner.fps
        needed = int(self.total_pixels) - self.cache_offset

        if needed < 0:
            print(
                'went backwards', needed, self.cache_offset, self.total_pixels)
        elif needed > 0:
            start = len(self.cache) - needed
            if start <= 0:
                self.cache_offset -= start
                needed = len(self.cache)
                start = 0
            else:
                self.cache[:-needed] = self.cache[needed:]

            for i in range(needed):
                self.cache[start + i] = self.get_color(self.cache_offset + i)
            self.cache_offset += needed

        cl = self.color_list
        r = self.total_pixels % 1
        cl[:] = (1 - r) * self.cache[:-1] + r * self.cache[1:]
        self.speed = perturb(
            self.speed, self.speed_variance, self.speed_bounds)

    def get_color(self, i):
        raise NotImplementedError


class Alternate(Streamer):
    def get_color(self, i):
        return (0, 0, 0) if i % 4 else (0, 0, 128)


class Counter(Streamer):
    def __init__(self, *args, scale=20, offsets=(0, 1, 2), **kwds):
        super().__init__(*args, **kwds)
        assert len(offsets) == 3
        self.offsets = offsets
        self.scale = scale

    def get_color(self, i):
        return [self.scale * self.count(i + o) for o in self.offsets]

    def count(self, i):
        raise NotImplementedError


class BitCounter(Counter):
    def count(self, i):
        # https://wiki.python.org/moin/BitManipulation
        count = 0
        while i:
            count += (i & 1)
            i >>= 1
        return count


class RightmostCounter(BitCounter):
    def count(self, i):
        return i & -i


class RandomWalk(Streamer):
    def __init__(self, *args,
                 variance=1, bounds=(0, 180), color=None, period=0, **kwds):
        super().__init__(*args, **kwds)

        self.cur_step = 0
        self.variance = variance
        self.next_color = color or [random.randint(*bounds) for i in range(3)]
        self.choices = -1, 1
        self.bounds = bounds

        self.period = period * self.speed

    def get_color(self, i):
        variance = self.variance
        if self.period:
            variance *= (i % self.period) / (self.period - 1)

        def comp(c):
            choice = variance * random.choice(self.choices)
            out = (c < self.bounds[0]) if (choice < 0) else (c >= self.bounds[1])
            return c - choice if out else c + choice

        result = [perturb(c, variance, self.bounds) for c in self.next_color]
        result, self.next_color = self.next_color, result
        return result


class Hamiltonian(Streamer):
    def __init__(self, *args, n=8, order=0, inverted='', **kwds):
        super().__init__(*args, **kwds)
        self.counter = hamiltonian.HamiltonianCounter(n, order, inverted)

    def get_color(self, i):
        return self.counter.next()
