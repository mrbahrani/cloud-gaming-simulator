from loaders import load_games, load_topology
from mockcontroller import MockController
from qcontroller import QController
from simulation import SimulationEngine

if __name__ == '__main__':
    games = load_games("games.json")
    topology = load_topology("topology.json")
    # controller = MockController()
    controller = QController(games)
    sim_engine = SimulationEngine(games, topology, controller)
    sim_engine.start(1000)
    sim_engine.create_report()
