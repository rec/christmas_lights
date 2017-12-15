import number
from bibliopixel.animation import collection



class Markov(collection.Collection):
    def __init__(self, layout, lengths=None, probabilities=None, **kwds):
        super().__init__(layout, **kwds)
