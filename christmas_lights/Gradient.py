from bibliopixel import animation
import numpy as np
from bibliopixel import util


class _Gradient(animation.Animation):
    def __init__(self, layout, range=(255, 0), mask=(1, 1, 1), **kwds):
        super().__init__(layout, preclear=False, **kwds)
        self._start, self._stop = range
        self.mask = mask

    def step(self, amt=1):
        self.color_list[:] = np.outer(self.envelope(), self.mask)


class Linear(_Gradient):
    def envelope(self):
        return np.linspace(self._start, self._stop, len(self.color_list),
                           endpoint=False, dtype=float)


class Log(_Gradient):
    def __init__(self, *args, base=10.0, **kwds):
        super().__init__(*args, **kwds)
        self.base = base

    def envelope(self):
        return np.logspace(self._start, self._stop, len(self.color_list),
                           base=self.base, endpoint=False, dtype=float)
