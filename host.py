import math

from simulationentity import SimulationEntity


class Host(SimulationEntity):
    def parse_message(self, msg):
        pass

    def __init__(self, identity=0, ram=math.inf, processing_elements={}):
        super().__init__()
        self.id = identity
        self.ram = ram
        self.pes = processing_elements
