from absgraph import AbstractGraph
from gateway import Gateway
from globals import global_id_generator
from host import Host
from idgenerator import IDGenerator
from simulationentity import SimulationEntity


class TopologyGraph(AbstractGraph):
    def __init__(self, id_generator: IDGenerator=global_id_generator):
        super().__init__()
        self.adj_list = dict()
        self.id_object_map = dict()
        self.id_gen = id_generator
        self.gateway = None

    def add_node(self, item: SimulationEntity):
        while item.id == 0 or item.id in self.adj_list:
            item.id = self.id_gen.getNextId()
        if isinstance(item, Gateway):
            self.gateway = item
            self.gateway.paths = [[self.gateway.id]]
        self.adj_list[item.id] = []
        self.id_object_map[item.id] = item
        return item

    def add_edge(self, item1: SimulationEntity, item2: SimulationEntity, edge_properties: dict):
        # ToDo exception handling
        if isinstance(item1, int):
            item1 = self.map(item1)
        if isinstance(item2, int):
            item2 = self.map(item2)

        self.adj_list[item1.id].append((item2.id, "out", edge_properties))
        self.adj_list[item2.id].append((item1.id, "in", edge_properties))
        for p in item1.paths:
            item2.paths.append(p+[item2.id])

    def get_edge_properties(self, item1, item2, direction="out"):
        if isinstance(item1, int):
            item1 = self.map(item1)
        if isinstance(item2, int):
            item2 = self.map(item2)
        if direction == "out":
            return list(filter(lambda x: x[0] == item2.id, self.get_outward_edges(item1)))[0][1]
        else:
            return list(filter(lambda x: x[0] == item2.id, self.get_inward_edges(item1)))[0][1]

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
        paths = dict()
        if node is None:
            node = self.gateway.id
        visited = dict(map(lambda x: (x[0], False), self.id_object_map.items()))
        stack = [node]
        while len(stack) != 0:
            n = stack.pop()
            visited[n] = True
            neighbors = self.get_outward_edges(n)
            for nn, _ in neighbors:
                if not visited[nn]:
                    stack.append(nn)
        return paths

    def get_path_dict(self):
        r = dict()
        for i, d in self.id_object_map.items():
            if isinstance(d, Host):
                r[i] = d.paths
        return r
