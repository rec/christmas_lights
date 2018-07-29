from bibliopixel import animation
import numpy as np
from bibliopixel import util


class Linear(animation.Animation):
    def __init__(self, layout, *, range=(255, 0), mask=(1, 1, 1), **kwds):
        super().__init__(layout, preclear=False, **kwds)
        env = np.linspace(range[0], range[1], len(self.color_list),
                          endpoint=False, dtype=int)
        self.gradient = np.outer(env, mask)

    def step(self, amt=1):
        self.color_list = self.gradient
