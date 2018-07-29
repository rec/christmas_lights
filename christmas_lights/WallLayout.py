from bibliopixel import layout


SIZE = 10

P0 = [[0, 79-i, 0] for i in range(80)]
P1 = [[1, 75-i, 0] for i in range(100)]
P2 = [[2, 79-i, 0] for i in range(80)]

POSITIONS = [[SIZE * i for i in p] for p in (P0 + P1 + P2)]


class WallLayout(layout.Strip):
    def set_pixel_positions(self, pp):
        super().set_pixel_positions(POSITIONS)
