import numpy as np
from . import envelope, Sprite1d


class Light(Sprite1d.Sprite1d):
    def __init__(self, color_list, speed, acceleration,
                 bound, position, color, width, shape):
        radius = max(1, round(Sprite1d.to_number(width) * len(color_list) / 2))
        curve = envelope.CURVES[shape]

        fade_in = curve(0, 1, radius)
        fade_out = curve(1, 0, radius)

        env = np.concatenate([fade_in, fade_out])
        icon = np.outer(env, color)
        super().__init__(icon, color_list, speed, acceleration, bound, position)

    def step(self, amt):
        self.display()
        self.move(amt)
        self.bounce()

    def render(self):
        whole, fraction = divmod(self.position * len(self.icon), 1)
        left = int(whole) - self.center
        right = left + len(self.icon)

        self._combine_clipped(left, right, 1 - fraction)
        if fraction:
            self._combine_clipped(left + 1, right + 1, fraction)
