from loaders import load_games, load_topology
from simulation import SimulationEngine

if __name__ == '__main__':
    games = load_games("games.json")
    topology = load_topology("topology.json")
    controller = None
    sim_engine = SimulationEngine(games, topology, controller)
    sim_engine.start(100)
    sim_engine.create_report()
