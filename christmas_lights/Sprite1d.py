class Sprite1d:
    """A one-dimensional sprite with subpixel positioning."""
    def __init__(self, icon, color_list, speed=0, acceleration=0, bound=(0, 1),
                 position=0, center=None):
        self.color_list = color_list
        if hasattr(color_list, 'dtype'):
            self._combine = self._combine_numpy

        self.icon = icon
        self.speed = speed
        self.acceleration = acceleration
        self.bound = bound
        self.position = position
        self.center = int(len(self.icon) / 2) if center is None else center
        self.fps = 0

    def display(self):
        # Handle subpixel positioning.
        whole, fraction = divmod(self.position * len(self.color_list), 1)
        left = int(whole) - self.center
        right = left + len(self.icon)

        self._add(left, right, 1 - fraction)
        if fraction:
            self._add(left + 1, right + 1, fraction)

    def move(self, amt):
        self.position += amt * (self.speed + self.acceleration / 2) / self.fps
        self.speed += self.acceleration

    def bounce(self):
        left, right = self.bound
        if self.position < left and self.speed < 0:
            self.position = left + (left - self.position)
            self.speed = -self.speed
        if self.position >= right and self.speed > 0:
            self.position = right - (self.position - right)
            self.speed = -self.speed

    def _combine_numpy(self, left, right, ratio, pixels):
        self.color_list[left:right] += ratio * pixels

    def _combine(self, left, right, ratio, pixels):
        for i in range(left, right):
            color = self.color_list[i]
            pixel = pixels[i - left]
            color = tuple(c + ratio * p for c, p in zip(color, pixel))

    def _add(self, left, right, ratio):
        pixels = self.icon

        # Is the sprite visible?
        if right < 0 or left >= len(self.color_list):
            return

        if left < 0:
            # It's partly off the left side.
            pixels = pixels[-left:]
            left = 0

        if right >= len(self.color_list):
            # It's partly off the right side.
            pixels = pixels[:len(self.color_list) - right - 1]
            right = len(self.color_list) - 1

        self._combine(left, right, ratio, pixels)
