from typing import List

from event import Event
from player import Player


class Game:
    def __init__(self, identity, host_list, player_list):
        self.id = identity
        self.hosts = host_list
        self.players: List[Player] = player_list

    def generate_events(self):
        events = []
        for p in self.players:
            packet = p.create_next_packet()
            e = Event()
            events.append(e)
        return events
