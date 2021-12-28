from abc import ABC


class AbstractGraph(ABC):
    def __init__(self):
        pass

    def add_node(self, item):
        raise NotImplementedError

    def add_edge(self, item1, item2, edge_properties:dict):
        raise NotImplementedError

    def get_inward_edges(self, item):
        raise NotImplementedError

    def get_outward_edges(self, item):
        raise NotImplementedError

    def get_edge_properties(self, item1, item2, direction="out"):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def map(self, identity):
        raise NotImplementedError
