from timegenerator import TimeGenerator


class UniformTimeGenerator(TimeGenerator):
    def __init__(self, s, e, g):
        self.start = s
        self.end = e
        self.gap = g
        self.current = s - g

    def get_next_time(self):
        self.current += self.gap
        if self.current < self.end:
            return self.current
        return -1
