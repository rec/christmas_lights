import numpy as np
import copy
from bibliopixel.animation import BaseAnimation


class Streamer(BaseAnimation):
    def __init__(self, *args, get_color=None, speed=1, **kwds):
        super().__init__(*args, **kwds)
        self.speed = speed
        self.get_color = get_color or self.get_color

        self.cache = np.empty((1 + len(self.color_list), 3))
        for i, c in enumerate(self.cache):
            self.cache[i] = self.get_color(i)
        self.cache_offset = 0

    def step(self, amt=1):
        pixels = self.speed * self.cur_step / self.runner.fps
        needed = int(pixels) - self.cache_offset

        if needed:
            np.roll(self.cache, -needed, axis=0)
            start = len(self.cache) - needed

            for i in range(needed):
                self.cache[start + i] = self.get_color(i + self.cache_offset)

            self.cache_offset = int(pixels)

        cl = self.color_list
        r = pixels % 1
        if r:
            cl[:] = (1 - r) * self.cache[:-1] + r * self.cache[1:]
        else:
            cl[:] = self.cache[:-1]


    def get_color(self, i):
        raise NotImplementedError


# https://wiki.python.org/moin/BitManipulation
def bitLenCount(int_type):
    count = 0
    while (int_type):
        count += (int_type & 1)
        int_type >>= 1
    return count


class Alternate(Streamer):
    def get_color(self, i):
        return (0, 0, 0) if i % 5 else (255, 255, 255)


class BitCounter(Streamer):
    def __init__(self, *args, offsets=(0, 1, 2), **kwds):
        assert len(offsets) == 3
        self.offsets = offsets

        super().__init__(*args, **kwds)

    def get_color(self, i):
        return [bitLenCount(i + o) for o in self.offsets]
