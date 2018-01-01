import numpy, random
from bibliopixel.animation import BaseStripAnim, BaseAnimation
from bibliopixel.colors import conversions
from bibliopixel import util
from . Searchlights import Searchlights
from . import distributions

PROJECT = {
    'layout': {
        'simpixel': 'strip',
        'num': 160,
    },
    'layout': 'strip',
    'animation': {}
}


class Fill(BaseAnimation):
    def __init__(self, layout, *, color, **kwds):
        super().__init__(layout, preclear=False, **kwds)
        self.color = color

    def step(self, amt=1):
        self.color_list[:None] = self.color


class ExponentialFade(BaseAnimation):
    def __init__(self, layout, *, ratio=0.98, color=None, **kwds):
        super().__init__(layout, preclear=False, **kwds)
        self.ratio = ratio
        self.color = color and numpy.array(color, dtype='float') * (1 - ratio)

    def step(self, amt=1):
        cl = self.color_list
        cl *= self.ratio
        if self.color is not None:
             cl[:None] += self.color


class Randomize(BaseAnimation):
    def __init__(self, layout, *, repeats=0, **kwds):
        super().__init__(layout, preclear=False, **kwds)
        self.repeats = repeats
        self.count = 0

    def step(self, amt=1):
        cl = self.color_list
        cl[:] = numpy.random.rand(*cl.shape) * 255


class Sort(BaseAnimation):
    def __init__(self, layout, *, ascending=True, **kwds):
        super().__init__(layout, preclear=False, **kwds)
        self.direction = 1 if ascending else -1

    def step(self, amt=1):
        for i, color in enumerate(self.color_list):
            color = [round(c) for c in color]
            if i and conversions.color_cmp(prev, color) * self.direction > 0:
                self.color_list[i - 1:i] = self.color_list[i:i - 1:-1]
                return

            prev = color


class Rain(BaseAnimation):
    def __init__(self, layout, *, colors=None, rate=10, **kwds):
        self.colors = colors or (
            (0, 0, 0), (0, 0, 0),
            (0, 0, 0), (0, 0, 0),
            (70, 70, 70), (35, 35, 35),
            (80, 20, 20), (45, 5, 5),
            (20, 80, 20), (5, 45, 5),
        )
        self.distrib = distributions.poisson(rate)
        self.wait = 0
        super().__init__(layout)

    def step(self, amt=1):
        if self.wait > 0:
            self.wait -= 1
        else:
            index = random.randrange(len(self.color_list))
            self.color_list[index] = random.choice(self.colors)
            self.wait = self.distrib() * self.runner.fps
