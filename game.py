from typing import List

from event import Event
from eventcodes import EventCodes
from player import Player


class Game:
    def __init__(self, identity, host_list, player_list):
        self.id = identity
        self.hosts = host_list
        self.players: List[Player] = player_list

    def generate_events(self, current_time):
        events = []
        for p in self.players:
            # ToDo Different reach-out time for players
            packet = p.create_next_packet(self)
            e = Event(EventCodes.PACKET_IN_NETWORK, current_time, current_time + p.reach_out_time, packet)
            events.append(e)
        return events
