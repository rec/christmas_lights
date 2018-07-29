import numpy as np
from bibliopixel import animation

# https://stackoverflow.com/a/10411108/43839
binary_to_sting = '{0:08b}'.format

GREYCODE = tuple(n ^ (n // 2) for n in range(256))

def array(x):
    return np.array(x, dtype='float')


def fill_with_greycode(color_list, offsets):
    assert len(offsets) == 3
    for i in range(len(color_list)):
        for j, o in enumerate(offsets):
            n = int((i + o) % 256)
            color_list[i][j] = n ^ (n // 2)


class GreyCode(animation.Animation):
    def __init__(self, *args, offsets=None, speeds=None, **kwds):
        super().__init__(*args, **kwds)
        self.offsets = array(offsets or [0, 0, 0])
        self.speeds = array(speeds or [0, 0, 0])
        self._elapsed = array([0, 0, 0])

    def step(self, amt=1):
        fill_with_greycode(self.color_list, self.offsets + self._elapsed)
        self._elapsed += self.speeds
