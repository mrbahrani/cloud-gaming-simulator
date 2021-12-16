class ProcessingElement:
    def __init__(self, identity=0, mips=1000):
        self.id = identity
        self.mips = mips
        self.occupied = 0

    def get_utilization(self):
        return self.occupied / self.mips

