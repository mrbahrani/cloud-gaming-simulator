from packet import Packet
from timegenerator import TimeGenerator


class Player:
    def __init__(self, identity,  time_gen: TimeGenerator):
        self.id: str = identity
        self.packet_time_generator: TimeGenerator = time_gen

    def create_next_packet(self):
        packet = Packet()
        return packet