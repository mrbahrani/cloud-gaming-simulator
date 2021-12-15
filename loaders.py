import json
from queue import Queue

from game import Game
from globals import global_id_generator
from host import Host
from switch import Switch
from topologygraph import TopologyGraph


def load_games(file_name:str= 'games.json'):
    with open(file_name, 'r') as games_file:
        games = json.load(games_file)
    gamesList = []
    print(games)
    for game_dict in games["games"]:
        print(game_dict)
        g = Game()
        g.id = game_dict["id"]
        g.hosts = game_dict["hosts"]
        gamesList.append(g)
    return gamesList


def parse_fat_tree_dict(topology_dict: dict):
    q = Queue()
    g = TopologyGraph(global_id_generator)
    for switch in topology_dict["switches"]:
        sw = Switch()
        g.add_node(sw)
        q.put((switch, sw))
    while not q.empty():
        s, p = q.get()
        if 'sub_switches' in s:
            for switch in s["sub_switches"]:
                sw = Switch()
                g.add_node(sw)
                q.put((switch, sw))
                g.add_edge(p, sw, {})
        if 'hosts' in s:
            for host in s["hosts"]:
                h = Host()
                g.add_node(h)
                g.add_edge(p, h, {})
    return g


def load_topology(file_name: str = 'topology.json', datacenter_name='cloud_gaming_dc'):
    with open(file_name, 'r') as games_file:
        topology_dict = json.load(games_file)["datacenters"][0]
    if topology_dict["type"] == "fat_tree":
        topology = parse_fat_tree_dict(topology_dict)
        return topology
    return None
