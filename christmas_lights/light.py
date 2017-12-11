import numpy as np


class Light:
    def __init__(self, color_list, speed, bound, position, color, width, shape):
        # print('__init__', speed, bound, position, color, width, shape)
        self.color_list = color_list
        self.speed = speed
        self.bound = bound
        self.position = position
        self.color = np.array(color, dtype=float)
        self.shape = shape
        self.fps = 0
        self.radius = round(width * len(color_list) / 2)

        fade_in = np.linspace(0, 1, self.radius, endpoint=False, dtype=float)
        fade_out = np.linspace(1, 0, self.radius, endpoint=False, dtype=float)

        envelope = np.concatenate([fade_in, fade_out])
        self.pixels = np.outer(envelope, color)

    def _display(self):
        N = len(self.color_list)

        def add(left, right, ratio):
            pixels = self.pixels

            # Is the searchlight visible?
            if right >= 0 and left < N:
                if left < 0:
                    # It's partly off the left side.
                    pixels = pixels[-left:]
                    left = 0

                if right >= N:
                    # It's partly off the right side.
                    pixels = pixels[:N - right - 1]
                    right = N - 1

                # print('???', left, right)
                self.color_list[left:right] += ratio * pixels

        # Handle subpixel positioning.
        whole, fraction = divmod(self.position * N, 1)
        left, right = int(whole) - self.radius, int(whole) + self.radius

        # print('light!!!', self.position, N, whole, fraction, left, right)

        add(left, right, 1 - fraction)
        if fraction:
            add(left + 1, right + 1, fraction)

    def _move(self, amt):
        # print('speeed!!!', self.speed, self.fps)
        self.position += amt * self.speed / self.fps
        left, right = self.bound
        if self.position < left or self.position >= right:
            # Reverse!
            self.speed = -self.speed

    def step(self, amt):
        self._display()
        self._move(amt)
