class Bandwidth:
    def __init__(self, downstream=10, upstream=10):
        self.downstream = downstream
        self.upstream = upstream
        self.downstream_occupied = 0
        self.upstream_occupied = 0

    def downstream_utilization(self):
        return self.downstream_occupied / self.downstream

    def upstream_utilization(self):
        return self.upstream_occupied / self.upstream





