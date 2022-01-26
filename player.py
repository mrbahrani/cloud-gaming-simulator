from random import randint

from packet import Packet
from task import Task
from timegenerator import TimeGenerator


class Player:
    def __init__(self, identity,  time_gen: TimeGenerator, reach_out_time: float = 1.0):
        self.id: str = identity
        self.packet_time_generator: TimeGenerator = time_gen
        self.nuance = randint(0, 100)
        self.last_packet_id = self.nuance - 1
        self.reach_out_time = reach_out_time
        self.delay_tolerance_limit = 62.5

    def create_next_packet(self, game):
        self.last_packet_id += 1
        s = self.create_packet_size()
        packet = Packet(self.last_packet_id, self, game, s, self.delay_tolerance_limit, self.create_task(), 'res')
        return packet

    def create_task(self):
        return Task(num_obj=randint(1,4))

    def create_packet_size(self):
        return 20
