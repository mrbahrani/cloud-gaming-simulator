from typing import List

from controller import Controller
from game import Game
from topologygraph import TopologyGraph


def group_by_game(paths_by_host, games: List[Game]):
    result = dict()
    for game in games:
        result[game] = []
        for host in game.hosts:
            result[game] += paths_by_host[host]
    return result


class MockController(Controller):
    def __init__(self, tg: TopologyGraph, games: List[Game]):
        paths_by_host = tg.dfs()
        self.paths_by_game = group_by_game(paths_by_host, games)

    def set_path(self, packet):
        pass

