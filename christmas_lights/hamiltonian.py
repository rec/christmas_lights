from bibliopixel.project.types import channel_order


def next_hamiltonian(n, a, b, c):
    # There are two special cases where we make an alternate choice:
    #
    #   a, 0, 0 where a is non-zero;  (we decrease a)
    #   a, 0, 1 where a is odd, but less than n - 1; (we increase a)
    #
    # This is how we make it a loop!
    # See https://math.stackexchange.com/a/1159383/127733

    if b == 0:
        if a != 0 and c == 0:
            return a - 1, b, c

        if a % 2 and a < n - 1 and c == 1:
            return a + 1, b, c

    next_c = c + (-1 if (a + b) % 2 else 1)
    if 0 <= next_c < n:
        return a, b, next_c

    next_b = b + (-1 if a % 2 else 1)
    if 0 <= next_b < n:
        return a, next_b, c

    return a + 1, b, c


class HamiltonianCounter:
    def __init__(self, n, order=0, inverted=''):
        assert not (n % 2), 'n must be even'
        assert n > 2, 'n must be > 2'
        self.n = n
        self.scale = 256 / n
        inverted = [i in inverted.lower() for i in 'rgb']
        self.inverters = [self.invert if i else lambda x: x for i in inverted]
        self.order = channel_order.make(order)
        self._color = 0, 0, 0

    def invert(self, x):
        return self.n - x - 1

    def next(self):
        color = [self._color[o] for o in self.order]
        color = [self.scale * inv(c) for inv, c in zip(self.inverters, color)]

        self._color = next_hamiltonian(self.n, *self._color)
        return color


if __name__ == '__main__':
    import sys

    n = int((sys.argv + ['4'])[1])
    counter = HamiltonianCounter(n, inverted='rb')

    i = 0
    r, g, b = counter.next()
    while not i or r or g or b:
        print('%04x:' % i, r, g, b)
        i += 1
        r, g, b = counter.next()
