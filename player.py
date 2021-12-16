from random import randint

from packet import Packet
from timegenerator import TimeGenerator


class Player:
    def __init__(self, identity,  time_gen: TimeGenerator, reach_out_time: float = 1.0):
        self.id: str = identity
        self.packet_time_generator: TimeGenerator = time_gen
        self.naunce = randint(0, 100)
        self.last_packet_id = self.naunce - 1
        self.reach_out_time = reach_out_time

    def create_next_packet(self, game):
        self.last_packet_id += 1
        t = self.create_task()
        s = self.create_packet_size()
        packet = Packet(self.last_packet_id, self, game, s, -1, t)
        return packet

    def create_task(self):
        pass

    def create_packet_size(self):
        pass