from bibliopixel.animation import BaseStripAnim
import numpy as np
from bibliopixel import util


class Fade(BaseStripAnim):
    def __init__(self, layout, *, range=(255, 0), mask=(1, 1, 1), **kwds):
        super().__init__(layout, preclear=False, **kwds)
        env = np.linspace(range[0], range[1], len(self.color_list),
                          endpoint=False, dtype=int)
        self.color_list[:] = np.outer(env, mask)

        print(self.color_list)

    def step(self, amt=1):
        pass
