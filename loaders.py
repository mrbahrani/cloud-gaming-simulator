import json
from queue import Queue
from typing import List

from bandwidth import Bandwidth
from game import Game
from gateway import Gateway
from globals import global_id_generator
from host import Host
from player import Player
from switch import Switch
from topologygraph import TopologyGraph
from globals import global_id_generator
from uniformgenerator import UniformTimeGenerator


def convert_to_player(player_dict):
    dist = None
    if player_dict["packet_distribution"] == "uniform":
        dist = UniformTimeGenerator(0, 10, 1)
    return Player(player_dict["id"], dist)


def create_players(player_dicts):
    return list(map(convert_to_player, player_dicts))


def load_games(file_name:str= 'games.json'):
    with open(file_name, 'r') as games_file:
        games = json.load(games_file)
    games_list = []
    for game_dict in games["games"]:
        players: List[Player] = create_players(game_dict['players'])
        g = Game(global_id_generator.getNextId(), list(map(hash, game_dict['hosts'])), players)
        games_list.append(g)
    return games_list


def parse_fat_tree_dict(topology_dict: dict):
    q = Queue()
    g = TopologyGraph(global_id_generator)
    # create the class gateway
    data_center_gateway = Gateway()
    g.add_node(data_center_gateway)
    for switch in topology_dict["switches"]:
        sw = Switch()
        g.add_node(sw)
        bw = Bandwidth()
        g.add_edge(data_center_gateway, sw, {"bandwidth": bw})
        g.add_edge(sw, data_center_gateway, {"bandwidth": bw})
        q.put((switch, sw))
    while not q.empty():
        s, p = q.get()
        if 'sub_switches' in s:
            for switch in s["sub_switches"]:
                sw = Switch()
                g.add_node(sw)
                q.put((switch, sw))
                bw = Bandwidth()
                g.add_edge(p, sw, {"bandwidth": bw})
                g.add_edge(sw, p, {"bandwidth": bw})
        if 'hosts' in s:
            for host in s["hosts"]:
                h = Host(identity=hash(host["name"]))
                g.add_node(h)
                bw = Bandwidth()
                g.add_edge(p, h, {"bandwidth": bw})
                g.add_edge(h, p, {"bandwidth": bw})
    return g


def load_topology(file_name: str = 'topology.json', datacenter_name='cloud_gaming_dc'):
    with open(file_name, 'r') as games_file:
        topology_dict = json.load(games_file)["datacenters"][0]
    if topology_dict["type"] == "fat_tree":
        topology = parse_fat_tree_dict(topology_dict)
        return topology
    return None
