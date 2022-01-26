import json
from queue import Queue
from random import randint
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

ethernet = {
    "1GB": 134217.728,
    "10GB": 1342177.28
}

def convert_to_player(player_dict):
    dist = None
    if player_dict["packet_distribution"] == "uniform":
        dist = UniformTimeGenerator(0, 10, 1)
    return Player(player_dict["id"], dist, reach_out_time=randint(2, 7))


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


def load_games2(file_name:str= 'games.json'):
    with open(file_name, 'r') as games_file:
        games = json.load(games_file)
    games_list = []
    for game_dict in games["games"]:
        players: List[Player] = create_players(game_dict['players'])
        g = Game(global_id_generator.getNextId(), [71, 148], players)
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

def create_fat_tree_by_k(k: int) -> TopologyGraph:
    gt = Gateway()
    tg = TopologyGraph(global_id_generator)
    tg.add_node(gt)
    cores = []
    for i in range((k//2) ** 2):
        sw = Switch(global_id_generator.getNextId())
        cores.append(sw)
        tg.add_node(sw)
        bw = Bandwidth(rate=ethernet["10GB"])
        tg.add_edge(gt, sw, {"bandwidth": bw})
        tg.add_edge(sw, gt, {"bandwidth": bw})
    # create pots
    for i in range(k):
        edges = []
        aggregate = []
        for j in range(k//2):
            ed = Switch(global_id_generator.getNextId())
            edges.append(ed)
            tg.add_node(ed)
        for j in range(k//2):
            ag = Switch(global_id_generator.getNextId())
            aggregate.append(ag)
            tg.add_node(ag)
            for l in range(j*(k//2), (j+1)*(k//2)):
                bw = Bandwidth(rate=ethernet["10GB"])
                tg.add_edge(ag, cores[l], {"bandwidth": bw})
                tg.add_edge(cores[l], ag, {"bandwidth": bw})
            for ed in edges:
                bw = Bandwidth(rate=ethernet["10GB"])
                tg.add_edge(ag, ed, {"bandwidth": bw})
                tg.add_edge(ed, ag, {"bandwidth": bw})
        for s in edges:
            hosts = []
            for _ in range(k//2):
                h = Host(global_id_generator.getNextId())
                hosts.append(h)
                tg.add_node(h)
                bw = Bandwidth(rate=ethernet["1GB"])
                tg.add_edge(s, h, {"bandwidth": bw})
                tg.add_edge(h, s, {"bandwidth": bw})
    return tg

