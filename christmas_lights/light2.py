import random, numbers, numpy as np
from . import envelope


class Sprite1d:
    """A one-dimensional sprite with subpixel positioning."""
    def __init__(self, icon, color_list, speed=0, bound=(0, 1), position=0,
                 center=None):
        self.color_list = color_list
        self.icon = icon
        self.speed = speed
        self.bound = bound
        self.position = position
        self.center = int(len(self.icon) / 2) if center is None else center
        self.fps = 0


class Light(Sprite1d):
    def __init__(self, color_list, speed, bound, position, color, width, shape):
        def number(x):
            if isinstance(x, numbers.Number):
                return x
            if not x.startswith('rand('):
                raise ValueError("Don't understand number '%s'" % x)
            lo, hi = (float(i) for i in x[5:-1].split(','))
            return random.uniform(lo, hi)

        self.color = np.array(color, dtype=float)
        self.radius = max(1, round(number(width) * len(color_list) / 2))
        curve = envelope.CURVES[shape]

        fade_in = curve(0, 1, self.radius)
        fade_out = curve(1, 0, self.radius)

        env = np.concatenate([fade_in, fade_out])
        icon = np.outer(env, color)

        super().__init__(
            icon, color_list, number(speed), bound, number(position))

    def _display(self):
        N = len(self.color_list)

        def add(left, right, ratio):
            # print('add', left, right, ratio)
            icon = self.icon

            # Is the searchlight visible?
            if right >= 0 and left < N:
                if left < 0:
                    # It's partly off the left side.
                    icon = icon[-left:]
                    left = 0

                if right >= N:
                    # It's partly off the right side.
                    icon = icon[:N - right - 1]
                    right = N - 1

                self.color_list[left:right] += ratio * icon

        # Handle subpixel positioning.
        whole, fraction = divmod(self.position * N, 1)
        left, right = int(whole) - self.radius, int(whole) + self.radius

        add(left, right, 1 - fraction)
        if fraction:
            add(left + 1, right + 1, fraction)

    def _move(self, amt):
        self.position += amt * self.speed / self.fps
        left, right = self.bound
        if self.position < left and self.speed < 0:
            self.position = left + (left - self.position)
            self.speed = -self.speed
        if self.position >= right and self.speed > 0:
            self.position = right - (self.position - right)
            self.speed = -self.speed

    def step(self, amt):
        self._display()
        self._move(amt)
