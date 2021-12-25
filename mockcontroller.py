from typing import List

from controller import Controller
from game import Game
from topologygraph import TopologyGraph


def group_by_game(paths_by_host, games: List[Game]):
    result = dict()
    for game in games:
        result[game] = []
        for host in game.hosts:
            if game in result:
                result[game] += paths_by_host[host]
            else:
                result[game] = paths_by_host[host]
    return result


class MockController(Controller):
    def preprocess(self):
        pass

    def __init__(self):
        self.paths_by_game = None

    def initialize(self, tg: TopologyGraph, games: List[Game]):
        paths_by_host = tg.get_path_dict()
        self.paths_by_game = group_by_game(paths_by_host, games)

    def set_path(self, packet):
        packet.set_path(self.paths_by_game[packet.game][0])

