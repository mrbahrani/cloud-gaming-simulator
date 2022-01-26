import math
from queue import Queue

from simulationentity import SimulationEntity


class Switch(SimulationEntity):
    def parse_message(self, msg):
        pass

    def __init__(self, identity=0, max_size=10, sending_time=0.01):
        super().__init__()
        self.id = identity
        self.queue_size = 0
        self.packet_queue = Queue()
        self.max_size = max_size
        self.sending_packet_time = sending_time

    def receive(self, packet):
        self.queue_size += 1

    def send(self):
        self.queue_size -= 1
