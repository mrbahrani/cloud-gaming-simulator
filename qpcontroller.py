from abc import ABC
from typing import List, Dict

import numpy as np

from controller import Controller
from game import Game
from player import Player
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
    def __init__(self, game, player,  paths):
        self.alpha = 0.5
        self.epsilon = 0.5
        self.minimum_epsilon = 0.01
        self.game = game
        self.player= player
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
        if self.epsilon > self.minimum_epsilon and reward >= Reward().good:
            self.decay_epsilon()

    def complete_path(self, path):
        return path + path[-2::-1]

    def decay_epsilon(self):
        self.epsilon *= 0.99


class Reward:
    def __init__(self):
        self.great = 2
        self.good = 1
        self.neutral = 0
        self.bad = -1
        self.awful = -2
        self.dropped = -10


def reward_by_delay(delay, reward_obj):
    if delay < 50:
        return reward_obj.great
    elif delay < 65:
        return reward_obj.good
    elif delay < 80:
        return reward_obj.neutral
    elif delay < 100:
        return reward_obj.bad
    return reward_obj.awful


class QPController(Controller, ABC):
    def __init__(self, games):
        self.reward = Reward()
        self.games = games
        self.q_tables: Dict[(Game, Player), GameQTable] = dict()

    def initialize(self, tg: TopologyGraph):
        paths_by_host = tg.get_path_dict()
        self.create_q_tables(self.games, paths_by_host)

    def get_feedback(self, packet):
        idx, delay = packet.extras
        # reward = reward_by_delay(delay, self.reward)
        reward = packet.timeout - (packet.end - packet.start)
        self.q_tables[(packet.game, packet.player)].update_value(idx, reward)

    def set_path(self, packet):
        q_coin = np.random.random()
        q_table = self.q_tables[(packet.game, packet.player)]
        if q_coin < q_table.epsilon:
            idx, path = q_table.get_random_item()
        else:
            idx, path = q_table.get_random_item()
        packet.path = path
        packet.extras = [idx, 0]

    def preprocess(self):
        pass

    def create_q_tables(self, games, path_by_host):
        game_dict = group_by_game(path_by_host, games)
        for g in games:
            for p in g.players:
                self.q_tables[(g, p)] = GameQTable(g, p, game_dict[g])
