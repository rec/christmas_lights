from bibliopixel import layout


class WallLayout(layout.Strip):

    def set_pixel_positions(self, pp):
        super().set_pixel_positions(POSITIONS)
        print('*** set_pixel_positions')
        print(pp)
        print()


OLD_POSITIONS = [
    [0, 0, 0],
    [1, 0, 0],
    [2, 0, 0],
    [3, 0, 0],
    [4, 0, 0],
    [5, 0, 0],
    [6, 0, 0],
    [7, 0, 0],
    [8, 0, 0],
    [9, 0, 0],
    [10, 0, 0],
    [11, 0, 0],
    [12, 0, 0],
    [13, 0, 0]]


POSITIONS = [
    [0, 3, 0],
    [0, 2, 0],
    [0, 1, 0],
    [0, 0, 0],
    [1, 4, 0],
    [1, 3, 0],
    [1, 2, 0],
    [1, 1, 0],
    [1, 0, 0],
    [2, 3, 0],
    [2, 2, 0],
    [2, 1, 0],
    [2, 0, 0]]
