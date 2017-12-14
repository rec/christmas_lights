import random, numbers, numpy as np
from . import envelope, Sprite1d


class Light(Sprite1d.Sprite1d):
    def __init__(self, color_list, speed, bound, position, color, width, shape):
        def number(x):
            if isinstance(x, numbers.Number):
                return x
            if not x.startswith('rand('):
                raise ValueError("Don't understand number '%s'" % x)
            lo, hi = (float(i) for i in x[5:-1].split(','))
            return random.uniform(lo, hi)

        speed = number(speed)
        position = number(position)

        curve = envelope.CURVES[shape]
        radius = max(1, round(number(width) * len(color_list) / 2))

        fade_in = curve(0, 1, radius)
        fade_out = curve(1, 0, radius)

        env = np.concatenate([fade_in, fade_out])
        icon = np.outer(env, color)

        super().__init__(icon, color_list, speed, bound, position)

    def step(self, amt):
        self.render()
        self.move(amt)
        self.bounce()
