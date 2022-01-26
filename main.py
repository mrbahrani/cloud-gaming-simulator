from numpy.random import randint

from game import Game
from globals import global_id_generator
from host import Host
from loaders import load_games, load_topology, create_fat_tree_by_k, load_games2
from mockcontroller import MockController
from player import Player
from qcontroller import QController
from qpcontroller import QPController
from simulation import SimulationEngine
import matplotlib.pyplot as plt

import numpy as np

from turncontroller import TurnBasedController


def create_players(count):
    return [Player(global_id_generator, None, np.random.uniform(5, 10)) for i in range(count)]


def create_games(game_count, topology, number_of_replicas):
    # count_of_players = np.random.random_integers(2, 20, game_count)
    count_of_players = [1 for i in range(game_count)]
    hosts = list(map(lambda x: x.id, filter(lambda x: isinstance(x, Host), topology.id_object_map.values())))
    tolerant_game_count = game_count //3 + game_count % 3
    medium_game_count = game_count //3
    sensitive_games = game_count //3
    games = [Game(global_id_generator, np.random.choice(hosts, number_of_replicas), create_players(count_of_players[i]),
                  100 if i < tolerant_game_count else (80 if i < tolerant_game_count+ medium_game_count else 65))
             for i in range(game_count)]
    return games


def chart1_2():
    delays = []
    delay_scores = []
    x = [20*i+5 for i in range(12)]
    for t in x:
        stats = do_experiment(10, 6, "QP", number_of_replicas=3, simulation_tim_min=t)
        delays.append(stats["delay_average"])
        delay_scores.append(stats["delay_score"])
    plt.bar(x, delays)
    plt.show()


def do_experiment(game_count, fat_tree_k, controller_type="QP", simulation_tim_min=30, number_of_replicas=2):
    controller = None
    topology = create_fat_tree_by_k(fat_tree_k)
    games = create_games(game_count, topology, number_of_replicas)
    if controller_type == "QP":
        controller = QPController(games)
    elif controller_type=="TB":
        controller = TurnBasedController(games)
    else:
        controller = MockController(games)
    sim_engine = SimulationEngine(games, topology, controller)
    sim_engine.start(simulation_tim_min * 60 * 1000)
    stats = sim_engine.create_report()
    return stats


if __name__ == '__main__':
    # games = load_games2("games.json")
    # # topology = load_topology("topology.json")
    # topology = create_fat_tree_by_k(4)
    # # controller = MockController(games)
    # controller = QPController(games)
    # sim_engine = SimulationEngine(games, topology, controller)
    # sim_engine.start(30*60*1000)
    # sim_engine.create_report()
    # stats = do_experiment(10, 6, "MK", number_of_replicas=2, simulation_tim_min=5)
    # f = open("ex1", "w")
    # f.write(str(stats))
    # f.close()
    for game_count in range(3, 10, 2):
        for k in [4, 6]:
            for controller_type in ["QP", "TB", "MK"]:
                for rep in range(2, 5):
                    for simu_time in [5, 30, 60, 120]:
                        f = open("./report/g{}_k{}_c{}_r{}_st{}.txt".
                                 format(game_count, k, controller_type, rep, simu_time), "w")
                        stats = do_experiment(game_count, k, controller_type, simu_time, rep)
                        f.write(str(stats))
                        f.close()


