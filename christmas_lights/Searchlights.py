from . light import Light

import math
from bibliopixel.animation import BaseStripAnim
from bibliopixel import util
from bibliopixel.util.colors import wheel

DEFAULT_SPEED = 1 / 3


class Searchlights(BaseStripAnim):
    def __init__(self, layout, *, count=3, speeds=DEFAULT_SPEED, bounds=None,
                 positions=None, colors=None, widths=None, shapes='linear',
                 background_color=util.colors.Black, **kwds):
        """
        Arguments

        speeds -- speed to move the light across the entire string
        """
        super().__init__(layout, **kwds)
        self.background_color = background_color
        self.count = count

        if not positions:
            if count == 1:
                positions = [1 / 2]
            else:
                positions = [i / (count) for i in range(count)]

        if not widths:
            widths = [1 / (2 * count)]

        if not isinstance(speeds, (list, tuple)):
            speeds = [speeds]
        if not isinstance(widths, (list, tuple)):
            widths = [widths]
        if not isinstance(shapes, (list, tuple)):
            shapes = [shapes]
        if not isinstance(positions, (list, tuple)):
            positions = [positions]

        if not colors:
            if count == 1:
                colors = [util.colors.Yellow]
            else:
                colors = [wheel.wheel_helper(p, 1, 0) for p in positions]
                colors = [(2 * r, 2 * g, 2 * b) for r, g, b in colors]

        n = len(self.color_list)
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
