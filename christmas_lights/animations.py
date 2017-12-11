import numpy
from bibliopixel.animation import BaseStripAnim, BaseAnimation
from bibliopixel import colors

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
    def __init__(self, layout, *, ratio, color=None, **kwds):
        super().__init__(layout, preclear=False, **kwds)
        self.ratio = ratio
        self.color = color and numpy.array(color, dtype='float') * (1 - ratio)

    def step(self, amt=1):
        self.color_list *= self.ratio
        if self.color:
             self.color_list[:None] += (1 - self.ratio) * self.color


class Randomize(BaseAnimation):
    def __init__(self, layout, *, repeats=0, **kwds):
        super().__init__(layout, preclear=False, **kwds)
        self.repeats = repeats
        self.count = 0

    def step(self, amt=1):
        self.color_list[:] = numpy.random.rand(colors.shape) * 255


class Sort(BaseAnimation):
    def __init__(self, layout, *, ascending=True, **kwds):
        super().__init__(layout, preclear=False, **kwds)
        self.direction = 1 if ascending else -1

    def step(self, amt=1):
        for i, color in enumerate(self.color_list):
            if i and conversions.color_cmp(prev, color) * self.direction > 0:
                self.color_list[i:i + 1] = self.color_list[i:i + 1:-1]
                return

            prev = color
