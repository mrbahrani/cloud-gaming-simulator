from typing import List

from numpy.random import randint

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
        result[game].sort(key=lambda x: len(x))
    return result

class TurnBasedController(Controller):
    def get_feedback(self, packet):
        pass

    def preprocess(self):
        pass

    def __init__(self, games):
        self.games = games
        self.paths_by_game = None
        self.order_by_game = dict()

    def initialize(self, tg: TopologyGraph):
        paths_by_host = tg.get_path_dict()
        self.paths_by_game = group_by_game(paths_by_host, self.games)
        for i in self.paths_by_game:
            self.order_by_game[i] = randint(0, len(self.paths_by_game[i]))

    def set_path(self, packet):
        order = self.order_by_game[packet.game] % len(self.paths_by_game[packet.game])
        self.order_by_game[packet.game] += 1
        p1 = self.paths_by_game[packet.game][order]
        p2 = self.paths_by_game[packet.game][order][-2::-1]
        packet.set_path(p1+p2)

