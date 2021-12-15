class IDGenerator:
    def __init__(self):
        self.gap = 7
        self.current = -6

    def getNextId(self):
        self.current += self.gap
        return self.current
