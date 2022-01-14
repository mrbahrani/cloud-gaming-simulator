from typing import List

from controller import Controller
from game import Game
from topologygraph import TopologyGraph





class MockController(Controller):
    def get_feedback(self, packet):
        pass

    def preprocess(self):
        pass

    def __init__(self):
        self.paths_by_game = None

    def initialize(self, tg: TopologyGraph, games: List[Game]):
        paths_by_host = tg.get_path_dict()
        self.paths_by_game = group_by_game(paths_by_host, games)

    def set_path(self, packet):
        p1 = self.paths_by_game[packet.game][0]
        p2 = self.paths_by_game[packet.game][0][-2::-1]
        packet.set_path(p1+p2)

