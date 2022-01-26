from typing import List

import numpy as np

from distributanmaker import DistributionMaker
from event import Event
from eventcodes import EventCodes
from player import Player


class Game:
    def __init__(self, identity, host_list, player_list, delay_tolerance=62.5):
        self.id = identity
        self.hosts = host_list
        self.players: List[Player] = player_list
        self.delay_tolerance = delay_tolerance
        for p in self.players:
            p.delay_tolerance_limit = self.delay_tolerance

    def generate_events(self, total_time):
        events = []
        for p in self.players:
            # d = DistributionMaker()
            # d.get_address("ds.txt")
            t = 0
            next_interval = np.random.normal(62.5, 5)
            while t < total_time:
                packet = p.create_next_packet(self)
                packet.start = t
                e = Event(EventCodes.PACKET_IN_NETWORK, t, t + next_interval, packet)
                events.append(e)
                t += next_interval
        return events
