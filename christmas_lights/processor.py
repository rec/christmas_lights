import numpy as np
from bibliopixel import wrapper


class Processor(wrapper.Wrapper):
    def __init__(self, *args, operation, **kwds):
        super().__init__(*args, **kwds)
