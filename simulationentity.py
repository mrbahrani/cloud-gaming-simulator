from abc import ABC


class SimulationEntity(ABC):
    def __init__(self):
        self.id = 0
        self.paths = []

    def parse_message(self, msg):
        raise NotImplementedError
