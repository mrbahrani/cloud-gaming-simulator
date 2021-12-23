from absgraph import AbstractGraph
from gateway import Gateway
from idgenerator import IDGenerator
from simulationentity import SimulationEntity


class TopologyGraph(AbstractGraph):
    def __init__(self, id_generator: IDGenerator):
        super().__init__()
        self.adj_list = dict()
        self.id_object_map = dict()
        self.id_gen = id_generator
        self.gateway = None

    def add_node(self, item: SimulationEntity):
        if isinstance(item, Gateway):
            self.gateway = item
        while item.id == 0 or item.id in self.adj_list:
            item.id = self.id_gen.getNextId()
        self.adj_list[item.id] = []
        self.id_object_map[item.id] = item
        return item

    def add_edge(self, item1: SimulationEntity, item2: SimulationEntity, edge_properties: dict):
        # ToDo exception handling
        self.adj_list[item1.id].append((item2.id, "out", edge_properties))
        self.adj_list[item2.id].append((item1.id, "in", edge_properties))

    def get_inward_edges(self, item):
        return map(lambda x: (x[0], x[2]), filter(lambda x: x[1] == "in", self.adj_list[item.id]))

    def get_outward_edges(self, item):
        return map(lambda x: (x[0], x[2]), filter(lambda x: x[1] == "out", self.adj_list[item.id]))

    def map(self, identity):
        if identity in self.id_object_map:
            return self.id_object_map[identity]
        return None

    def __iter__(self):
        pass

    def dfs(self, node=None):
        if node is None:
            node = self.gateway
        