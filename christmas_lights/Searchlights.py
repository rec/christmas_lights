from . light import Light

import math
from bibliopixel.animation import BaseStripAnim
from bibliopixel import util
from bibliopixel.util.colors import wheel

DEFAULT_TIME = 3


class Searchlights(BaseStripAnim):
    def __init__(self, layout, *, count=3, times=DEFAULT_TIME, bounds=None,
                 positions=None, colors=None, widths=0.15, shapes='linear',
                 background_color=util.colors.Black, **kwds):
        """
        Arguments

        times -- time to move the light across the entire string
        """
        super().__init__(layout, **kwds)
        self.background_color = background_color
        self.count = count

        if not positions:
            if count == 1:
                positions = [1 / 2]
            else:
                positions = [i / (count) for i in range(count)]

        if not isinstance(times, (list, tuple)):
            times = [times]
        if not isinstance(widths, (list, tuple)):
            widths = [widths]
        if not isinstance(shapes, (list, tuple)):
            shapes = [shapes]
        if not isinstance(positions, (list, tuple)):
            positions = [positions]

        print('!!!', positions)
        if not colors:
            if count == 1:
                colors = [util.colors.Yellow]
            else:
                colors = [wheel.wheel_helper(p, 1, 0) for p in positions]

        n = len(self.color_list)
        speeds = [1 / t for t in times]
        bounds = bounds or [(0, 1)]

        arrays = speeds, bounds, positions, colors, widths, shapes

        def make_light(i):
            return Light(self.color_list, *[a[i % len(a)] for a in arrays])

        self.lights = [make_light(i) for i in range(count)]

    def pre_run(self):
        for light in self.lights:
            light.fps = self.runner.fps

    def step(self, amt=1):
        self.color_list[:None] = self.background_color

        for light in self.lights:
            light.step(amt)
