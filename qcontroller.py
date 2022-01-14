from abc import ABC
from typing import List, Dict

import numpy as np

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


class GameQTable:
    def __init__(self, game, paths):
        self.alpha = 0.1
        self.game = game
        self.paths = paths
        self.table = np.zeros(len(paths))

    def get_max_item(self):
        x = self.table.argmax()
        return x, self.complete_path(self.paths[x])

    def get_random_item(self):
        n = len(self.paths)
        idx = np.random.randint(0, n)
        return idx, self.complete_path(self.paths[idx])

    def update_value(self, item, reward):
        self.table[item] += self.alpha * reward

    def complete_path(self, path):
        return path + path[-2::-1]

class Reward:
    def __init__(self):
        self.great = 2
        self.good = 1
        self.neutral = 0
        self.bad = -1
        self.awful = -2


def reward_by_delay(delay, reward_obj):
    if delay < 10:
        return reward_obj.great
    elif delay < 50:
        return reward_obj.good
    elif delay < 100:
        return reward_obj.neutral
    elif delay < 150:
        return reward_obj.bad
    return reward_obj.awful


class QController(Controller, ABC):
    def __init__(self, games):
        self.reward = Reward()
        self.epsilon = 0.1
        self.games = games
        self.q_tables: Dict[Game, GameQTable] = dict()

    def initialize(self, tg: TopologyGraph):
        paths_by_host = tg.get_path_dict()
        self.create_q_tables(self.games, paths_by_host)

    def get_feedback(self, packet):
        idx, delay = packet.extras
        reward = reward_by_delay(delay, self.reward)
        self.q_tables[packet.game].update_value(idx, reward)

    def set_path(self, packet):
        q_coin = np.random.random()
        if q_coin < self.epsilon:
            idx, path = self.q_tables[packet.game].get_random_item()
        else:
            idx, path = self.q_tables[packet.game].get_random_item()
        packet.path = path
        packet.extras = [idx, 0]

    def preprocess(self):
        pass

    def create_q_tables(self, games, path_by_host):
        game_dict = group_by_game(path_by_host, games)
        self.q_tables =  {g: GameQTable(g, game_dict[g]) for g in game_dict}
