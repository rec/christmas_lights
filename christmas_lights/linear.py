from bibliopixel.animation import BaseStripAnim


class Linear(BaseStripAnim):
    def step(self, amt=1):
        self.color_list[:] = ((i, i, i) for i in range(250))
