def accumulate(state_count, probabilities):
    assert state_count > 1
    assert len(probabilities) <= state_count
    for i, row in enumerate(probabilities):
        assert all(p >= 0 for p in row)
        total = sum(row)
        yield itertools.accumulate(p / total for p in row)

    for j in range(i + 1, state_count):
        yield [(i + i) / state_count for i in range(state_count)]


class StateMachine:
    def __init__(self, state_count, probabilities, state=0):
        self.probabilities = list(accumulate(state_count, probabilities))
        assert len(self.probabilities) == state_count
        self.state = state

    def next_state(self, variate):
        self.state = bisect_right(self.probabilities[self.state], variate)
        assert self.state < len(self.probabilities)
        return self.state
